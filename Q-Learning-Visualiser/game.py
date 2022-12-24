import pickle,random,pygame
class Game:
    def __init__(self,H=480,W=480,block=80):
        
        self.maze = [[0,0,0,0,0,0],
                    [0,1,0,0,1,-2],
                    [0,0,-2,0,0,0],
                    [0,0,0,1,0,-2],
                    [0,-2,0,0,0,0],
                    [1,0,0,0,-2,-1],]
        
        self.obstacles = []
        self.goal = []
        self.fires = []
        self.total_return = 0

        self.death_by_fire = False
        self.death_by_winning = False
        self.direction_dict = {0:"UP" ,1:"RIGHT", 2:"DOWN", 3:"LEFT"}
        for i in range(len(self.maze)):
            for j in range(len(self.maze)):
                if self.maze[i][j] == 1:
                    self.obstacles.append([j*80 ,i*80])
                if self.maze[i][j] == -1:
                    self.goal.append([j*80,i*80])
                if self.maze[i][j] == -2:
                    self.fires.append([j*80 ,i*80])

        
        self.qtable = [[None]*len(self.maze) for i in range(len(self.maze))]
        for i in range(len(self.qtable)):
            for j in range(len(self.qtable)):
                self.qtable[i][j] = [random.uniform(0,1),random.uniform(0,1),random.uniform(0,1),random.uniform(0,1)]
        ## actions 0,1,2,3 index in qtable are UP ,Right ,down ,left
        
        

            
        self.H = H
        self.W = W
        self.block = block
        self.total_moves = 0
        self.reward = 0
        self.gameOver = False
        self.speed = 2;
        pygame.init()
        self.clock = pygame.time.Clock()
        self.scr = pygame.display.set_mode((H,W))
    def play_step(self ,agent,display_qtable = False):
        #returns reward , gameover
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_qtable("qtable_saved")
                pygame.quit()
                quit()
        
        #fill screen with black
        self.scr.fill((0,0,0))

        #draw agent blockk
        pygame.draw.rect(self.scr ,(127,127,127) ,[agent.x ,agent.y,self.block,self.block])


        #utility to visualise learning policy  
        if display_qtable:
            for i in range(len(self.qtable)):
                for j in range(len(self.qtable)):
                    act = self.qtable[i][j].index(max(self.qtable[i][j]))
                    mid_coord_x = j*self.block + self.block // 2 
                    mid_coord_y = i*self.block + self.block // 2
                    if act == 0:
                        pygame.draw.line(self.scr ,(255,255,255) ,(mid_coord_x ,mid_coord_y) , (mid_coord_x , mid_coord_y - 15))
                        pygame.draw.line(self.scr , (255,255,255) ,(mid_coord_x , mid_coord_y - 15),(mid_coord_x+5,mid_coord_y-15+5))
                        pygame.draw.line(self.scr , (255,255,255) ,(mid_coord_x , mid_coord_y - 15),(mid_coord_x-5,mid_coord_y-15+5))
                        
                    if act == 1:
                        pygame.draw.line(self.scr ,(255,255,255) ,(mid_coord_x ,mid_coord_y) , (mid_coord_x + 15 , mid_coord_y))
                        pygame.draw.line(self.scr ,(255,255,255) ,(mid_coord_x+15 ,mid_coord_y) , (mid_coord_x + 15 - 5 , mid_coord_y - 5))
                        pygame.draw.line(self.scr ,(255,255,255) ,(mid_coord_x+15 ,mid_coord_y) , (mid_coord_x + 15 - 5 , mid_coord_y + 5))
                    if act == 2:
                        pygame.draw.line(self.scr ,(255,255,255) ,(mid_coord_x ,mid_coord_y) , (mid_coord_x , mid_coord_y + 15))
                        pygame.draw.line(self.scr ,(255,255,255) ,(mid_coord_x ,mid_coord_y+15) , (mid_coord_x - 5 , mid_coord_y + 15 - 5))
                        pygame.draw.line(self.scr ,(255,255,255) ,(mid_coord_x ,mid_coord_y + 15) , (mid_coord_x + 5 , mid_coord_y + 15 - 5))
                    if act == 3:
                        pygame.draw.line(self.scr ,(255,255,255) ,(mid_coord_x ,mid_coord_y) , (mid_coord_x - 15 , mid_coord_y))
                        pygame.draw.line(self.scr ,(255,255,255) ,(mid_coord_x - 15  ,mid_coord_y) , (mid_coord_x - 15 + 5 , mid_coord_y - 5))
                        pygame.draw.line(self.scr ,(255,255,255) ,(mid_coord_x - 15  ,mid_coord_y) , (mid_coord_x - 15 + 5 , mid_coord_y + 5))
        

        

        #draw obstacles , fires & goal
        pygame.draw.rect(self.scr, (0,0,70), [0, 0,self.block, self.block])
        for i in range(len(self.obstacles)):
            pygame.draw.rect(self.scr ,(200,150,0) ,[self.obstacles[i][0],self.obstacles[i][1],self.block,self.block])
        for i in range(len(self.fires)):   
            pygame.draw.rect(self.scr ,(200,0,0) ,[self.fires[i][0],self.fires[i][1],self.block,self.block])
        for i in range(len(self.goal)):   
            pygame.draw.rect(self.scr ,(0,150,0) ,[self.goal[i][0],self.goal[i][1],self.block,self.block])            

        #update display , set frame rate
        pygame.display.update()
        self.clock.tick(self.speed)
        return self.isGameOver(agent)
                
                

        
    def isGameOver(self,agent):
        if [agent.x ,agent.y] in self.fires:
            self.death_by_fire = True
            return True
        if [agent.x,agent.y] in self.goal:            
            self.death_by_winning = True
            return True
        return False
    def reset(self,agent):
        self.reward = 0
        self.gameOver = False
        agent.x = 0
        agent.y = 0
        self.total_return = 0
        self.total_moves = 0
        self.death_by_fire = False
        self.death_by_winning = False
    
    def get_reward(self,agent,action):
        # needs agent state and action taken , 
        # St , at --> Rt
        self.reward = -1
        if action == 0:
            if agent.y - self.block < 0 or [agent.x ,agent.y - self.block] in self.obstacles:
                self.reward = -10
            if [agent.x ,agent.y - self.block] in self.fires:
                self.reward = -60
                self.death_by_fire = True
            if [agent.x ,agent.y - self.block] in self.goal:
                self.reward = 150
                self.death_by_winning = True

        if action == 1:
            if agent.x + self.block == self.W or [agent.x + self.block,agent.y] in self.obstacles:
                self.reward = -10
            if [agent.x + self.block ,agent.y] in self.fires:
                self.reward = -60
                self.death_by_fire = True
            if [agent.x + self.block ,agent.y] in self.goal:
                self.reward = 150
                self.death_by_winning = True
        if action == 2:
            if agent.y + self.block == self.H or [agent.x,agent.y + self.block] in self.obstacles:
                self.reward = -10
            if [agent.x,agent.y + self.block ] in self.fires:
                self.reward = -60
                self.death_by_fire = True
            if [agent.x,agent.y + self.block ] in self.goal:
                self.reward = 150
                self.death_by_winning = True
        if action == 3:
            if agent.x - self.block < 0 or [agent.x - self.block ,agent.y] in self.obstacles:
                self.reward = -10
            if [agent.x - self.block ,agent.y] in self.fires:
                self.reward = -60
                self.death_by_fire = True
            if [agent.x - self.block , agent.y] in self.goal:
                self.reward = 150
                self.death_by_winning = True
        
        return self.reward
    def move(self,agent,action):
        if action == 0:
            agent.y -= self.block
            if agent.y < 0:
                agent.y = 0
            if [agent.x ,agent.y] in self.obstacles:
                agent.y += self.block
        if action == 1:
            agent.x += self.block
            if agent.x >= self.W:
                agent.x = self.W - self.block
            if [agent.x ,agent.y] in self.obstacles:
                agent.x -= self.block
        if action == 2:
            agent.y += self.block
            if agent.y >= self.H:
                agent.y = self.H - self.block
            if [agent.x,agent.y] in self.obstacles:
                agent.y -= self.block
        if action == 3:
            agent.x -= self.block
            if agent.x < 0:
                agent.x = 0
            if [agent.x,agent.y] in self.obstacles:
                agent.x += self.block
        self.total_moves += 1
        
    def get_next_action(self,agent):
        if random.uniform(0,1) < agent.epsilon:
            #choose max action
            index_x = agent.y // self.block
            index_y = agent.x // self.block
            action = self.qtable[index_x][index_y].index(max(self.qtable[index_x][index_y]))
            self.action_chosen = action
            return action
        else:
            #choose random
            return random.choice([0,1,2,3])
    
    def save_qtable(self,path):
        with open(f"{path}.pkl","wb") as f:
            pickle.dump(self.qtable ,f)
    def load_qtable(self,path):
        with open(f"{path}.pkl","rb") as f:
            self.qtable = pickle.load(f)