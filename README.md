# Two Methods to Remove Blaze Function from Echelle Spectrum Orders: AFS and ALSFS in Python

This repository contains the implementation of the AFS and the ALSFS algorithms in python proposed by Xin Xu, Jessi Cisewski-Kehe, et al, whose paper is available  <a href="https://arxiv.org/pdf/1904.10065.pdf"> here </a>.  </p>

## Motivation:
The AFS and the ALSFS algorithms can be used to flatten the spectrum continuum, an important data analysis step in spectroscopic analysis. The original code was implemented in R. Here, we implemented the AFS and the ALSFS algorithms in Python which will be convenient for astronomers to work with. 

## Prerequisite:
The following python packages are required to run the AFS and the ALSFS algorithms: 
<br><a href="https://pandas.pydata.org/"> Pandas </a> : used for data analysis 
<br><a href="https://www.numpy.org/"> Numpy </a> : used for scientific computing
<br><a href="https://pypi.org/project/alphashape/"> alphashape </a>: used for calculation of the alphashape of a geometric object
<br><a href="https://pypi.org/project/Shapely/"> shapely </a>: used for analysis of geometric objects in the Cartesian plane.
<br><a href="https://rpy2.readthedocs.io/en/version_2.8.x/overview.html"> rpy2 </a>: used for calling R loess function in Python: 
<br><a href="https://www.scipy.org/"> scipy </a>: used for optimaztion problem appeared in the end of the ALSFS algorithm

## Installation:
To use these two algorithms, first change the current working directory to the location where you want the cloned directory to be made on terminal. Then type the following command on terminal:
<br> <code> git clone https://github.com/JiguangLi/Blaze_Function.git </code>
<br> You will then be ready to go.

## Descriptions:
<br> AFS.py: implementation of the AFS algorithm. It can produce the same result as Xin's original R code.
<br>
<br> ALSFS.py: implementation of the ALSFS algorithm. The final result might slightly differ from Xin's original code because the minimize function from scipy and the optim function from R sometimes can produce different results for the same optimazation problem.
<br>
<br> Boundary_Correction.py: calculate the weighted average of the blaze-removed spectrum of the two orders to correct the boundary of spectrums and to estimate the blaze function in the overlapping region. The method is discussed in section 2.4.1 of the <a href="https://arxiv.org/pdf/1904.10065.pdf"> paper </a>. 
<br>
<br> LS_Smoothing.py: An exmaple to use AFS to smooth the raw lab source spectrum, as discussed in section 2.2.2 of the <a href="https://arxiv.org/pdf/1904.10065.pdf"> paper </a>.
<br>
<br>
Data: includes all the csv files that will be used in the usage examples illustrated below
<br>
## Usage:
<br>
1. An Example to run AFS.py:
<pre>
  <code>
# load essential packages, make sure you have downloaded the repository
import pandas as pd
from AFS import *

# read the input csv file as a pandas dataframe,
# ExampleSpectrum.csv should two columns: wavelength and intensity
data= pd.read_csv('ExampleSpectrum.csv', sep=',')

# run the AFS algorithm where result, a one-dimensional vector, contains the blaze removed spectrum
result= AFS(data,0.95,0.25)

# if you want to output the result as a CSV file in your working directory, you can do the following: 
# result1.csv contains two columns: wavelength and the blaze removed spectrum
x=data["wv"].values
df=pd.DataFrame({"wv":x,"intens":result})
df.to_csv("result1.csv", index=False)
    
  </code>
</pre>




