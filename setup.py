"""Setup for Markdown XBlock."""

import os

from setuptools import setup


def package_data(pkg, roots):
    """Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.

    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='markdown-xblock',
    use_scm_version=True,
    description='Markdown XBlock provides editing course content in Markdown.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/cleura/markdown-xblock',
    license='AGPL-3.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Topic :: Education :: Computer Aided Instruction (CAI)',
        'Topic :: Education',
    ],
    packages=[
        'markdown_xblock',
    ],
    python_requires='>=3.11',
    install_requires=[
        'XBlock<5',
        'markdown2>=2.3.9',
        'Pygments>=2.0.1',
    ],
    setup_requires=[
        'setuptools-scm',
    ],
    entry_points={
        'xblock.v1': [
            'markdown = markdown_xblock:MarkdownXBlock'
        ]
    },
    package_data=package_data("markdown_xblock", ["static", "public"]),
)
