# pySDA

a python Suite for Diffusion Analysis (for python 3.5 and above)

## Intro

This package currently included the two diffusion analysis algorithms:

1. TaPiTaS: A geo-computational algorithm for exploring the structure of diffusion progression in time and space. Scientific Reports.
   https://www.nature.com/articles/s41598-017-12852-z
2. MST-DBSCAN: Characterizing Diffusion Dynamics of Disease Clustering: A Modified Space–Time DBSCAN (MST-DBSCAN) Algorithm. Annals of the American Association of Geographers.
   https://www.tandfonline.com/doi/full/10.1080/24694452.2017.1407630

## Install

You can choose one of the following to install pySDA to your python environment.

### 1. download then pip install

1. download the package by clicking the green button (Clone or download), choose Download ZIP.

2. extract the zip file to your working directory

3. in cmd (where you can use pip install to the intended python environment):

   ```sh
   cd C://the/extract/directory/pysda-master
   pip install .
   ```

This should install the package to your python.

### 2.  git clone and pip install

in cmd:

```sh
cd C://a/place/you/like/
git clone https://github.com/wenlab501/pysda.git
cd pysda
pip install .
```

This is actually the exact same thing as the first option.

### 3. pip install from github

in cmd:

```
pip install git+https://github.com/wenlab501/pysda.git
```

This is also the same as above.

### 4. pip install from pypi

 in cmd:

```
pip install pysda
```

This will download the pysda from pypi.



## Dependency

- numpy, scipy: for calculations, including spatial indexing and querying
- pandas, geopandas: for data manipulation and result preparation
- shapely: deal with the geometry
- descartes, matplotlib, seaborn: for making maps
- python-dateutil: deal with the date conversion
- imageio: animated figure exporting
- tapitas: the core algorithm for TaPiTas
- mstdbscan: the core algorithm for MST-DBSCAN

## Tutorials
- The tutorial for using TaPiTaS in pySDA:
https://github.com/wenlab501/pysda/blob/master/pysda-taipitas-tutorial.ipynb
- The tutorial for using MST-DBSCAN in pySDA:
https://github.com/wenlab501/pysda/blob/master/pysda-mstdbscan%20tutorial.ipynb

## License

Copyright (c) 2018 wenlab501, Tzai-Hung Wen, Department of Geography, National Taiwan University

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
