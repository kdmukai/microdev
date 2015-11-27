import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="microdev",
    version="0.0.7",
    author="Keith Mukai",
    author_email="keith.mukai@essaytagger.com",
    description=("A collection of simple reusable Django utility modules."),
    license="BSD",
    keywords="example documentation tutorial",
    url="https://github.com/kdmukai/microdev",
    packages=['microdev', 'microdev.cached', 'microdev.csv', 'microdev.google_client_api', 'microdev.migrations', 'microdev.postal_address', 'microdev.templatetags'],
    package_data={'templates':['*'],},
    # long_description=read('README.md'),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
