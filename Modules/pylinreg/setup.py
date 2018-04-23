import re
from setuptools import setup

with open('pylinreg/__init__.py') as f:
    version = re.findall("^__version__ = '(.*)'", f.read())[0]

setup(name='pylinreg',
        version=version,
        description='python makefile system',
        url='http://github.com/chuck1/pylinreg',
        author='Charles Rymal',
        author_email='charlesrymal@gmail.com',
        license='MIT',
        packages=[
            'pylinreg',
            ],
        zip_safe=False,
        )

