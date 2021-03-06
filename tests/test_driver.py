#! python3
# -*- encoding: utf-8 -*-
'''
Current module: tests.test_driver

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:     luokefeng@163.com
    RCS:      tests.test_driver,  v1.0 2018年9月30日
    FROM:   2018年9月30日
********************************************************************
======================================================================

Provide a function for the automation test

'''


import unittest
from rtsf.p_executer import TestRunner
from rtsf.p_applog import logger
from winuidriver.driver import Driver

class TestDriver(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.case_file = r'data\test_case.yaml'
        cls.data_driver_case = r'data\data_driver.yaml'
    
    def test_Driver(self):        
        runner = TestRunner(runner = Driver).run(self.case_file)
        html_report = runner.gen_html_report()
        print(html_report)
        self.assertIsInstance(html_report, (list, tuple))
    
    def test_Driver_with_data_driver(self):        
        runner = TestRunner(runner = Driver).run(self.data_driver_case)
        html_report = runner.gen_html_report()
        print(html_report)
        self.assertIsInstance(html_report, (list, tuple))
                
if __name__ == "__main__":
    #logger.setup_logger("debug")
    #unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(TestDriver("test_Driver_with_data_driver"))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
    
    