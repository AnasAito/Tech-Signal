from setuptools import setup, find_packages


DISTNAME = 'tech_signal'

DOWNLOAD_URL = 'https://github.com/AnasAito/Tech-Signal.git'
URL = 'https://github.com/AnasAito/Tech-Signal'
VERSION = '0.0'

setup(
    name=DISTNAME,
    version=VERSION,
    url=URL,
    download_url=DOWNLOAD_URL,
    install_requires=[
        # required dependencies for extractnet
        'lxml', 'Cython>=0.21.1',
        'extractnet',
        'feedparser', 'skillner'],
    packages=find_packages(),
)
