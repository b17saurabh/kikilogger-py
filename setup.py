from setuptools import setup, find_packages

setup(
    name='kikiLogger',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'elasticsearch',
        'opensearch-py<=2.4.2'
    ],
    entry_points={
        'console_scripts': [
            'kikiLogger = kikiLogger.__main__:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
