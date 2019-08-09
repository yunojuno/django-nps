import os

from setuptools import find_packages, setup

README = open(os.path.join(os.path.dirname(__file__), "README.rst")).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="django-nps",
    version="0.6",
    packages=find_packages(),
    install_requires=["Django>=1.11"],
    include_package_data=True,
    description="Django app supporting Net Promoter Score (NPS) surveys.",
    license="MIT",
    long_description=README,
    url="https://github.com/yunojuno/django-nps",
    author="Hugo Rodger-Brown",
    author_email="hugo@yunojuno.com",
    maintainer="Hugo Rodger-Brown",
    maintainer_email="hugo@yunojuno.com",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
