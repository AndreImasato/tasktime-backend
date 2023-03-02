import os

from setuptools import setup, find_packages

with open(os.path.join(
    os.path.dirname(__file__),
    'README.md'
)) as readme:
    README = readme.read()

# Allows setup to be run from any path
os.chdir(
    os.path.normpath(
        os.path.join(
            os.path.abspath(__file__),
            os.pardir
        )
    )
)

setup(
    name="TaskTime Backend",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    license="BSD License",
    description="TaskTime Backend",
    long_description=README,
    author="André Imasato",
    author_email="andresimasato@gmail.com",
    install_requires=[],
    url="https://github.com/AndreImasato/backend-django-qa"
)
