import serial
import pygame
import os, sys
import math, random, time
import copy


class Control(object):
	'''Class defines methods for how the controller will interact with the rat'''
	def __init__(self):
		'''initialize controls and communication stuff'''
		# init screen
		self.screen = pygame.display.get_surface()
		self.screen_rect = self.screen.get_rect()
		# get keys
		self.keys = pygame.key.get_pressed()
		# setup joystick, if not joysticks found, then joy=None
		self.joy = initialize_gamepad()
		
		# set up communication.
		self.c = serial.Serial('COM7', baudrate=9600, timeout=1)
		
		
		# points to represent the display positions
		self.desired = [x / 2.0 for x in SCREEN_SIZE]
		self.current = copy.deepcopy(self.desired)
		self.boundary_width = 20
		
		# real world constants
		self.FRAME_SIZE = (1,12) # inches
		self.STEPS_PER_ROT = 200
		self.CIRCUMFERENCE = math.pi * 1.25 # diameter in inches

		self.done = False
			
	
	
	def event_loop(self):
		'''handles events. Updates motor variables with axes of joysticks'''
		for event in pygame.event.get():
			self.keys = pygame.key.get_pressed()
			if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]: # handle quit
				self.done = True
			elif event.type == pygame.JOYBUTTONDOWN:
				print(event.button)
				if event.button == 0: # 'a' button
					self.handle_a()
				elif event.button == 7:
					pass # center system
	
	def handle_a(self):
		'''update display and motors'''
		delta_y = -self.desired[1] + self.current[1] # difference in display height

		delta_h = delta_y / SCREEN_SIZE[1] * self.FRAME_SIZE[1] # convert to distance in inches for robot

		steps = delta_h / self.CIRCUMFERENCE * self.STEPS_PER_ROT

		print(steps)
		self.c.write(bytearray(str(steps) + '\r', 'utf-8'))

		self.current = copy.deepcopy(self.desired)

	def update(self):
		self.x_stick = self.joy.get_axis(0)
		if abs(self.x_stick) > 0.1:
			#self.c.write(bytearray('lu\r', 'utf-8'))
			self.desired[0] += 2.0 * self.x_stick
			if self.desired[0] > SCREEN_SIZE[0]:
				self.desired[0] = SCREEN_SIZE[0]
			elif self.desired[0] < 0:
				self.desired[0] = 0

		self.y_stick = self.joy.get_axis(1)
		if abs(self.y_stick) > 0.1:
			#self.c.write(bytearray('ru\r', 'utf-8'))
			self.desired[1] += 2.0 * self.y_stick
			if self.desired[1] > SCREEN_SIZE[1]:
				self.desired[1] = SCREEN_SIZE[1]
			elif self.desired[1] < 0:
				self.desired[1] = 0

	def draw(self):
		#draw background 
		pygame.display.get_surface().fill(BACKGROUND_COLOR)
		#draw border
		pygame.draw.rect(pygame.display.get_surface(), GRAY, [0,									0,									self.boundary_width,	SCREEN_SIZE[1]])
		pygame.draw.rect(pygame.display.get_surface(), GRAY, [0,									0,									SCREEN_SIZE[0],			self.boundary_width])
		pygame.draw.rect(pygame.display.get_surface(), GRAY, [SCREEN_SIZE[0]-self.boundary_width,	0,									self.boundary_width,	SCREEN_SIZE[1]])
		pygame.draw.rect(pygame.display.get_surface(), GRAY, [0,									SCREEN_SIZE[1]-self.boundary_width,	SCREEN_SIZE[0],	self.boundary_width])
		# draw cur and desired
		pygame.draw.rect(pygame.display.get_surface(), BLUE, [self.current[0]-5, self.current[1]-5, 10,10])
		pygame.draw.rect(pygame.display.get_surface(), RED, [self.desired[0]-5, self.desired[1]-5, 10,10])


		
	def main_loop(self):
		'''main loop'''
		while not self.done:
			self.event_loop()
			self.update()
			self.draw()

			pygame.display.flip()
			pygame.time.wait(10)

			

def text_objects(text, font):
	text_surface = font.render(text, True, (255,255,255))
	return text_surface, text_surface.get_rect()

def initialize_gamepad():
	'''checks for gamepads and returns an intialized list of them if found'''
	joystick = None
	if not pygame.joystick.get_count(): 
		print('please connect controller')
	while not pygame.joystick.get_count():
		print('.', end='')
		pygame.time.wait(1000)
		
	joystick = (pygame.joystick.Joystick(0))
	joystick.init() 
	return joystick
	
def main():
	'''prepare display and start program'''
	os.environ['SLD_VIDEO_CENTERED'] = '1'
	#pygame window setup 
	pygame.init()
	pygame.display.set_caption(CAPTION)
	GAME_DISPLAY=pygame.display.set_mode(SCREEN_SIZE)
	dir_path = os.path.dirname(os.path.realpath(__file__))
	
	Control().main_loop()
	
	pygame.quit()
	sys.exit()
	

CAPTION = 'Motor Controller'
SCREEN_SIZE = (200,300)
BACKGROUND_COLOR = (0,0,0)
GRAY = (150,150,150)
RED = (255,0,0)
BLUE = (0,0,255)


if __name__ == '__main__':
	
	main()
	
