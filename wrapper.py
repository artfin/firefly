from __future__ import print_function

import os
import re

class Wrapper(object):

    def __init__(self, jobname, __full__ = True, __clear__ = True, input_dir = 'INPUTS', output_dir = 'OUTPUTS', punch_dir = 'PUNCHS'):
        
        self.__full__ = __full__
        self.__clear__ = __full__

        self.input_dir = input_dir
        self.output_dir = output_dir
        self.punch_dir = punch_dir

        self.jobname = jobname

        self.input_file_path = os.path.join(self.input_dir, jobname + '.inp')
        self.output_file_path = os.path.join(self.output_dir, jobname + '.out')
        
        self.out_dir_check()
        
        if not __full__:
            cmd = 'firefly -i {0} 2>&1 | tee {1}'.format(self.input_file_path, self.output_file_path)
            print('cmd: {0}'.format(cmd))
        else:
            self.is_output()

            print('Output file path: {0}'.format(self.output_file_path))

            cmd = 'firefly -i {0} -o {1}'.format(self.input_file_path, self.output_file_path)
            print('cmd: {0}'.format(cmd))

        os.system( cmd )
       
        self.read_output()

        self.check_execution()
        self.clear_files()

        print('*' * 30)
        print('PARSING OUTPUT FILE. AVAILABLE:\n [1]: Total energy')
        
        user_input = raw_input()
        if user_input == '1':
            total_energy = self.find_total_energy()
            print('Found total energy: {0}'.format(total_energy))
        
    def find_total_energy(self):
        for line in self.output:
            if 'TOTAL ENERGY' in line:
                energy = line.split()[-1]
                
                if self.is_float(energy):
                    return energy

    @staticmethod
    def is_float(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def is_output(self):
        if os.path.isfile(self.output_file_path):
            print('Output file already exists! Delete [y/n]?')
            user_input = raw_input()

            if user_input == 'y':
                os.remove(self.output_file_path)

            if user_input == 'n':
                filenames = os.listdir(self.output_dir)
                
                matching_files = []

                for filename in filenames:
                    matchObj = re.match(self.jobname + '\d+', filename)
                    
                    if matchObj == None:
                        continue 
                    
                    matching_files.append(matchObj.group())

                #print('matching_files: {0}'.format(matching_files))
               
                numbers = [int(filename.split(self.jobname)[-1]) for filename in matching_files]

                if matching_files:
                    new_filename = self.jobname + "{0:03}.out".format(sorted(numbers, reverse = True)[0] + 1)
                    self.output_file_path = os.path.join(self.output_dir, new_filename) 
                else:
                      self.output_file_path = os.path.join(self.output_dir, self.jobname + '001.out')

    def read_output(self):
        with open(self.output_file_path, mode = 'r') as inputfile:
            self.output = inputfile.readlines()

    def out_dir_check(self):
        if not ( os.path.isdir(self.output_dir) ):
            os.mkdir(self.output_dir_name)
        return

    def check_execution(self):
        if 'NORMALLY' in self.output[-1]:
            print('Execution of firefly terminated NORMALLY')
            return True

        if 'ABNORMALLY' in self.output[-1]:
            print('Execution of firefly terminated ABNORMALLY')
            return False

    def clear_files(self):
        os.remove('DICTNRY')
        os.remove('INPUT')
        
        if not ( os.path.isdir(self.punch_dir) ):
            os.mkdir(self.punch_dir)

        os.rename('PUNCH', os.path.join(self.punch_dir, self.jobname + '.punch'))

wrapper = Wrapper(jobname = 'test')
