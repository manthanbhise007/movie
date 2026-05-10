from setuptools import find_packages,setup
from typing import List

E_DOT="-e ."

def get_requirements(txt_name:str)->List[str]:
    requirements=[]
    with open(txt_name)as f:
        requirements=f.readlines()
        requirements=[req.replace("\n","")for req in requirements]
        if E_DOT in requirements:
            requirements.remove(E_DOT)
    return requirements

setup(
    version="0.0.1",
    name="Movie Recomend",
    author="Manthan",
    author_email="bhisemanthan985@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)
