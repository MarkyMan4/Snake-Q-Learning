import pygame
import sys
from random import random

MOVEEVENT = pygame.USEREVENT

WIDTH = 800
HEIGHT = 800
BLUE = (50,50,255)
WHITE = (255,255,255)
BACKGROUND = (0,0,0)
TILE_SIZE = [20, 20]

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

GAME_OVER = False
score = 0

class Snake:

	# This is used if I want the screen to display.
	# During training, the screen will not display since the AI can learn to play the game
	# without having it displayed on screen. This will speed up training
	def init_screen(self):
		global screen

		pygame.init()
		screen = pygame.display.set_mode((WIDTH, HEIGHT))

	def get_world(self):
		return grid

	# initialize global variables, draw the initial empty grid
	# display will not update in training mode
	def init_game(self, train_mode):
		global player
		global grid
		global pellet_pos
		global score
		global GAME_OVER
		global T
		global is_training

		is_training = train_mode

		# this will be a list of tuples where each element is a position in the grid
		# this is the rest of the snake
		player = []
		grid = [[BACKGROUND for i in range(40)] for j in range(40)]
		pellet_pos = (0,0)

		score = 0
		GAME_OVER = False

		# the T value controls how fast the snake moves, the grid is updated every T milliseconds
		T = 75
		pygame.time.set_timer(MOVEEVENT, T)

		self.update_grid()

	# redraws the grid, this is called each time the snake moves
	def update_grid(self):
		for i in range(0, len(grid)):
			for j in range(0, len(grid[i])):

				if not is_training:
					pygame.draw.rect(screen, grid[i][j], (i * TILE_SIZE[0], j * TILE_SIZE[1], TILE_SIZE[0], TILE_SIZE[1]))

		if not is_training:
			pygame.display.update()

	# pick a random starting point for the player
	# spawn the initial pellet
	def init_player_and_pellet(self):
		player_random_x = int(random() * len(grid))
		player_random_y = int(random() * len(grid[0]))
		player.append((player_random_x,player_random_y))

		grid[player_random_x][player_random_y] = BLUE

		self.new_pellet()

	# spawn a pellet at a random location
	# won't spawn a pellet directly on the snake
	def new_pellet(self):
		pellet_random_x = int(random() * len(grid))
		pellet_random_y = int(random() * len(grid[0]))

		while grid[pellet_random_x][pellet_random_y] == BLUE:
			pellet_random_x = int(random() * len(grid))
			pellet_random_y = int(random() * len(grid[0]))

		pellet_pos = (pellet_random_x,pellet_random_y)
		grid[pellet_random_x][pellet_random_y] = WHITE

	# check if the snake is about to hit the wall or its own body
	def is_collision(self, new_tile):
		if new_tile[0] < 0 or new_tile[0] >= len(grid) or new_tile[1] < 0 or new_tile[1] >= len(grid[0]) \
			or grid[new_tile[0]][new_tile[1]] == BLUE:
			return True

		return False

	# Updates the position of the snake and each body part for a single time step.
	# This doesn't actually draw any components, it sets the colors and the list of
	# positions stored in player. The components get redrawn when update_grid() is called
	def update_player(self, direction):
		global GAME_OVER
		global score
		global T

		new_tile = (0,0)
		head = player[0]

		# update position of head
		if direction == UP:
			new_tile = (head[0], head[1] - 1)
		elif direction == DOWN:
			new_tile = (head[0], head[1] + 1)
		elif direction == LEFT:
			new_tile = (head[0] - 1, head[1])
		elif direction == RIGHT:
			new_tile = (head[0] + 1, head[1])

		if self.is_collision(new_tile):
			GAME_OVER = True
			return

		end_of_tail = player[len(player) - 1]

		# update position of the rest of the body
		for i in range(len(player) - 1, 0, -1):
			player[i] = player[i - 1]
			body_part_pos = player[i]
			grid[body_part_pos[0]][body_part_pos[1]] = BLUE

		grid[end_of_tail[0]][end_of_tail[1]] = BACKGROUND

		if grid[new_tile[0]][new_tile[1]] == WHITE:
			score += 1
			player.append(end_of_tail)
			self.new_pellet()

		player[0] = new_tile
		grid[new_tile[0]][new_tile[1]] = BLUE

	# main game loop
	# listens for events and key presses
	def game_loop(self):
		self.init_player_and_pellet()

		# set the initial direction
		# could be a random direction too
		direction = UP

		while not GAME_OVER:
			for event in pygame.event.get():
				if event.type == MOVEEVENT:
					self.update_player(direction)
					self.update_grid()

				if event.type == pygame.QUIT:
					sys.exit()

			keys = pygame.key.get_pressed()  #checking pressed keys

			# update direction of the head
			if keys[pygame.K_w]:
				direction = UP
			elif keys[pygame.K_s]:
				direction = DOWN
			elif keys[pygame.K_a]:
				direction = LEFT
			elif keys[pygame.K_d]:
				direction = RIGHT

			if keys[pygame.K_ESCAPE]:
				sys.exit()

	def play(self):
		quit = False

		while not quit:
			self.init_screen()
			self.init_game(False)
			self.game_loop()

# s = Snake()
# s.play()