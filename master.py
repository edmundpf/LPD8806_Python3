#:::LED MASTER:::

import os
import sys
import json
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

#:::DRIVER:::

main = Display()

#:::END PROGRAM:::