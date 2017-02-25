
import os

class BuildError(Exception):
    def __init__(self, message):
        super(BuildError, self).__init__(message)

"""
manages the building of targets
"""
class Makefile(object):
    def __init__(self):
        self.rules = []
    def find_rule(self, target):
        for rule in self.rules:
            f_out = list(rule.f_out())
            #print target, f_out
            if target in f_out:
                return rule
        return None
    def make(self, filename):
        rule = self.find_rule(filename)
        if rule is None:
            if os.path.exists(filename):
                pass
            else:
                raise Exception("no rules to make {}".format(filename))
        else:
            rule.make(self)

"""
a rule
f_out and f_in are generator functions that return a list of files
func is a function that builds the output
"""
class Rule(object):

    def __init__(self, f_out, f_in, func):
        self.f_out = f_out
        self.f_in = f_in
        self.func = func

    def check(self, makefile, f_out, f_in):

        for f in f_in:
            makefile.make(f)
        
        for f in f_out:
            if not os.path.exists(f): return True

        mtime = [os.path.getmtime(f) for f in f_out]
        
        for f in f_in:
            for t in mtime:
                if os.path.getmtime(f) > t:
                    return True

        return False

    def make(self, makefile):
        f_in = list(self.f_in())
        f_out = list(self.f_out())

        if self.check(makefile, f_out, f_in):
            ret = self.func(f_out, f_in)

            if ret != 0:
                raise BuildError(str(self) + ' return code ' + str(ret))

"""
a rule to which we can pass a static list of files for f_out and f_in
"""
class RuleStatic(Rule):
    def __init__(self, static_f_out, static_f_in, func):
        super(RuleStatic, self).__init__(
                lambda: static_f_out,
                lambda: static_f_in,
                func)



