from setuptools import find_packages , setup
from typing import List

edot = '-e .'
def get_requirements(file_path:str)->List[str]:
    """ Function will return requirements list"""
    requirements =[]
    with open(file_path) as file_obj:
        requiremnet = file_obj.readlines()
        requirements = [req.replace('\n','') for req in requiremnet]

        requirements = [req for req in requirements if req != edot]
    return requirements

setup(
    name = 'mlproject',
    version = '0.0.1',
    author = 'Gaurav',
    author_email='gauravsolanki421@gmail.com',
    packages= find_packages(),
    install_requires = get_requirements('requirements.txt')

)
