from setuptools import setup

with open('README.md', 'r') as arq:
    readme = arq.read()

setup(name='cartesify_backend',
    version='0.0.38',
    license='MIT License',
    author='Diego Guimaraes',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='diego.sena.guimaraes@gmail.com',
    keywords='cartesify',
    description=u'Cartesify Backend',
    packages=['cartesify_backend'],
    install_requires=['requests'],)