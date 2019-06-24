#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 20:41:19 2019

@author: jiguangli
"""
# Alpha-shape and Lab Source Fitting to Spectrum algorithm (ALSFS) in Python
# Based on Xin's code here: https://github.com/xinxuyale/AFS/blob/master/functions/ALSFS.R

# Load essential packages
import pandas as pd
import numpy as np
import alphashape
import shapely

from rpy2.robjects import r
import rpy2.robjects as robjects
import rpy2.rinterface as ri
from scipy.optimize import minimize




# Input variables:
# order: the order of spectrum to remove blaze function. It is an n by 2 matrix,
#   where n is the number of pixels. Each row is the wavelength and intensity at 
#   each pixel.
# led: the corresponding order of lab source spectrum. It is also an n by 2 matrix.
# q: the parameter q, uppder q quantile within each window will be used to 
#   do linear transformation on the lab source spectrum. 
# d: the smoothing parameter for local polynomial regression, which is the 
#   proportion of neighboring points to be used when fitting at one point. 




# Input Vairables:
# polygon: shapely polygon object
# ref: a pandas series that tracks the index of each data point
# return Variable:
# variable indices is a list recording the indices of the vertices in the polygon
def find_vertices(polygon,ref):
    coordinates=list(polygon.exterior.coords)
    indices=[]
    for i in range(len(coordinates)):
        indices.append(ref[ref==coordinates[i][0]].index[0])
    return indices

    

def ALSFS (order, led, q = 0.95, d = 0.25):
    # Default value of q and d are 0.95 and 0.25.
    # Change the column names and format of the dataset.
    order.columns=["wv","intens"]
    # n records the number of pixels.
    n=order.shape[0]
    # Variable u is the parameter u in the step 1 of AFS algorithm. It scales the intensity vector.
    u=(order["wv"].max()-order["wv"].min())/10/order["intens"].max()
    order["intens"] = order["intens"]*u 
    
    # Let alpha be 1/6 of the wavelength range of the whole order. 
    alpha= (order["wv"].max()-order["wv"].min())/6
    
    # This chunk of code detects loops in the boundary of the alpha shape. 
    # Ususally there is only one loop(polygon).
    # Variable loop is a list.
    # The indices of the k-th loop are recorded in the k-th element of variable loop. 
    loops=[]
    # Variable points is a list that represents all the sample point (lambda_i,y_i)
    points=[(order["wv"][i],order["intens"][i]) for i in range(order.shape[0])]
    alpha_shape = alphashape.alphashape(points, 1/alpha)
    ref=order["wv"]
    # if alpha_shape is just a polygon, there is only one loop
    # if alpha_shape is a multi-polygon, we interate it and find all the loops.
    if (isinstance(alpha_shape,shapely.geometry.polygon.Polygon)):
        temp= find_vertices(alpha_shape,ref)
        loops.append(temp)
       
    else:
        for polygon in alpha_shape:
            temp= find_vertices(polygon,ref)
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
    #wv_vec= robjects.FloatVector(list(order["wv"]))
    B1 =r.predict(loess_fit, x)
    # Add a new column called select to the matrix order. 
    # order["select"] records hat(y^(1)).
    select= order["intens"].values/B1
    order["select"]=select
    
    # Calculate Q_2q-1 in step 3 of the ALSFS algorithm.
    Q=np.quantile(order["select"],1-(1-q)*2)
    
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
        temp_q= max(np.quantile(temp["select"],q),Q)
        index_i= temp[temp["select"] >= temp_q].index
        index=index+list(index_i)  
    index=np.unique(index[1:])  
    index=np.sort(index)
    
    
    # The following chunk of code does step 5 of the ALSFS algorithm.
    # The function optim() is used to calculate the optimization of the three 
    # linear transformation parameters.
    # The final estimate is in variable B2.
# =============================================================================
#     m <- length(index)
#     led[,2] <- led[,2]/max(led[,2])*max(order$intens)
#     Xnew <- cbind(rep(1, m), led[index,2], led[index,1])
#     beta <- c(0, 1, 0)
#     fn <- function(x) sum((order$intens[index]/(Xnew%*%x)-1)^2)
#     beta <- optim(beta, fn)$par
#     B2 <- beta[1]+beta[2]*led[,2]+beta[3]*led[,1]
# =============================================================================
    m=len(index)
    led["intens"]=led["intens"]/np.max(led["intens"].values)*np.max(order["intens"].values)
    Xnew=led.iloc[index]
    Xnew["constants"]=np.ones(m)
    columnsTitles=["constants","intens","wv"]
    Xnew=Xnew.reindex(columns=columnsTitles)
    order_new= order.iloc[index]
    beta= np.array([0,1,0])

    v1= order_new["intens"].values
    m1= Xnew.values
    
    
    def f(beta):
        return np.sum(np.square((np.divide(v1,np.matmul(m1,beta))-1)))
   
# =============================================================================
#     print(f(beta))
#     op_result= minimize(f,beta,method='nelder-mead')
#     print(op_result.x)
#     print(f(np.array([-7.7225,0.9975,0.001548])))
#     print(f(np.array([-8.995,0.9979,0.001801])))
# =============================================================================
    print("hah")
    r_f = ri.rternalize(f)
    Beta =  robjects.FloatVector((0,1,0))
    res = r.optim(Beta, r_f)
    print(res)


   
    
    

    
    
data= pd.read_csv('ExampleSpectrum.csv', sep=',')
source= pd.read_csv('LabSource.csv', sep=',')
result= ALSFS(data,source,0.95,0.25)
