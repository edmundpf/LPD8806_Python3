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

			presets = ['--off', '--color', '--rainbow']

			print_args = []

			if init_args[1] in presets:
				init_args = self.presets(init_args)

			for i in range(1, len(init_args)):
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

		try:

			text = getFileJSON(self.file)
			self.config = json.loads(text)
			printLog(colorful.bold_orange('CONFIG: ') + str(self.config))
			printSuccess('Unloaded JSON config file.')

		except Exception as e:
			if str(e)[-1] != '.':
				e_str = str(e) + '.'
			else:
				e_str = str(e)
			printExit('Could not parse JSON: ' + e_str)			

	#: Do actions

	def doActions(self):

		try:

			for i in range(0, len(self.config)):

				inf_check = False

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
						if inf_check == False:
							printLog(colorful.bold_orange(rem) + ' loops remaining.')
							inf_check = True

				elif self.config[i]['action'] == 'color':
					loop_itt = -1
					rem, loop_bool = self.loopLogic(loop_itt, self.config[i]['loops'])
					while loop_bool == True:
						if 'args' in self.__dict__:
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
						if inf_check == False:
							printLog(colorful.bold_orange(rem) + ' loops remaining.')
							inf_check = True

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
						if inf_check == False:
							printLog(colorful.bold_orange(rem) + ' loops remaining.')
							inf_check = True

			if self.config[-1]['action'] != 'off':
				led.all_off() 

			printSuccess('Actions completed.')

		except KeyboardInterrupt:
			led.all_off()
			print(colorful.bold(' ---------->>> ') + colorful.magenta('Interrupt entered.'))
			printExit('Actions interrupted.')

		except Exception as e:
			if str(e)[-1] != '.':
				e_str = str(e) + '.'
			else:
				e_str = str(e)
			printExit('Invalid config: ' + e_str)	

	#: Loop Logic		

	def loopLogic(self, itt, val):

		if val == -1:
			return 'Infinite', True
		elif val != -1 and itt < val:
			return str(max(val - itt, 0)), True
		elif val != -1 and itt >= val:
			return '0', False

	#: Presets

	def presets(self, init_args):

		if init_args[1] == '--off':
			printSuccess('Loading off preset.')
			return ['master.py', '-f', 'actions/off.json']
		elif init_args[1] == '--color':
			if len(init_args) > 2:
				if init_args[2] in COLORS:
					color_temp = COLORS[init_args[2]]
				else:
					color_temp = init_args[2]
				printSuccess('Loading color preset.')
				return ['master.py', '-f', 'actions/color.json', '-l', '-1', '-a', color_temp]
			else:
				printError('Invalid color preset.')
				printExit('Invalid arguments.')
				sys.exit()
		elif init_args[1] == '--rainbow':
			printSuccess('Loading rainbow preset.')
			return ['master.py', '-f', 'actions/rainbow.json']
			
#:::DRIVER:::

main = Display()
main.doActions()

#:::END PROGRAM:::