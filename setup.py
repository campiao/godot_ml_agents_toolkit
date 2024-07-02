# setup.py

from setuptools import setup, find_packages

setup(
    name='godot-mlagents',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'godot-mlagents=godot_ml_agents_toolkit.main:main',
        ],
    },
    author='Pedro Campião',
    author_email='pedro.campiao1@gmail.com',
    description='Toolkit to integrate RL algorithms with Godot games',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/mypackage',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
