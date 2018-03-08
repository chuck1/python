
from setuptools import setup

setup(name='testpackage',
        version='0.1',
        #description='python spreadsheets',
        #url='http://github.com/chuck1/sheets',
        #author='Charles Rymal',
        #author_email='charlesrymal@gmail.com',
        #license='MIT',
        packages=['foo','bar'],
        package_dir={'foo':'a/foo', 'bar':'b/bar'},
        zip_safe=False,
        )

