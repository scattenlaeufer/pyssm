# -*- coding: utf-8 -*-
import time

class Log_Handler:

    def __init__(self):

        try:
            with open('pyssm.log', mode='r') as log_file:
                self.log = log_file.read()
        except:
            self.log = ''

        if self.log == '':
            self.log += 'time\tstage\tmiss teaching\tmiss test'
    

    def add(self,stage,miss_teaching,miss_test):
        self.log += '\n{}\t{}\t{}\t{}'.format(time.strftime('%d.%m.%Y %H:%M'),stage,miss_teaching,miss_test)

    def __str__(self):
        return self.log

    def get_stage(self):
        return Stage_A
