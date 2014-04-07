#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="Stevedore Template Resolver Example",
    version="0.1",
    packages=find_packages(),
    author="Daniel Rocco",
    author_email="drocco@gmail.com",
    entry_points="""
        [console_scripts]
        serve_example = base_app.main:main
        enumerate_extensions = demo:enumerate_template_extensions

        [templates]
        base = base_app.templates
        shared = shared_lib.templates
        client_custom = client_custom.templates
    """
)
