from os import system
from phulpy import task


@task
def test(phulpy):
    phulpy.start(['lint'])


@task
def lint(phulpy):
    result = system('flake8 phoopy')
    if result:
        raise Exception('lint test failed')


@task
def clean(phulpy):
    system('find . -name \'*.pyc\' -delete')


@task
def release(phulpy):
    system('rm -Rf dist && rm -Rf build && python setup.py sdist upload && python setup.py bdist_wheel upload')
