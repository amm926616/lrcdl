from setuptools import setup, find_packages

setup(
    name='lrcdl',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'click',
        'mutagen',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'lrcdl=lrcdl.cli:lrcdl',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
