#coding=utf8
import  logging
import  interface
from    tc_tools   import *
# from    impl.rg_cmd import *
from    impl.rg_args import *
import  impl.rg_run , impl.rg_var



_logger = logging.getLogger()



class cmd_tc(rigger_tc):
    def asst_cmd(self,conf,cmd):
        impl.rg_run.run_cmd(cmd,conf)
    def test_insobj(self) :
        self.asst_cmd(None,"help")
        self.asst_cmd(None,"help res")
        self.asst_cmd(None,"help res echo ")

    def test_conf(self):
        conf   = impl.rg_var.value_of("${HOME}/devspace/rigger-ng/test/data/res_2.yaml")
        self.asst_cmd(conf,"conf -s test1 -e env1 ")
        self.asst_cmd(conf,"conf -s test2 -e env1 ")
        self.asst_cmd(conf,"conf -s test1,test2 -e env1 ")

