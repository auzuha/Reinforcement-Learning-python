import pygame
import random
import pickle
import time

class Game:
    def __init__(self,H=600,W=600):
        pygame.init()
        self.H = H
        self.W = W
        self.screen = pygame.display.set_mode((self.W + 240,self.H ))
        self.clock = pygame.time.Clock()
        self.speed = 20
        self.block = 10
        self.num_blocks = self.H // self.block
        self.states_dict = {"food_right":0,"food_up":1,"danger_up":2, "danger_right":3, "danger_down":4, "danger_left":5}
        self.move_vector = [1,0,0,0]
        self.xchange = 0
        self.ychange = -self.block
        self.qtable = [[None]*4 for i in range(64)]
        for i in range(len(self.qtable)):
            self.qtable[i] = [random.uniform(0,1), random.uniform(0,1), random.uniform(0,1), random.uniform(0,1)]
        self.food_x = random.randint(0,self.num_blocks-1)*self.block 
        self.food_y = random.randint(0,self.num_blocks-1)*self.block
        self.t1 = time.time()
        self.states = [0 for i in range(len(self.states_dict))]
        self.reward = None
        self.dead_by_bounds = False
        self.dead_by_eating_itself = False
        self.visualize_food = [[0,0,0]* 3]
        self.visualize_danger = [[0,0,0]* 3]
        self.food_eaten = False
    def visualize(self,agent):
        state = self.get_state(agent)
        self.visualize_food = state[:2]
        self.visualize_danger = state[2:]      
        if self.visualize_danger[0] == [0,0,0,0]:
            pygame.draw.rect(self.screen,(0,0,0),[self.W,160,80,80])
            pygame.draw.rect(self.screen,(0,0,0),[self.W,0,80,80])
            pygame.draw.rect(self.screen,(0,0,0),[self.W+160,160,80,80])
            pygame.draw.rect(self.screen,(0,0,0),[self.W+160,0,80,80])
        if self.visualize_danger[3] == 1:
            pygame.draw.rect(self.screen,(200,0,0),[self.W,80,80,80])
        if self.visualize_danger[2] == 1:
            pygame.draw.rect(self.screen,(200,0,0),[self.W+80,160,80,80])
        if self.visualize_danger[1] == 1:
            pygame.draw.rect(self.screen,(200,0,0),[self.W+160,80,80,80])
        if self.visualize_danger [0]== 1:
            pygame.draw.rect(self.screen,(200,0,0),[self.W+80,0,80,80])
        pygame.draw.rect(self.screen,(0,0,255),[self.W+80,80,80,80])
        pygame.draw.line(self.screen,(255,255,255),(self.W,0),(self.W,self.H + 20))
        pygame.draw.line(self.screen, (255,255,255),(self.W,0),(self.W + 240,0))
        
        pygame.draw.line(self.screen,(255,255,255),(self.W + 239,0),(self.W+239,240))
        pygame.draw.line(self.screen,(255,255,255),(self.W + 0*80,0),(self.W + 0*80, 240))
        pygame.draw.line(self.screen, (255,255,255), (self.W,(0+1)*80) , (self.W + 240,(0+1)*80))
        pygame.draw.line(self.screen,(255,255,255),(self.W + 1*80,0),(self.W + 1*80, 240))
        pygame.draw.line(self.screen, (255,255,255), (self.W,(1+1)*80) , (self.W + 240,(1+1)*80))
        pygame.draw.line(self.screen,(255,255,255),(self.W + 2*80,0),(self.W + 2*80, 240))
        pygame.draw.line(self.screen, (255,255,255), (self.W,(2+1)*80) , (self.W + 240,(2+1)*80))
        

    def get_reward(self, agent):
        self.reward = 0
        if [self.food_x ,self.food_y] in agent.body or [agent.head[0] ,agent.head[1]] == [self.food_x ,self.food_y]:
            self.reward = 300
        if [agent.head[0] ,agent.head[1]] in agent.body:
            self.reward = - 75
        if [agent.head[0] ,agent.head[1]] in agent.body:
            self.reward = - 75
        if agent.head[0] >= self.W or agent.head[0] < 0 or agent.head[1] >= self.H or agent.head[1] < 0:
            self.reward = -50
        return self.reward
    def get_state(self ,agent):
        self.state = [0 for i in range(6)]
        if self.food_x > agent.head[0]:
            self.state[0] = 1
        if self.food_y < agent.head[1]:
            self.state[1] = 1
        if agent.head[1] - self.block < 0 or [agent.head[0], agent.head[1] - self.block] in agent.body:
            self.state[2] = 1
        if agent.head[0] + self.block >= self.W or [agent.head[0] + self.block,agent.head[1]] in agent.body:
            self.state[3] = 1
        if agent.head[1] + self.block >= self.H or [agent.head[0], agent.head[1]+self.block] in agent.body:
            self.state[4] = 1
        if agent.head[0] - self.block < 0 or [agent.head[0]-self.block, agent.head[1]] in agent.body:
            self.state[5] = 1
        return self.state
    def spawn_food(self):
        self.food_x = random.randint(1,self.num_blocks-1)
        self.food_y = random.randint(1,self.num_blocks-1)
        self.food_x *= self.block
        self.food_y *= self.block
        self.t1 = time.time()
    def move(self,agent,action):

        '''
        if self.move_vector.index(1) == 0:
            agent.head[1] -= self.block
        if self.move_vector.index(1) == 1:
            agent.head[0] += self.block
        if self.move_vector.index(1) == 2:
            agent.head[1] += self.block
        if self.move_vector.index(1) == 3:
            agent.head[0] -= self.block
        '''
        
        
                
        valid = False
        
        if action == 0 :
            valid = True
            tempx = agent.head[0]
            tempy = agent.head[1]
            self.ychange = -self.block
            self.xchange = 0
            if len(agent.body) >= 1:
                agent.body = [[tempx,tempy]] + agent.body[:-1]
            self.move_vector = [1,0,0,0]
        if action == 1:
            valid = True
            tempx = agent.head[0]
            tempy = agent.head[1]
            self.ychange = 0
            self.xchange = self.block
            if len(agent.body) >= 1:
                agent.body = [[tempx,tempy]] + agent.body[:-1]
            self.move_vector = [0,1,0,0]
        if action == 2:
            valid = True
            tempx = agent.head[0]
            tempy = agent.head[1]
            self.xchange = 0
            self.ychange = self.block
            if len(agent.body) >= 1:
                agent.body = [[tempx,tempy]] + agent.body[:-1]
            self.move_vector = [0,0,1,0]
        if action == 3:
            valid = True
            tempx = agent.head[0]
            tempy = agent.head[1]
            self.xchange = -self.block
            self.ychange = 0
            if len(agent.body) >= 1:
                agent.body = [[tempx,tempy]] + agent.body[:-1]
            self.move_vector = [0,0,0,1]
        if valid:
            agent.head[0] += self.xchange
            agent.head[1] += self.ychange
        else:
            if self.move_vector == [1,0,0,0]:
                self.xchange = 0
                self.ychange = -self.block
            if self.move_vector == [0,1,0,0]:
                self.xchange = self.block
                self.ychange = 0
            if self.move_vector == [0,0,1,0]:
                self.xchange = 0
                self.ychange = self.block
            if self.move_vector == [0,0,0,1]:
                self.xchange = -self.block
                self.ychange = 0
            agent.head[0] += self.xchange
            agent.head[1] += self.ychange
    def get_next_action(self,agent,state):
        if random.uniform(0,1) < agent.epsilon:
            if state == [0,0,0,0,0,0]:
                return self.qtable[0].index(max(self.qtable[0]))
            if state == [0,1,0,0,0,0]:
                return self.qtable[1].index(max(self.qtable[1]))
            if state == [1,0,0,0,0,0]:
                return self.qtable[2].index(max(self.qtable[2]))
            if state == [1,1,0,0,0,0]:
                return self.qtable[3].index(max(self.qtable[3]))
            if state == [0,0,1,0,0,0]:
                return self.qtable[4].index(max(self.qtable[4]))
            if state == [0,1,1,0,0,0]:
                return self.qtable[5].index(max(self.qtable[5]))
            if state == [1,0,1,0,0,0]:
                return self.qtable[6].index(max(self.qtable[6]))
            if state == [1,1,1,0,0,0]:
                return self.qtable[7].index(max(self.qtable[7]))
            if state == [0,0,0,1,0,0]:
                return self.qtable[8].index(max(self.qtable[8]))
            if state == [0,1,0,1,0,0]:
                return self.qtable[9].index(max(self.qtable[9]))
            if state == [1,0,0,1,0,0]:
                return self.qtable[10].index(max(self.qtable[10]))
            if state == [1,1,0,1,0,0]:
                return self.qtable[11].index(max(self.qtable[11]))
            if state == [0,0,1,1,0,0]:
                return self.qtable[12].index(max(self.qtable[12]))
            if state == [0,1,1,1,0,0]:
                return self.qtable[13].index(max(self.qtable[13]))
            if state == [1,0,1,1,0,0]:
                return self.qtable[14].index(max(self.qtable[14]))
            if state == [1,1,1,1,0,0]:
                return self.qtable[15].index(max(self.qtable[15]))
            if state == [0,0,0,1,1,0]:
                return self.qtable[16].index(max(self.qtable[16]))
            if state == [0,1,0,1,1,0]:
                return self.qtable[17].index(max(self.qtable[17]))
            if state == [1,0,0,1,1,0]:
                return self.qtable[18].index(max(self.qtable[18]))
            if state == [1,1,0,1,1,0]:
                return self.qtable[19].index(max(self.qtable[19]))
            if state == [0,0,0,0,1,0]:
                return self.qtable[20].index(max(self.qtable[20]))
            if state == [0,1,0,0,1,0]:
                return self.qtable[21].index(max(self.qtable[21]))
            if state == [1,0,0,0,1,0]:
                return self.qtable[22].index(max(self.qtable[22]))
            if state == [1,1,0,0,1,0]:
                return self.qtable[23].index(max(self.qtable[23]))
            if state == [0,0,0,0,1,1]:
                return self.qtable[24].index(max(self.qtable[24]))
            if state == [0,1,0,0,1,1]:
                return self.qtable[25].index(max(self.qtable[25]))
            if state == [1,0,0,0,1,1]:
                return self.qtable[26].index(max(self.qtable[26]))
            if state == [1,1,0,0,1,1]:
                return self.qtable[27].index(max(self.qtable[27]))
            if state == [0,0,0,0,0,1]:
                return self.qtable[28].index(max(self.qtable[28]))
            if state == [0,1,0,0,0,1]:
                return self.qtable[29].index(max(self.qtable[29]))
            if state == [1,0,0,0,0,1]:
                return self.qtable[30].index(max(self.qtable[30]))
            if state == [1,1,0,0,0,1]:
                return self.qtable[31].index(max(self.qtable[31]))
            if state == [0,0,1,0,0,1]:
                return self.qtable[32].index(max(self.qtable[32]))
            if state == [0,1,1,0,0,1]:
                return self.qtable[33].index(max(self.qtable[33]))
            if state == [1,0,1,0,0,1]:
                return self.qtable[34].index(max(self.qtable[34]))
            if state == [1,1,1,0,0,1]:
                return self.qtable[35].index(max(self.qtable[35]))
            if state == [0,0,1,0,1,0]:
                return self.qtable[36].index(max(self.qtable[36]))
            if state == [0,1,1,0,1,0]:
                return self.qtable[37].index(max(self.qtable[37]))
            if state == [1,0,1,0,1,0]:
                return self.qtable[38].index(max(self.qtable[38]))
            if state == [1,1,1,0,1,0]:
                return self.qtable[39].index(max(self.qtable[39]))
            if state == [0,0,0,1,0,1]:
                return self.qtable[40].index(max(self.qtable[40]))
            if state == [0,1,0,1,0,1]:
                return self.qtable[41].index(max(self.qtable[41]))
            if state == [1,0,0,1,0,1]:
                return self.qtable[42].index(max(self.qtable[42]))
            if state == [1,1,0,1,0,1]:
                return self.qtable[43].index(max(self.qtable[43]))
            if state == [0,0,1,1,1,1]:
                return self.qtable[44].index(max(self.qtable[44]))
            if state == [0,1,1,1,1,1]:
                return self.qtable[45].index(max(self.qtable[45]))
            if state == [1,0,1,1,1,1]:
                return self.qtable[46].index(max(self.qtable[46]))
            if state == [1,1,1,1,1,1]:
                return self.qtable[47].index(max(self.qtable[47]))
            if state == [0,0,1,1,0,1]:
                return self.qtable[48].index(max(self.qtable[48]))
            if state == [0,1,1,1,0,1]:
                return self.qtable[49].index(max(self.qtable[49]))
            if state == [1,0,1,1,0,1]:
                return self.qtable[50].index(max(self.qtable[50]))
            if state == [1,1,1,1,0,1]:
                return self.qtable[51].index(max(self.qtable[51]))
            if state == [0,0,0,1,1,1]:
                return self.qtable[52].index(max(self.qtable[52]))
            if state == [0,1,0,1,1,1]:
                return self.qtable[53].index(max(self.qtable[53]))
            if state == [1,0,0,1,1,1]:
                return self.qtable[54].index(max(self.qtable[54]))
            if state == [1,1,0,1,1,1]:
                return self.qtable[55].index(max(self.qtable[55]))
            if state == [0,0,1,1,1,0]:
                return self.qtable[56].index(max(self.qtable[56]))
            if state == [0,1,1,1,1,0]:
                return self.qtable[57].index(max(self.qtable[57]))
            if state == [1,0,1,1,1,0]:
                return self.qtable[58].index(max(self.qtable[58]))
            if state == [1,1,1,1,1,0]:
                return self.qtable[59].index(max(self.qtable[59]))
            if state == [0,0,1,0,1,1]:
                return self.qtable[60].index(max(self.qtable[60]))
            if state == [0,1,1,0,1,1]:
                return self.qtable[61].index(max(self.qtable[61]))
            if state == [1,0,1,0,1,1]:
                return self.qtable[62].index(max(self.qtable[62]))
            if state == [1,1,1,0,1,1]:
                return self.qtable[63].index(max(self.qtable[63]))
        else:
            return random.choice([0,1,2,3])
    def get_state_index(self,state):
        if state == [0,0,0,0,0,0]:
            return 0
        if state == [0,1,0,0,0,0]:
            return 1
        if state == [1,0,0,0,0,0]:
            return 2
        if state == [1,1,0,0,0,0]:
            return 3
        if state == [0,0,1,0,0,0]:
            return 4
        if state == [0,1,1,0,0,0]:
            return 5
        if state == [1,0,1,0,0,0]:
            return 6
        if state == [1,1,1,0,0,0]:
            return 7
        if state == [0,0,0,1,0,0]:
            return 8
        if state == [0,1,0,1,0,0]:
            return 9
        if state == [1,0,0,1,0,0]:
            return 10
        if state == [1,1,0,1,0,0]:
            return 11
        if state == [0,0,1,1,0,0]:
            return 12
        if state == [0,1,1,1,0,0]:
            return 13
        if state == [1,0,1,1,0,0]:
            return 14
        if state == [1,1,1,1,0,0]:
            return 15
        if state == [0,0,0,1,1,0]:
            return 16
        if state == [0,1,0,1,1,0]:
            return 17
        if state == [1,0,0,1,1,0]:
            return 18
        if state == [1,1,0,1,1,0]:
            return 19
        if state == [0,0,0,0,1,0]:
            return 20
        if state == [0,1,0,0,1,0]:
            return 21
        if state == [1,0,0,0,1,0]:
            return 22
        if state == [1,1,0,0,1,0]:
            return 23
        if state == [0,0,0,0,1,1]:
            return 24
        if state == [0,1,0,0,1,1]:
            return 25
        if state == [1,0,0,0,1,1]:
            return 26
        if state == [1,1,0,0,1,1]:
            return 27
        if state == [0,0,0,0,0,1]:
            return 28
        if state == [0,1,0,0,0,1]:
            return 29
        if state == [1,0,0,0,0,1]:
            return 30
        if state == [1,1,0,0,0,1]:
            return 31
        if state == [0,0,1,0,0,1]:
            return 32
        if state == [0,1,1,0,0,1]:
            return 33
        if state == [1,0,1,0,0,1]:
            return 34
        if state == [1,1,1,0,0,1]:
            return 35
        if state == [0,0,1,0,1,0]:
            return 36
        if state == [0,1,1,0,1,0]:
            return 37
        if state == [1,0,1,0,1,0]:
            return 38
        if state == [1,1,1,0,1,0]:
            return 39
        if state == [0,0,0,1,0,1]:
            return 40
        if state == [0,1,0,1,0,1]:
            return 41
        if state == [1,0,0,1,0,1]:
            return 42
        if state == [1,1,0,1,0,1]:
            return 43
        if state == [0,0,1,1,1,1]:
            return 44
        if state == [0,1,1,1,1,1]:
            return 45
        if state == [1,0,1,1,1,1]:
            return 46
        if state == [1,1,1,1,1,1]:
            return 47
        if state == [0,0,1,1,0,1]:
            return 48
        if state == [0,1,1,1,0,1]:
            return 49
        if state == [1,0,1,1,0,1]:
            return 50
        if state == [1,1,1,1,0,1]:
            return 51
        if state == [0,0,0,1,1,1]:
            return 52
        if state == [0,1,0,1,1,1]:
            return 53
        if state == [1,0,0,1,1,1]:
            return 54
        if state == [1,1,0,1,1,1]:
            return 55
        if state == [0,0,1,1,1,0]:
            return 56
        if state == [0,1,1,1,1,0]:
            return 57
        if state == [1,0,1,1,1,0]:
            return 58
        if state == [1,1,1,1,1,0]:
            return 59
        if state == [0,0,1,0,1,1]:
            return 60
        if state == [0,1,1,0,1,1]:
            return 61
        if state == [1,0,1,0,1,1]:
            return 62
        if state == [1,1,1,0,1,1]:
            return 63
    def play_step(self,agent,save=False):
        if agent.head == [self.food_x ,self.food_y] or [self.food_x ,self.food_y] in agent.body:
            #agent.body.append([self.food_x ,self.food_y])

            if self.move_vector == [1,0,0,0]:
                agent.body.append([agent.body[-1][0],agent.body[-1][1] + self.block])
            if self.move_vector == [0,1,0,0]:
                agent.body.append([agent.body[-1][0]  - self.block ,agent.body[-1][1]])
            if self.move_vector == [0,0,1,0]:
                agent.body.append([agent.body[-1][0],agent.body[-1][1] - self.block])
            if self.move_vector == [0,0,0,1]:
                agent.body.append([agent.body[-1][0]  + self.block ,agent.body[-1][1]])
            self.spawn_food()

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if save:
                    self.save_qtable("snake-reinforcement-learning-qtable")
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.speed -= 10
                    print("speed is now",self.speed)
                if event.key == pygame.K_d:
                    self.speed += 10
                    print("speed is now",self.speed)

        self.screen.fill((0,0,0))
        #render snake



        pygame.draw.rect(self.screen, (0,0,255), [agent.head[0], agent.head[1], self.block, self.block])
        
        for i in range(len(agent.body)):
            pygame.draw.rect(self.screen, (0,255,0), [agent.body[i][0], agent.body[i][1], self.block, self.block],1,1,1,1,1,1)
            
            
        #render food
        pygame.draw.rect(self.screen ,(255 ,0 ,0) ,[self.food_x, self.food_y, self.block, self.block])

        self.visualize(agent)

        pygame.display.update()
        self.clock.tick(self.speed)
    def isGameOver(self,agent):
        if [agent.head[0],agent.head[1]] in agent.body:
            self.dead_by_eating_itself = True
            return True
        if agent.head[0] < 0 or agent.head[1] < 0 or agent.head[1] >= self.H or agent.head[0] >= self.W:
            self.dead_by_bounds = True
            return True
        return False
    def reset(self,agent):
        agent.head = [300,300]
        agent.body = [[300,320], [300,340]]
        self.move_vector = [1,0,0,0]
        self.xchange = 0
        self.ychange = -self.block
        self.food_x = random.randint(0,self.num_blocks-1)*self.block 
        self.food_y = random.randint(0,self.num_blocks-1)*self.block
        self.reward = 0
        self.dead_by_bounds = False
        self.dead_by_eating_itself = False
        self.t1 = time.time()
    def load_qtable(self,path):
        with open(f"{path}.pkl","rb") as f:
            self.qtable = pickle.load(f)
    def save_qtable(self,path):
        with open(f"{path}.pkl","wb") as f:
            pickle.dump(self.qtable, f)

class Agent:
    def __init__(self):
        self.head = [300,300]
        self.body = [[300,320], [300,340]]
        self.epsilon = 1

def main():
    game = Game()
    agent = Agent()
    num_episodes = 8000
    game.load_qtable("snake-reinforcement-learning-qtable")
    for i in range(1,num_episodes+1):
        cumulative_reward = 0
        if i == 6000:
            game.speed = 10
        while True:            
            if game.isGameOver(agent) or time.time()-game.t1 > 15:
                print(f"Episode {i} end.",end="")
                if game.dead_by_bounds:
                    print("Dead by wall.")
                elif game.dead_by_eating_itself:
                    print("Dead by eating itself.")
                else:
                    print("Dead by starvation.")
                game.reset(agent)
                break
            #print(agent.head,game.isGameOver(agent))
            game.play_step(agent,save=False)
            state = game.get_state(agent)
            action = game.get_next_action(agent,state)
            curr_q = game.qtable[game.get_state_index(state)][action]
            game.move(agent, action)
            reward = game.get_reward(agent)
            cumulative_reward += reward
            new_q = curr_q + 0.05*(reward + 1*game.qtable[game.get_state_index(game.get_state(agent))][game.get_next_action(agent,game.get_state(agent))] - curr_q)
            game.qtable[game.get_state_index(state)][action] = new_q

            
        print(cumulative_reward)   
          

if __name__ == "__main__":
    
    main()