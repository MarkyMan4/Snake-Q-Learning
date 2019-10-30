from snake import Snake
import pygame
from random import random

UP = pygame.K_w
DOWN = pygame.K_d
LEFT = pygame.K_a
RIGHT = pygame.K_d
END = pygame.K_ESCAPE

BLUE = (50,50,255)
WHITE = (255,255,255)
BACKGROUND = (0,0,0)

MOVEEVENT = pygame.USEREVENT
T = 75
pygame.time.set_timer(MOVEEVENT, T)


EPISODES = 1000

def main():
	global s
	s = Snake()
	s.init_game(True)
	game_loop()

def get_random_move():
	return int(random() * 4)

# each step along the normal area is -1 reward
# the player hitting itself is -10 reward (this will apply to hitting a wall eventually too)
# getting the pellet is 0 reward
def init_rewards(world):
	rewards = [[0 for i in range(len(world))] for j in range(len(world[0]))]
	for i in range(len(world)):
		for j in range(len(world[i])):
			if world[i][j] == BACKGROUND: rewards[i][j] = -1
			if world[i][j] == BLUE: rewards[i][j] = -10
			if world[i][j] == WHITE: rewards[i][j] = 0

	return rewards

def game_loop():
	global GAME_OVER
	s.init_player_and_pellet()

	# set the initial direction
	# could be a random direction too
	direction = UP

	world = s.get_world()
	init_rewards(world)

	for i in range(EPISODES):
		direction = get_random_move()
		s.update_player(direction)
		s.update_grid()

	# world = s.get_world()

	# print(world)

if __name__ == '__main__':
	main()