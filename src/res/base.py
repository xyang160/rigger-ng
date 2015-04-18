
#coding=utf-8

import  interface
import  utls.rg_sh
import  utls.rg_var
import  os

class res_utls:
    def execmd(self,cmd) :
        utls.rg_sh.shexec.execmd(cmd,tag=self.__class__.__name__)

    @staticmethod
    def value(v) :
        nv =   utls.rg_var.value_of(v)
        return nv

    @staticmethod
    def ensure_path(dst) :
        dst       = res_utls.value(dst)
        if not os.path.exists(dst) :
            os.makedirs(dst)


class cmdres(interface.resource,res_utls) :
    config  = None
    start   = None
    stop    = None
    clean   = None
    reload  = None
    def _before(self,context):
        pass

    def runcmd(self,cmd):
        if cmd is None :
            return
        cmd = res_utls.value(cmd)
        self.execmd(cmd)

    def _config(self,context):
        self.runcmd(self.config)

    def _start(self,context):
        self.runcmd(self.start)

    def _stop(self,context):
        self.runcmd(self.stop)

    def _reload(self,context):
        self.runcmd(self.reload)

    def _clean(self,context):
        self.runcmd(self.clean)


class service_ctrol(cmdres) :
    def __init__(self,svcname):
        self.start  = "/usr/sbin/service %s start" %(svcname)
        self.stop   = "/usr/sbin/service %s stop " %(svcname)
        self.reload = "/usr/sbin/service %s reload" %(svcname)
