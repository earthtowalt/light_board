import serial
import pygame
import os, sys
import math, random, time

CAPTION = 'Motor Controller'
SCREEN_SIZE = (320,200)
BACKGROUND_COLOR = (0,0,0)





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

		self.done = False
			
	
	
	def event_loop(self):
		'''handles events. Updates motor variables with axes of joysticks'''
		for event in pygame.event.get():
			self.keys = pygame.key.get_pressed()
			if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]: # handle quit
				self.done = True
			elif event.type == pygame.JOYBUTTONDOWN:
				if event.button == 7:
					pass
					self.c.write(bytearray('100\r', 'utf-8'))
					print('sent 100')

	def update(self):
		# print(self.joy.get_axis(1))
		self.left_stick = -round(self.joy.get_axis(1))
		if self.left_stick < -0.15:
			self.c.write(bytearray('ld\r', 'utf-8'))
			print('ld')
		elif self.left_stick > 0.15:
			self.c.write(bytearray('lu\r', 'utf-8'))
			print('lu')

		self.right_stick = -round(self.joy.get_axis(3))
		if self.right_stick > 0.15:
			self.c.write(bytearray('ru\r', 'utf-8'))
			print('ru')
		elif self.right_stick < -0.15:
			self.c.write(bytearray('rd\r', 'utf-8'))
			print('rd')

		back = self.c.readline()[:-2]
		if back:
			print(back)
		
	def main_loop(self):
		'''main loop'''
		while not self.done:
			self.event_loop()
			#self.update()
			pygame.display.flip()
			pygame.time.wait(100)

			

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
		pygame.time.wait(100)
		
	joystick = (pygame.joystick.Joystick(0))
	joystick.init() 
	return joystick
	
def main():
	'''prepare display and start program'''
	os.environ['SLD_VIDEO_CENTERED'] = '1'
	#pygame window setup 
	pygame.init()
	pygame.display.set_caption(CAPTION)
	pygame.display.set_mode(SCREEN_SIZE)
	dir_path = os.path.dirname(os.path.realpath(__file__))
	
	Control().main_loop()
	
	pygame.quit()
	sys.exit()
	

if __name__ == '__main__':
	
	main()
	
