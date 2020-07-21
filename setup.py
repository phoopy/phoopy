from setuptools import setup
import phoopy.phoopy

long_description = open('README.rst', 'r').read()

setup(
    name='phoopy',
    version=phoopy.phoopy.__version__,
    packages=['phoopy', 'phoopy.phoopy'],
    setup_requires=['wheel'],
    install_requires=[
        'phoopy-kernel>=1.2.0,<1.3.0',
        'phoopy-console>=1.2.0,<1.3.0',
        'phoopy-yaml>=1.1.2,<1.2.0',
        'phoopy-http>=1.0.5',
    ],
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
