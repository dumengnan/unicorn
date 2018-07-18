#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2018

@author: Administrator
'''
import os
import uni_util
import get_config

class FileWriter(object):
    '''
    '''

    def __init__(self, fix_line_number, module_name, output_dir):
        '''
        Constructor
        '''
        self.fix_line_number = fix_line_number
        self.module_name = module_name
        self.output_dir = output_dir
        
        self.tmp_file = uni_util.get_file_name(self.module_name)
        self.f_output = open(self.tmp_file, 'w')
        self.lines_num = 0
        
        self.write_stat = True
                  
    def append_line(self, line_str):

        if self.lines_num >= self.fix_line_number:
            self.f_output.close()
            os.rename(self.tmp_file, os.path.join(self.output_dir, uni_util.get_file_name(self.module_name)))
            if self.write_stat:
                self.write_to_stat()
            self.tmp_file = uni_util.get_file_name(self.module_name)
            self.f_output = open(self.tmp_file, 'w')
            self.lines_num = 0
            
        self.f_output.write(line_str)
        self.f_output.write("\n")
        self.lines_num = self.lines_num + 1
               
    def close(self):
        self.f_output.close()
        self.lines_num = 0
        
        
    def write_to_stat(self):
        stat_dir = get_config.get_config()["stat_dir"]
        if not os.path.exists(stat_dir):
            os.mkdir(stat_dir)
            
        stat_file = os.path.join(stat_dir, uni_util.get_file_name("stat_flow"))
        with open(stat_file, "w") as f_stat:
            f_stat.write(uni_util.get_current_time() + "\t" + self.module_name + "\t" + str(self.fix_line_number))
        
        