from setuptools import setup
from setuptools import find_packages

setup(
    name="pysda",

    version="0.1.0",

    author="WenLab: Tzai-Hung Wen (Director), Wei-Chin Benny Chen, Fei-Ying Felix Kuo",
    author_email="wenthung@gmail.com",

    packages=['pysda'],

    include_package_data=True,

    url="https://bitbucket.org/wcchin/pysda",

    license="LICENSE.txt",
    description="A suite for diffusion analysis algorithms.",

    long_description=open("README.md").read(),

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: GIS',

         'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.5',
    ],

    keywords='diffusion model',

    install_requires=[
        "numpy",
        "scipy",
        "pandas",
        "geopandas",
        "shapely",
        "descartes",
        "matplotlib",
        "seaborn",
        "datetime",
        "dateutil",
        "imageio",
        "tapitas",
        "mstdbscan"
    ],
)
