import re
from setuptools import setup

with open('gen_reg/__init__.py') as f:
    version = re.findall("^__version__ = '(.*)'", f.read())[0]

setup(name='gen_reg',
        version=version,
        description='general regression',
        url='',
        author='Charles Rymal',
        author_email='charlesrymal@gmail.com',
        license='MIT',
        packages=[
            'gen_reg',
            ],
        zip_safe=False,
        )

