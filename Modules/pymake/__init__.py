
import os
import traceback

import pymake.os0

def bin_compare(b0,b1):
    for c0,c1 in zip(b,b1):
        try:
            s0 = chr(c0)
            s1 = chr(c1)
        except Exception as e:
            print(e)
            s0 = ''
            s1 = ''
        
        msg = '' if c0==c1 else 'differ'
        
        print("{:02x} {:02x} {:6} {:6} {}".format(c0,c1,repr(s0),repr(s1),msg))

def check_existing_binary_data(filename, b0):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            b1 = f.read()
        
        if b0 == b1:
            return False
        else:
            #bin_compare(b0,b1)
            return True
    else:
        return True

class BuildError(Exception):
    def __init__(self, message):
        super(BuildError, self).__init__(message)


class MakeCall(object):
    def __init__(self, makefile, test=False, force=False):
        self.makefile = makefile
        self.test = test
        self.force = force
    
    def make(self,t):
        self.makefile.make(t, self.test, self.force)

"""
manages the building of targets
"""
class Makefile(object):
    def __init__(self):
        self.rules = []
    def find_rule(self, target):
        for rule in self.rules:
            f_out = list(rule.f_out())
            if target in f_out:
                return rule
        return None

    def make(self, t, test=False, force=False):

        if isinstance(t, list):
            for t1 in t: self.make(t1, test, force)
            return
        
        if t is None:
            raise Exception('target is None'+str(t))

        if isinstance(t, Rule):
            t.make(MakeCall(self, test, force))
            return

        rule = self.find_rule(t)
        if rule is None:
            if os.path.exists(t):
                pass
            else:
                #for r in self.rules:
                #    print(r,list(r.f_out()))
                raise Exception("no rules to make {}".format(t))
        else:
            rule.make(MakeCall(self, test, force))


"""
a rule
f_out and f_in are generator functions that return a list of files
func is a function that builds the output

a rule does not have to build an actual file as output
"""
class Rule(object):

    def __init__(self, f_out, f_in, func):
        self.func_f_out = f_out
        self.func_f_in = f_in
        self.func = func

        self.up_to_date = False
    
    def rule_f_out(self):
        for f in self.func_f_out():
            if not isinstance(f,str):
                raise TypeError('f_out generator must return str')
            yield f

    def check(self, makecall, f_out, f_in):

        if None in f_in:
            return True, "None in f_in {}".format(self)
            raise Exception("None in f_in {}".format(self))
        
        for f in f_in:
            makecall.make(f)

        if makecall.force: return True, None
        
        for f in f_out:
            if not os.path.exists(f): return True, "{} does not exist".format(f)
        
        mtime = [os.path.getmtime(f) for f in f_out]
        
        for f in f_in:
            if isinstance(f, Rule):
                #return True, "Rule object in f_in {}".format(f)
                continue

            for t in mtime:
                if os.path.exists(f):
                    if os.path.getmtime(f) > t:
                        return True, f

        return False, None

    def make(self, makecall):

        if self.up_to_date: return
        
        try:
            f_in = list(self.f_in(makecall))
        except Exception as e:
            print(self)
            traceback.print_exc()
            raise e

        f_out = list(self.rule_f_out())
        
        should_build, f = self.check(makecall, f_out, f_in)

        if should_build:
            if makecall.test:
                print('build',f_out,'because',f)
            else:
                ret = self.func(f_out, f_in)
                if ret is None:
                    pass
                elif ret != 0:
                    raise BuildError(str(self) + ' return code ' + str(ret))

        self.up_to_date = True
    
    def write_text(self, filename, s):
        # it appears that this functionality is actually not useful as currently
        # implemented. revisit later

        #if check_existing_binary_data(filename, s.encode()):
        if True:
            pymake.os0.makedirs(os.path.dirname(filename))
            with open(filename, 'w') as f:
                f.write(s)
        else:
            print('binary data unchanged. do not write.')

    def write_binary(self, filename, b):
        # it appears that this functionality is actually not useful as currently
        # implemented. revisit later

        #if check_existing_binary_data(filename, b):
        if True:
            pymake.os0.makedirs(os.path.dirname(filename))
            with open(filename, 'wb') as f:
                f.write(b)
        else:
            print('binary data unchanged. do not write.')

"""
a rule to which we can pass a static list of files for f_out and f_in
"""
class RuleStatic(Rule):
    def __init__(self, static_f_out, static_f_in, func):
        super(RuleStatic, self).__init__(
                lambda: static_f_out,
                lambda makefile: static_f_in,
                func)



