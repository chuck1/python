import subprocess
import myos
import os
import argparse



class Project(object):
    def __init__(self, source_dir):
        self.source_dir = os.path.abspath(os.path.split(source_dir)[0])
        self.binary_dir = os.getcwd() #os.path.abspath(".")

        self.compiler = "g++"
        self.compiler_flags = "-std=c++0x"

        #print(self.source_dir)
        #print(self.binary_dir)

    def cpp_files(self):

        return myos.glob(".*\.cpp$", self.source_dir)

    def o_files(self):

        for f in self.cpp_files():
            s = os.path.relpath(f, self.source_dir)
            d = os.path.join(self.binary_dir, 'pymake_files', s)
            d = os.path.splitext(d)[0] + ".o"
            yield d


    def generate(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('command', default='all')
        args = parser.parse_args()
        
        #lines = []
        
        #lines.append( "CPP_FILES = " + " ".join(self.cpp_files()) )
        #lines.append( "O_FILES   = " + " ".join(self.o_files()) )
        
        o = list(self.o_files())

        if args.command == 'all':
            self.all()
        elif args.command == 'clean':
            subprocess.call(["rm","-rf"] + o)
        else:
            print('error')

        #for c,o in zip(self.cpp_files(), self.o_files()):
            #lines.append("{}:{}".format(o,c))
            #lines.append("\t@echo {}".format(os.path.split(o)[0]))
            #lines.append("\t@mkdir -p {}".format(os.path.split(o)[0]))
            #lines.append("\t@{} {} {} -o {}".format(self.compiler,self.compiler_flags,c,o))

            #subprocess.call(["g++", "-c", c, "-o", o])

        #lines.append( "clean:" )
        #lines.append( "\t@rm -f " + " ".join(self.o_files()))
        
    def all(self):
        for c,o in zip(self.cpp_files(), self.o_files()):
            print(o)
            subprocess.call(["g++", "-c", c, "-o", o])


        #return "\n".join(lines)
        

