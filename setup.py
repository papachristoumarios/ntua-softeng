from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_reqs = f.read().splitlines()

setup(name='cheapies',
      version='1.0',
      packages=find_packages(),
      scripts=['manage.py'],
      include_package_data=True,
      install_requires=install_reqs,
      author='mycoderocks',
      description='Price observatory developed in django')
