import os

with open('requirements.txt') as file_requirements:
    install_requires = file_requirements.read().split('\n')

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_long_description():
    path = os.path.join(os.path.dirname(__file__), 'README.md')

    try:
        import pypandoc
        return pypandoc.convert(path, 'rst')
    except(IOError, ImportError, RuntimeError):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()


setup(
    name='gse',
    version='0.0.1',
    license='LGPL-3.0',
    description='Graph semantic engine',
    packages=[
        'gse',
    ],
    long_description=get_long_description(),
    author='smer44',
    author_email='',
    maintainer='smer44',
    maintainer_email='',
    url='https://github.com/smer44/graph-semantical-engine/',
    download_url='https://github.com/smer44/graph-semantical-engine/archive/master.zip',

    install_requires=install_requires,

    entry_points={
        'gui_scripts': [
            'gse = gse.gui:run',
        ],
        'console_scripts': [
            'gse-wd-label = gse.tut_wikidata.tut_wikidata_get_label:cli',
            'gse-wd-soap = gse.tut_wikidata.tut_wikidata_soap:cli',
            'gse-wd-sparkql = gse.tut_wikidata.tut_wikidata_sparkql_superclasses:cli',
        ]
    },

    include_package_data=True,
    classifiers=[  # source: https://pypi.org/classifiers/
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering',
    ]
)
