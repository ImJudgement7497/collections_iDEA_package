from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = ''
LONG_DESCRIPTION = 'Python package to help analyse collections of states in iDEA'

# Setting up
setup(
        name="collections_iDEA", 
        version=VERSION,
        author="Benjamin Mason",
        author_email="benwalshe.mason@outlook.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['iDEA-latest'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python'],
        classifiers= [
        ]
)