import time, string, os

class Log_Handler:

	def __init__(self):

		self.path = __file__[:-7]

		try:
			with open(os.path.join(self.path,'log'), mode='r') as log_file:
				self.log = log_file.read()
		except:
			self.log = ''

		if self.log == '':
			self.log += 'time\tstage\tmiss teaching\tmiss test'
	

	def add(self,stage,miss_teaching,miss_test):
		self.log += '\n{}\t{}\t{}\t{}'.format(time.strftime('%d.%m.%Y %H:%M'),stage,miss_teaching,miss_test)

	def __str__(self):
		return self.log

	def save(self):

		with open(os.path.join(self.path,'log'), mode='w') as log_file:
			log_file.write(self.log)


	def analyze(self):

		entrys = string.split(self.log,'\n')
		if len(entrys) == 1:
			return ('0',False)

		last = string.split(entrys[len(entrys)-1],'\t')

		if int(last[2]) == 0:
			teach = False
		else:
			teach = True

		if int(last[3]) == 0:
			test = False
		else:
			test = True

		if not test or not teach:
			return (last[1],True)
		else:
			return (last[1],False)


class Trial_Logger:

	def __init__(self,name):
		self.name = os.path.join(__file__[:-7],'trial_log/',name)
		if os.path.isdir(os.path.join(__file__[:-7],'trial_log')):
			try:
				with open(self.name, mode='r') as log_file:
					self.log = log_file.read()
					self.lines = string.split(self.log,'\n')
					last_line = string.split(self.lines[len(self.lines)-1],'\t')
					try:
						self.cc = int(last_line[0])
					except ValueError:
						self.cc = 0
			except IOError:
				self.lines = []
				self.log = ''
				self.cc = 0
		else:
			self.lines = []
			os.mkdir(os.path.join(__file__[:-7],'trial_log'))
			self.log = ''
			self.cc = 0

	def set_top(self,top):
		self.cc += 1
		top = 'cycle_count\t'+top
		if self.log == '':
			self.log += top
			self.lines.append(top)
		else:
			if self.lines[0] != top:
				self.log += '\n' + top



	def __str__(self):
		return self.log

	def add(self,line):
		self.log += '\n' + str(self.cc) + '\t'
		for i in line:
			self.log += str(i) + '\t'

	def add_str(self,entry):
		self.log += '\n' + entry

	def save(self):
		with open(self.name, mode='w') as log_file:
			log_file.write(self.log)
