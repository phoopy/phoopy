from setuptools import setup
import phoopy

long_description = open('README.rst', 'r').read()

setup(
    name='phoopy',
    version=phoopy.__version__,
    packages=['phoopy'],
    setup_requires=['wheel'],
    install_requires=[],
    description="Full stack framework for python based on bundles",
    long_description=long_description,
    url='https://github.com/phoopy/phoopy',
    author='Phoopy',
    author_email='reisraff@gmail.com',
    license='MIT',
    classifiers=[
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
