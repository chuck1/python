
import os

class Makefile(object):
    def __init__(self):
        self.rules = {}
    def make(self, filename):
        try:
            rule = self.rules[filename]
        except:
            if os.path.exists(filename):
                pass
            else:
                raise Exception("no rules to make {}".format(filename))
        else:
            rule.make(self)

class Rule(object):

    def __init__(self, f_out, f_in, func):
        self.f_out = f_out
        self.f_in = f_in
        self.func = func

    def check(self, master, f_out, f_in):

        for f in f_in:
            master.make(f)
        
        if not os.path.exists(f_out): return True

        mtime = os.path.getmtime(f_out)
        
        for f in f_in:
            if os.path.getmtime(f) > mtime:
                return True

        return False

    def make(self, master):
        f_in = list(self.f_in())
        f_out = list(self.f_out())

        if self.check(master, f_out, f_in):
            self.func(f_out, f_in)

class RuleStatic(Rule):
    def __init__(self, static_f_out, static_f_in, func):
        super(RuleStatic, self).__init__(
                lambda: static_f_out,
                lambda: static_f_in,
                func)



