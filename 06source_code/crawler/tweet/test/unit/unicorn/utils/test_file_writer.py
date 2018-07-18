#!/usr/bin/env python

'''
@author: Administrator
'''
import unittest
import os
import glob
from file_writer import FileWriter


class Test(unittest.TestCase):


    def testFileWriter(self):
        file_writer = FileWriter(2, "twitter-content", ".")
        
        file_writer.write_stat = False
        
        file_writer.append_line("hello")
        file_writer.append_line("world")
        file_writer.append_line("this is a real world")
        file_writer.close()
        
        file_list = glob.glob("*.bcp")
        self.assertEqual(2, len(file_list))
        for bcp_file in file_list:
            os.remove(bcp_file)
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()