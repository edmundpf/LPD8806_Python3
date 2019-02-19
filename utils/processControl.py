import os
import subprocess

#:::PROCESS CONTROL:::

class Process:

	#: INIT

	def __init__(self, proc_name=None, proc_id=None, proc_args=None, proc_match='OR'):

		self.proc_name = proc_name
		self.proc_id = proc_id
		self.proc_args = proc_args
		self.proc_match = proc_match
		self.proc_lookup = 'ps -ef | grep {}'

	#: Get all running processes

	def getProcesses(self):

		output = subprocess.check_output(self.proc_lookup.format(self.proc_name), shell=True).decode('utf-8')
		output = output.split('\n')
		result = []
		if output[-1] == '':
			del output[-1]
		for i in range(0, len(output)):
			x = 0
			temp_str = ''
			for x in range(0, len(output[i])):
				if output[i][x] != ' ':
					temp_str += output[i][x]
				elif ((x + 1) < len(output[i])) and output[i][x] == ' ' and output[i][x + 1] != ' ':
					temp_str += output[i][x]
				temp_list = temp_str.split(' ')
			if len(temp_list) >= 8:
				temp_dict = {'user_id': temp_list[0],
							'proc_id': temp_list[1],
							'parent_id': temp_list[2],
							'cpu_usage': temp_list[3],
							'start_time': temp_list[4],
							'terminal': temp_list[5],
							'run_time': temp_list[6],
							'cmd': []}
				for x in range(7, len(temp_list)):
					temp_dict['cmd'].append(temp_list[x])
				result.append(temp_dict)
		return result


	#: Kill Processes

	def killProcesses(self):

		proc = self.getProcesses()
		kill_list = []
		for i in range(0, len(proc)):
			if self.proc_match == 'OR':
				if proc[i]['cmd'][0] == self.proc_name and any(x in proc[i]['cmd'] for x in self.proc_args):
					kill_res = os.system('kill -9 {}'.format(proc[i]['proc_id']))
					if kill_res == 0:
						kill_list.append({'proc_id': proc[i]['proc_id'],
											'cmd': ' '.join(proc[i]['cmd'])})
			elif self.proc_match == 'AND':
				if proc[i]['cmd'][0] == self.proc_name and all(x in proc[i]['cmd'] for x in self.proc_args):
					kill_res = os.system('kill -9 {}'.format(proc[i]['proc_id']))
					if kill_res == 0:
						kill_list.append({'proc_id': proc[i]['proc_id'],
											'cmd': ' '.join(proc[i]['cmd'])})
		return kill_list

#:::END PROGRAM:::