#coding=utf-8
import logging
import interface
import utls.rg_io


_logger = logging.getLogger()

def setup() :
    interface.regist_res("env,project,system,xmodule,prj_main" , "res.inner")
    interface.regist_res("mysql"                               , "res.mysql")
    interface.regist_res("echo,vars,assert_eq"                 , "res.inner")

    interface.regist_res("link,path,intertpl,file_tpl"                       , "res.files")

    interface.regist_cmd("check,clean,info"                    , "impl.rg_cmd.rg_cmd_prj")
    interface.regist_cmd("conf,reconf,start,stop,restart,data" , "impl.rg_cmd.rg_cmd_prj")
    interface.regist_cmd("help"                                , "impl.rg_cmd.rg_cmd")

def list_res() :
    import  res
    for name,module in interface.registed_resource.items() :
        code = "obj = res.%s()" %(name)
        _logger.debug("exec code : %s" %code)
        try :
            exec code
            utls.rg_io.export_objdoc(name,obj )
        except  Exception as e :
            raise interface.rigger_exception("@list_res() code error: %s \n %s" %(code,e) )



def ins_res(name) :
    import  res
    for res_name,module in interface.registed_resource.items() :
        if  res_name == name :
            code = "obj = res.%s()" %(name)
            _logger.debug("exec code : %s" %code)
            try :
                exec code
                return obj
            except  Exception as e :
                raise interface.rigger_exception("@ins_res() code error: %s \n %s" %(code,e) )
    return None


def list_cmd() :
    import  impl.rg_cmd
    for name,module in interface.registed_cmd.items() :
        code = "obj = impl.rg_cmd.%s_cmd()" %(name)
        _logger.debug("exec code : %s" %code)
        try :
            exec code
            utls.rg_io.export_objdoc(name,obj )
        except  Exception as e :
            raise interface.rigger_exception("@list_cmd() code error: %s \n %s" %(code,e) )



def ins_cmd(name) :
    import  impl.rg_cmd
    for cmd,module in interface.registed_cmd.items() :
        if  cmd == name :
            code = "obj = impl.rg_cmd.%s_cmd()" %(name)
            _logger.debug("exec code : %s" %code)
            try :
                exec code
                return obj
            except  Exception as e :
                raise interface.rigger_exception("@ins_cmd() code error: %s \n %s" %(code,e) )
    return None