#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 12:14:02 2019
@author: jiguangli
"""

# Alpha-shape Fitting to Spectrum algorithm (AFS) in Python using ryp2
# Based on Xin's code here: https://github.com/xinxuyale/AFS/blob/master/functions/AFS.R
# We used rpy2 package here


# Load essential packages
import pandas as pd
import numpy as np
import alphashape
import shapely
from rpy2.robjects import r
import rpy2.robjects as robjects

from pathlib import Path


# Input variables:
# order: the order of spectrum to remove blaze function. It is an n by 2 NumPy arrays,
#   where n is the number of pixels. Each row is the wavelength and intensity at 
#   each pixel.
# a: the parameter a should be a number between 3 and 12. It determines the value
#    of alpha in calculating alphashape, which is defined as the range of wavelength
#    diveded by a. The default value of a is 6. 
# q: the parameter q, uppder q quantile within each window will be used to fit 
#   a local polynomial model. 
# d: the smoothing parameter for local polynomial regression, which is the 
#   proportion of neighboring points to be used when fitting at one point. 

# Define AFS function
def AFS (order, a=6, q=0.95, d=0.25):
    # Default value of q and d are 0.95 and 0.25.
    # Change the column names and format of the dataset.
    order.columns=["wv","intens"]
    # n records the number of pixels.
    n=order.shape[0]
    # ref is a pandas series recording wavelength
    ref=order["wv"]
    # Variable u is the parameter u in the step 1 of AFS algorithm. It scales the intensity vector.
    u=(ref.max()-ref.min())/10/order["intens"].max()
    order["intens"] = order["intens"]*u 
    
    # Let alpha be 1/6 of the wavelength range of the whole order. 
    alpha= (order["wv"].max()-order["wv"].min())/a
    

    # This chunk of code detects loops in the boundary of the alpha shape. 
    # Ususally there is only one loop(polygon).
    # Variable loop is a list.
    # The indices of the k-th loop are recorded in the k-th element of variable loop. 
    loops=[]
    # Variable points is a list that represents all the sample point (lambda_i,y_i)
    points=[(order["wv"][i],order["intens"][i]) for i in range(order.shape[0])]
    #tl=time()
    alpha_shape = alphashape.alphashape(points, 1/alpha)
    #th=time()
   # print("alphashape function takes ", th-tl)
    
    
    # Input Vairables:
    # polygon: shapely polygon object
    # return Variable:
    # variable indices is a list recording the indices of the vertices in the polygon
    def find_vertices(polygon):
        coordinates=list(polygon.exterior.coords)
        return [ref[ref==coordinates[i][0]].index[0] for i in range(len(coordinates))]
        
    # if alpha_shape is just a polygon, there is only one loop
    # if alpha_shape is a multi-polygon, we interate it and find all the loops.
    if (isinstance(alpha_shape,shapely.geometry.polygon.Polygon)):
        temp= find_vertices(alpha_shape)
        loops.append(temp)
       
    else:
        for polygon in alpha_shape:
            temp= find_vertices(polygon)
            loops.append(temp)
    
    # Use the loops to get the set W_alpha. 
    # Variable Wa is a vector recording the indices of points in W_alpha.
    Wa=[0]
    for loop in loops:
        temp=loop
        temp=loop[:-1]
        temp=[i for i in temp if (i<n-1)]
        max_k=max(temp)
        min_k=min(temp)
        len_k=len(temp)
        as_k=temp
        if((as_k[0] == min_k and as_k[len_k-1] == max_k)==False):
                index_max= as_k.index(max_k)
                index_min= as_k.index(min_k)
                if (index_min < index_max): 
                    as_k =as_k[index_min:(index_max+1)]
                else:
                    as_k= as_k[index_min:]+as_k[0:(index_max+1)]    
       
        Wa=Wa+as_k
    Wa.sort()  
    Wa=Wa[1:]
   
    # AS is an n by 2 matrix recording tilde(AS_alpha). Each row is the wavelength and intensity of one pixel.
    AS=order.copy()
    for i in range(n-1):
        indices=[m for m,v in enumerate(Wa) if v > i]
        if(len(indices)!=0):
            index=indices[0]
            a= Wa[index-1]
            b= Wa[index]
            AS["intens"][i]= AS["intens"][a]+(AS["intens"][b]-AS["intens"][a])*((AS["wv"][i]-AS["wv"][a])/(AS["wv"][b]-AS["wv"][a]))
        else:
           # AS=AS.drop(list(range(i, n)))
            break

    # Run a local polynomial on tilde(AS_alpha), as described in step 3 of the AFS algorithm.
    # Use the function loess_1d() to run a second order local polynomial.
    # Variable y_result is the predicted output from input x
    x=AS["wv"].values
    y=AS["intens"].values
    # covert x and y to R vectors
    x = robjects.FloatVector(list(x))
    y = robjects.FloatVector(list(y))
    df = robjects.DataFrame({"x": x, "y": y})
    # run loess (haven't found a way to specify "control" parameters)
    loess_fit = r.loess("y ~ x", data=df, degree = 2, span = d, surface="direct")
    B1 =r.predict(loess_fit, x)
    # Add a new column called select to the matrix order. 
    # order["select"] records hat(y^(1)).
    select= order["intens"].values/B1
   

    order["select"]=select
    # Make indices in Wa to the format of small windows. 
    # Each row of the variable window is a pair of neighboring indices in Wa.
    window= np.column_stack((Wa[0:len(Wa)-1],Wa[1:]))
    
    # This chunk of code select the top q quantile of points in each window.
    # The point indices are recorded in variable index, which is S_alpha, q in step 4
    # of the AFS algorithm.
    index=[0]
    for i in range(window.shape[0]):
        loc_window= window[i,]
        temp = order.loc[loc_window[0]:loc_window[1]]
        index_i= temp[temp["select"] >= np.quantile(temp["select"],q)].index
        index=index+list(index_i)  
    index=np.unique(index[1:])  
    index=np.sort(index)
    
 
    # Run Loess for the last time
    x_2=order.iloc[index]["wv"].values
    y_2=order.iloc[index]["intens"].values
    x_2 = robjects.FloatVector(list(x_2))
    y_2 = robjects.FloatVector(list(y_2))
    df2 = robjects.DataFrame({"x_2": x_2, "y_2": y_2})
    loess_fit2 = r.loess("y_2 ~ x_2", data=df2, degree = 2, span = d,surface="direct")
    y_final= r.predict(loess_fit2, x)
    # Return the blaze-removed spectrum.
    result= order["intens"].values/y_final
    return result



# Input variable:
# directory: a string representing the directory of an order
# name: a string represnting the file name. The file can either be in csv or fits format.
#       The first column and the second column must be wavelength and intensity respectively.
# a: the parameter a should be a number between 3 and 12. It determines the value
#    of alpha in calculating alphashape, which is defined as the range of wavelength
#    diveded by a. The default value of a is 6. 
# q: the parameter q, uppder q quantile within each window will be used to fit 
#   a local polynomial model. 
# d: the smoothing parameter for local polynomial regression, which is the 
#   proportion of neighboring points to be used when fitting at one point. 


def AFS_d(directory,name, a=6, q = 0.95, d = 0.25):
     path=directory+"/"+name
     p = Path(path)
     
     if(p.exists()):
         
         if(name[-4:]==".csv"):
             csv= pd.read_csv(path, sep=',')
             data = csv.iloc[:,0:2]
             result= AFS(data,a,q,d)
             return result
         elif(name[-5:]==".fits"):
             from astropy.table import Table
             data_fits = Table.read(path, format='fits')
             data_fits=data_fits[data_fits.colnames[0],data_fits.colnames[1]]
             data=data_fits.to_pandas()
             result= AFS(data,a,q,d)
             return result
         else:
             raise Exception("The format of this file is neither csv nor fits")
           
     else:
         raise Exception("directory or file doesn't exist")
         
