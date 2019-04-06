import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


ROOT = os.path.dirname(os.path.abspath(__file__))

requirements = [
    'lxml',
    'oslo.config',
    'oslo.log',
    'oslo.service',
    'paramiko',
    'requests'
]

setup(
    name='ptmanage',
    version='0.0.2',
    author='ayasakinagi',
    author_email='ayasakinagi@littleya.com',
    description='automate manager pt torrent',
    packages=find_packages(),
    package_data={
        '': ['*.cfg'],
    },
    data_files=[('/etc/ptmanage',
                 [os.path.join(ROOT, 'etc/ptmanage/ptmanage.conf')])],
    scripts=['ptmanage/cmd/ptmanage_server.py'],
    entry_points={
        'console_scripts': [
            'ptmanage-server = ptmanage.cmd.ptmanage_server:main'
        ]
    },
    install_requires=requirements
)
