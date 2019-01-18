#:::LED MASTER:::

import os
import sys
import json
import time
import datetime
import colorful
from raspledstrip.bootstrap import *

#:::INITIALIZATION:::

colorful.use_style('monokai')

#:::DEFINITIONS:::

#: Print Log w/ timestamp

def printLog(text):

	print(colorful.bold(datetime.datetime.now().strftime("%m/%d/%Y-%H:%M")) + ' ' + text)

#: Print error message

def printError(text):

	printLog(colorful.bold_magenta('ERROR: ') + text)
	return True

#: Print success message

def printSuccess(text):

	printLog(colorful.bold_seaGreen('SUCCESS: ') + text)

#: Print exit message and exit

def printExit(text):

	printLog(colorful.bold_magenta('ERROR: ') + text + ' Will exit...')
	sys.exit()

#: Check for Int

def intCheck(val):
	try:
		return float(val).is_integer()
	except:
		return False

#: Get JSON from file

def getFileJSON(file):

	with open(file) as f:
		text = ''.join(line.rstrip() for line in f)
	f.close()
	return text

#:::DISPLAY CLASS:::

class Display:

	#: Init

	def __init__(self, args=sys.argv):

		printLog(colorful.bold_purple('PI LED LAUNCHED...'))
		self.getArguments(args)
		self.getConfig()

	#: Get Arguments
		
	def getArguments(self, init_args):

		try:

			args = {'file': ['-f', '--file'],
					'duration': ['-d', '--duration'],
					'loops': ['-l', '--loops'],
					'args': ['-a', '--args']}

			print_args = []

			for i in range(0, len(init_args)):
				for key in args:
					if init_args[i] in args[key]:
						if (i + 1) < len(init_args):
							if key != 'args':
								setattr(self, key, init_args[i + 1])
								print_args.append(str(colorful.bold_orange(key.capitalize())) + ': ' + init_args[i + 1])
								break
							elif key == 'args':
								args_temp = []
								for x in range(i + 1, len(init_args)):
									if '-' not in init_args[x]:
										args_temp.append(init_args[x])
									else:
										break
								if len(args_temp) > 0:
									setattr(self, key, args_temp)
									print_args.append(str(colorful.bold_orange(key.capitalize())) + ': ' + str(args_temp))

			req_exit = False

			if 'file' not in self.__dict__:
				req_exit = printError('Missing file argument.')
			if 'file' in self.__dict__ and not os.path.isfile(str(self.__dict__['file'])):
				req_exit = printError('File not valid.')
			if 'duration' in self.__dict__ and not intCheck(self.__dict__['duration']):
				req_exit = printError('Invalid duration.')
			if 'loops' in self.__dict__ and not intCheck(self.__dict__['loops']):
				req_exit = printError('Invalid number of loops.')

			if req_exit == True:
				printExit('Invalid arguments.')
			else:
				printLog(colorful.bold_seaGreen('ARGUMENTS: ') + ', '.join(print_args))

		except Exception as e:
			if str(e)[-1] != '.':
				e_str = str(e) + '.'
			else:
				e_str = str(e)
			printExit('Invalid arguments: ' + e_str)

	#: Get Config

	def getConfig(self):

		text = getFileJSON(self.file)
		self.config = json.loads(text)
		printLog(colorful.bold_orange('CONFIG: ') + str(self.config))
		printSuccess('Unloaded JSON config file.')

	#: Do actions

	def doActions(self):

		for i in range(0, len(self.config)):

			if len(self.config) == 1 and 'duration' in self.__dict__:
				self.config[i]['duration'] = int(self.duration)

			if len(self.config) == 1 and 'loops' in self.__dict__:
				self.config[i]['loops'] = int(self.loops)

			if self.config[i]['action'] == 'off':
				printLog(colorful.bold_purple("Turning Pi LED's off..."))
				loop_itt = -1
				rem, loop_bool = self.loopLogic(loop_itt, self.config[i]['loops'])
				while loop_bool == True:
					led.all_off()
					if self.config[i]['duration'] != 0:
						printLog('Sleeping for ' + colorful.bold_blue(str(self.config[i]['duration'])) + ' seconds.')
						time.sleep(self.config[i]['duration'])
					if loop_itt == -1:
						loop_itt += 2
					elif self.config[i]['loops'] > -1:
						loop_itt += 1
					rem, loop_bool = self.loopLogic(loop_itt, self.config[i]['loops'])
					printLog(colorful.bold_blue(rem) + ' loops remaining.')

			elif self.config[i]['action'] == 'color':
				loop_itt = -1
				rem, loop_bool = self.loopLogic(loop_itt, self.config[i]['loops'])
				while loop_bool == True:
					if 'args' in self.__dict__ and 'color' in self.args:
						self.config[i]['args']['color'] = self.args[i]
					led.fill(color_hex(self.config[i]['args']['color']))
					led.update()
					if self.config[i]['duration'] != 0:
						printLog('Sleeping for ' + colorful.bold_blue(str(self.config[i]['duration'])) + ' seconds.')
						time.sleep(self.config[i]['duration'])
					if loop_itt == -1:
						loop_itt += 2
					elif self.config[i]['loops'] > -1:
						loop_itt += 1
					rem, loop_bool = self.loopLogic(loop_itt, self.config[i]['loops'])
					printLog(colorful.bold_blue(rem) + ' loops remaining.')

			elif self.config[i]['action'] == 'rainbow':
				loop_itt = -1
				anim = Rainbow(led)
				rem, loop_bool = self.loopLogic(loop_itt, self.config[i]['loops'])
				while loop_bool == True:
					anim.step()
					led.update()
					if self.config[i]['duration'] != 0:
						printLog('Sleeping for ' + colorful.bold_blue(str(self.config[i]['duration'])) + ' seconds.')
						time.sleep(self.config[i]['duration'])
					if loop_itt == -1:
						loop_itt += 2
					elif self.config[i]['loops'] > -1:
						loop_itt += 1
					rem, loop_bool = self.loopLogic(loop_itt, self.config[i]['loops'])
					printLog(colorful.bold_blue(rem) + ' loops remaining.')

		if self.config[-1]['action'] != 'off':
			led.all_off() 

		printSuccess('Actions completed.')	

	#: Loop Logic		

	def loopLogic(self, itt, val):

		if val == -1:
			return 'Infinite', True
		elif val != -1 and itt < val:
			return str(max(val - itt, 0)), True
		elif val != -1 and itt >= val:
			return '0', False
		
#:::DRIVER:::

main = Display()
main.doActions()

#:::END PROGRAM:::