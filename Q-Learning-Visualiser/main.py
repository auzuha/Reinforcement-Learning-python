from game import Game
from agent import Agent
import pygame

def main():
    running = True
    game = Game(480,480)
    agent = Agent()
    game_over = False
    num_episodes = 5000
    for i in range(1,num_episodes):
        repitition = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        game.speed -= 1
                    if event.key == pygame.K_RIGHT:
                        game.speed += 1
                    if event.key == pygame.K_DOWN:
                        game.speed = 1   
            if game.isGameOver(agent):
                break            
            if game.total_moves >= 50:
                repitition = True
                break
            action = game.get_next_action(agent)
            reward = game.get_reward(agent ,action)
            index_x = agent.y // game.block
            index_y = agent.x // game.block
            temp_action = action
            curr_q = game.qtable[index_x][index_y][temp_action]
            game.move(agent ,action)
            #reward = game.get_reward(agent ,action)
            new_q = curr_q + 0.04 * (reward + 1*game.qtable[agent.y//game.block][agent.x//game.block][game.get_next_action(agent)] - curr_q)
            game.qtable[index_x][index_y][temp_action] = new_q           
            game.play_step(agent,display_qtable=True)
        if game.death_by_fire:
            print("Cause of death:Fire",end='.')
            print(f"Episode {i} complete.")
        if game.death_by_winning:
            print("Cause of death:Suffering from success",end='.')
            print(f"Episode {i} complete.")
        if repitition:
            print("Cause of death:Repitition.",end='.')
            print(f"Episode {i} complete.")
        if i % 10 == 0:
            agent.epsilon += 0.005
        game.reset(agent)

if __name__ == "__main__":
    main()