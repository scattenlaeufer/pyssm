import time, string, os

class Log_Handler:

	def __init__(self):

		try:
			with open('log', mode='r') as log_file:
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

		with open('log', mode='w') as log_file:
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


class Trail_Logger:

	def __init__(self,top):
		self.log = top

	def __str__(self):
		return self.log

	def add(self,line):
		self.log += '\n'
		for i in line:
			self.log += i + '\t'
	
	def save(self,title):

		if not os.path.isdir('trail_log'):
			os.mkdir('trail_log')
		
		title = 'trail_log/' + title
		if os.path.isfile(title):
			i = 2
			while True:
				if not os.path.isfile(title+'_'+str(i)):
					break
				i += 1
			title = title + '_' + str(i)

		with open(title, mode='w') as log_file:
			log_file.write(self.log)

