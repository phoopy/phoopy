from os import system, unlink
from os.path import dirname, join
import xml.etree.ElementTree as ET
from phulpy import task


@task
def test(phulpy):
    phulpy.start(['lint', 'unit_test', 'functional_test'])


@task
def lint(phulpy):
    result = system('flake8 phoopy')
    if result:
        raise Exception('lint test failed')


@task
def unit_test(phulpy):
    result = system(
        'pytest --cov-report term-missing'
        + ' --cov-report xml --cov=phoopy test'
    )
    if result:
        raise Exception('Unit tests failed')
    coverage_path = join(dirname(__file__), 'coverage.xml')
    xml = ET.parse(coverage_path).getroot()
    unlink(coverage_path)
    if float(xml.get('line-rate')) < 1:
        raise Exception('Unit test is not fully covered')


@task
def clean(phulpy):
    system('find . -name \'*.pyc\' -delete')


@task
def release(phulpy):
    system('rm -Rf dist && rm -Rf build && python setup.py sdist upload && python setup.py bdist_wheel upload')
