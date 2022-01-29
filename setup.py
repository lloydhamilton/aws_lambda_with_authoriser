from setuptools import setup, find_packages

setup(
    name="lamba_with_authoriser",
    version="0.0.1",
    packages=find_packages(exclude=(['tests*'])),
    description="Lambda functions with authoriser",
    author='Lloyd Hamilton',
    author_email=''
)
