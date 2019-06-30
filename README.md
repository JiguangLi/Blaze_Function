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
AFS.py: implementation of the AFS algorithm. It can produce the same result as Xin's original R code.
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
### AFS.py:
</p>AFS algorithm can be used to remove the blaze function of s spectrum when this
is no available corresponding lab source spectrum. </p>

<p>The AFS algorithm  allows users to specify 3 parameters:
<p>order: order represents the spectrum to remove blaze function. It is an n by 2 data frame, in which the first column records wavelength and the second column records intensity.
  <br>
q: a number between 0 and 1.  Under q quantile within each window will be used to fit a local polynomial model. The default value is 0.95.
  <br>
d: the smoothing parameter for local polynomial regression, which is the proportion of neighboring points to be used when fitting at one point. The default value is 0.25.
</p>
<p>The algorithm will return a one dimensional vector with length n, representing the blaze removed spectrum</p>
<pre>
  <code>
# load essential packages, make sure you have downloaded the repository
import pandas as pd
from AFS import *
<br>
# read the input csv file as a pandas dataframe,
# ExampleSpectrum.csv should have two columns: wavelength and intensity
data= pd.read_csv('ExampleSpectrum.csv', sep=','
<br>
# run the AFS algorithm, where result, a one-dimensional vector, contains the blaze removed spectrum.
result= AFS(data,0.95,0.25)
<br>
# If you want to plot the blaze-removed spectrum
plt.clf()
plt.plot(data["wv"], result, 'b', linewidth=1, label='Blaze removed spectrum python')
plt.legend(loc='lower right')
plt.title("AFS Result")
<br>
# if you want to output the result as a CSV file in your working directory, you can do the following: 
# result1.csv contains two columns: wavelength and the blaze removed spectrum
x=data["wv"].values
df=pd.DataFrame({"wv":x,"intens":result})
df.to_csv("result1.csv", index=False)
    
  </code>
</pre>

### An Example to use ALSFS.py:
<pre>
  <code>
# load essential packages, make sure you have downloaded the repository
import pandas as pd
from ALSFS import *
import matplotlib.pyplot as plt
<br>
# read the input csv files as a pandas dataframe
# data is the input spectrum and source is the lab source, each of which is n by 2 matrix
data= pd.read_csv('ExampleSpectrum.csv', sep=',')
source= pd.read_csv('LabSource.csv', sep=',')
result= ALSFS(data,source,0.95,0.25)
print(result)
<br>
#If you want to plot the blaze-removed spectrum
plt.clf()
plt.plot(data["wv"], result, 'b', linewidth=1, label='Blaze removed spectrum python')
plt.legend(loc='lower right')
plt.title("ALSFS Result")
<br>
# if you want to output the result as a pandas dataframe
# You will find a new csv file named result1.csv in your working directory
# result1.csv contains two columns: wavelength and the blaze removed spectrum
x=data["wv"].values
df=pd.DataFrame({"wv":x,"intens":result})
df.to_csv("result1.csv", index=False)   
  </code>
</pre>

### An Example to use Boundary_Correction.py:
<pre>
  <code>
# Load Essential Packages
import pandas as pd
from Boundary_Correction import*
import matplotlib.pyplot as plt
<br>
# Read the left and right order in csv files
# where left_data is an n1 by 2 dataframe, and right data is an n2 by 2 dataframe
left_data= pd.read_csv('left_order.csv', sep=',')
right_data= pd.read_csv('right_order.csv', sep=',')
<br>
# Run the boundary correction algorithm
# result is a 2-element tuple that contains the corrected left_order and righr_order
result= Boundary_correction(left_data,right_data)
<br>
# To retrieve the corrected left_order and right_order:
left_order=result[0]
right_order=result[1]
<br>
# output the corrected two orders into two csv files
left_order.to_csv("corrected_left_order.csv", index=False)
right_order.to_csv("corrected_right_order.csv", index=False)
  </code>
</pre>

### An Example to use LS_Smoothing.py:
<pre>
  <code>
# Load Essential Packages
import pandas as pd
from LS_Smoothing import*
import matplotlib.pyplot as plt
<br>
#input the Raw lab source in csv format
# result records a smooth version of the raw lab source as a dataframe
data= pd.read_csv("RawLabSource.csv", sep=',')
result= LSS(data, 0.98, 0.25, 0.97)
<br>
# To output the result in a csv file
result.to_csv("smooth lab source.csv", index=False)
  </code>
</pre>
<br>

## Some advice on parameter selection from the paper:
<p>There are two parameters in the AFS Algorithm:</p>
<p>
q: selecting a good value of q means selecting points on the spectrum that do not drop into absorption lines. In general, If the S/N is high or the absorption is large, a larger q is needed to select points in S so that few points fall in absorption lines; if S/N is low or there is minimal absorption, a smaller q is needed to get enough points. As a rule of thumb,  a q from 0.95 to 0.99 works for S/N 300, a q from 0.85 to 0.95 works for S/N 150, and a q from 0.5 to 0.85 works for S/N lower than 150.</p>
<p>
d: If there are many absorption lines or any absorption lines that are wide, a large d is needed to get a good estimate. If there are few absorption lines or absorption lines that are narrow, a small d is needed so that the estimation better adapts to local regions. A range between 0.15-0.3 is usually a good starting point to find the right value of d.
</p>
<p>
In general, the blaze function estimate is more sensitive to small changes in q than d. 
we can start with the default value of d and tune
the parameter q within the range according to its S/N and amount of absorption.
</p>
<p>
The ALSFS algorithm has the same parameters as AFS and can be determined in a similar fashion. In ALSFS, d has less influence on the results than for the AFS algorithm. The quantile parameter q epends on the appearances of spikes. If spikes are long, use a smaller q such as 0.95; if spikes are very small, use a larger q such as 0.98 or 0.99. </p>






