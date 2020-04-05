import glob, os
from distutils.core import setup
from Cython.Build import cythonize
from sh import rm, mv, find, cp



def build(path):
    pwd = os.getcwd()
    os.chdir(path)
    for f in glob.glob("*.py"):
        name = os.path.basename(f)[0:-3]
        if name not in ["__init__" , "setup"]:
            setup(name=name, ext_modules=cythonize(f))
            rm(f)
            if os.path.exists("%s.c" % name):
                rm("%s.c" % name)
            if os.path.exists("%s.pyc" % name):
                rm("%s.pyc" % name)
    os.chdir(pwd)

def main():
    build(os.sep.join([os.getcwd(), "controller"]))
    build(os.sep.join([os.getcwd(), "reportbro"]))
    build(os.sep.join([os.getcwd(), "view"]))

if __name__ == '__main__':
    main()

    