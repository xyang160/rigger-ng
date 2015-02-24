import types , re , os , string ,  getopt , pickle ,yaml , logging , new , sys
import tpl_action,tpl_var
_logger = logging.getLogger()
class tplstatus:
    NONE     = 0
    BLOCK_IN = 1

class tplworker:
    def proc_files(self,arg,dirname,names):
        src_path    = dirname
        relat_path  = src_path.replace(self.src,'').lstrip('/')
        dst_path    = os.path.join(self.dst   , relat_path)
        dst_path    = self.ng.proc_path(dst_path)
        if dst_path is None :
            return
        _logger.debug("proc file : curpath[ %s ] + %s   " %(self.dst,relat_path))
        _logger.info("proc file : src[ %s ]   -> dst [%s]" %(src_path,dst_path))
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)
        for n in names:
            src = os.path.join(src_path ,n)
            dst = self.ng.value(os.path.join(dst_path ,n))
            if n != "_tpl.yaml"  and not os.path.isdir(src):
                _logger.info( "proc tpl file: %s -> %s" %(src,dst) )
                self.ng.file( src  , dst )
    def proc_single_file(self, src, dst):
        _logger.info( "proc single tpl file: %s -> %s" %(src,dst) )
        if dst and os.path.isdir(dst):
            dst = sys.stdout
        elif dst and os.path.isfile(dst):
            _logger.info( "overwriten exsits file: %s" %(dst) )
        self.ng.file( src  , dst )
    def execute(self,src,dst):
        self.src = src
        self.dst = dst
        _logger.debug("src: %s dst: %s" %(src,dst))
        if not os.path.exists(src):
            raise inf.rigger_exception("tpl src not found : %s" %src)
        self.ng = tplngin( src + "/_tpl.yaml")
        #process single file
        if os.path.isfile(src):
            self.proc_single_file(self.src, self.dst)
        else:
        #process dir
            scope= tpl_var.scope_nofound(self.ng.input_var)
            with scope:
                os.path.walk(self.src,self.proc_files,None)

def cond_bool(val):
        if isinstance(val,str):
            return val.upper() == 'TRUE'
        return bool(val)


class engine:
    def __init__(self,tplconf=None):
        self.var_funs = {}
        if tplconf and os.path.exists(tplconf) :
            self.var_funs = dev.yaml_ext(tplconf).load_data('!T','tpl.tpl_action')

        self. input_var = tpl_var.layzer_var(self.var_funs,tpl_action.input())

        tpl_conf = tpl_action.conf()
        if self.var_funs.has_key('_conf'):
            tpl_conf = self.var_funs['_conf']
        self.re_block_beg       = re.compile("^%s (.+):(.*) *{ *$" % tpl_conf.line_tag)
        self.re_block_end       = re.compile("^%s *} *$" % tpl_conf.line_tag)
        self.re_code            = re.compile("^%s(.+)" %tpl_conf.line_tag )
        self.re_var             = re.compile('%s\{(\w+)\}' %tpl_conf.var_tag)
        self.re_path            = re.compile("%s" % tpl_conf.line_tag)
        self.re_path_match      = re.compile("^%s([^/]*):([^/]*)$" % tpl_conf.line_tag)
        self.re_path_val        = re.compile("^%s([^/]*)$" % tpl_conf.line_tag)

    def envval_of_match(self,match):
        var= str(match.group(1))
        val = getattr(tpl_var.var.dict(),var.lower())
        _logger.debug( "key[%s] val[%s]" %(var,val))
        return val

    def value(self,exp):
        try:
            new = self.re_var.sub(self.envval_of_match,exp)
            return new
        except:
            print("tpl:" + exp) ;
            raise

    def proc_path(self,path):
        # %T.need_admin:
        # %T.mvc_mode:action
        path_match = self.re_path.search(path)
        if path_match:
            dst = ""
            if path[0] == '/' :
                dst = "/"
            sections =  path.split("/")
            dst_sections = []
            for sec in sections :
                sec_match = self.re_path_match.match(sec)
                if sec_match :
                    cond_var     = sec_match.group(1).strip()
                    cond_val     = sec_match.group(2).strip()
                    if  len(cond_val) == 0 :
                        cond_val = "TRUE"
                    code         = cond_var.replace("T.","tpl_var.var.dict().")
                    exec "val = " + code
                    if str(val).upper() != cond_val.upper() :
                        return None
                    continue
                sec_match  = self.re_path_val.match(sec)
                if sec_match :
                    cond_var    = sec_match.group(1).strip()
                    code        = cond_var.replace("T.","tpl_var.var.dict().")
                    exec "val = " + code
                    dst_sections.append(val)
                    continue
                dst_sections.append(sec)
            for sec in dst_sections :
                dst = os.path.join(dst,sec)
            return dst
        return path



    def file(self,tplfile,dstfile):
        tpl=open(tplfile, 'r')
        isstdout = dstfile == sys.stdout
        dst = dstfile if isstdout else open(dstfile, 'w')
        st = tplstatus.NONE
        block   = []
        cond    = ""
        expect  = None
        for line in tpl:
            if st == tplstatus.BLOCK_IN:
                if self.re_block_end.match(line) :
                    st=tplstatus.NONE
                    code = "cond_val = %s"  %cond
                    code = code.replace("T.","tpl_var.var.dict().")
                    exec  code
                    _logger.debug(" code in block '%s'[%s]" %(cond,str(cond_val)) )
                    if str(cond_val).upper() == expect.upper() :
                        xblock = []
                        for line in block :
                            _logger.debug("proc line: %s" %(line) )
                            xblock.append(self.value(line))
                        dst.writelines(xblock)
                    block = []
                else:
                    block.append(line)
                continue
            if st == tplstatus.NONE:
                code_match  = self.re_code.match(line)
                block_match = self.re_block_beg.match(line)
                if  block_match:
                    st=tplstatus.BLOCK_IN
                    cond    = block_match.group(1).strip()
                    expect  = block_match.group(2).strip()
                    if len(expect) == 0 :
                        expect = "TRUE"
                    pass
                elif code_match :
                    code = code_match.group(1).strip()
                    code = code.replace("T.","tpl_var.var.dict().")
                    _logger.info(code)
                    exec code
                else:
                    line = self.value(line)
                    dst.write(line)
        tpl.close()
        dst.close()
        if not isstdout:
            stat =  os.stat(tplfile)
            os.chmod(dstfile,stat.st_mode)
