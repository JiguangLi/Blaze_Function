#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 10:54:00 2019

@author: jiguangli
"""


import pandas as pd
from LS_Smoothing import*
import matplotlib.pyplot as plt

# =============================================================================
# # read the input csv file as a pandas dataframe,
# # ExampleSpectrum.csv has two columns: wavelength and intensity
# data= pd.read_csv('ExampleSpectrum.csv', sep=',')
# 
# # run the AFS algorithm where result contains the blaze removed spectrum
# result= AFS(data,0.95,0.25)
# 
# # If you want to plot the blaze-removed spectrum
# plt.clf()
# plt.plot(data["wv"], result, 'b', linewidth=1, label='Blaze removed spectrum python')
# plt.legend(loc='lower right')
# plt.title("AFS Result")
# 
# # if you want to output the result as a pandas dataframe
# # You will find a new csv file named result1.csv in your working directory
# # result1.csv contains two columns: wavelength and the blaze removed spectrum
# x=data["wv"].values
# df=pd.DataFrame({"wv":x,"intens":result})
# df.to_csv("result1.csv", index=False)
# 
# =============================================================================

# =============================================================================
# 
# 
# # read the input csv files as a pandas dataframe
# # data is the input spectrum and source is the lab source, each of which is n by 2 matrix
# data= pd.read_csv('ExampleSpectrum.csv', sep=',')
# source= pd.read_csv('LabSource.csv', sep=',')
# result= ALSFS(data,source,0.95,0.25)
# print(result)
# 
# #If you want to plot the blaze-removed spectrum
# plt.clf()
# plt.plot(data["wv"], result, 'b', linewidth=1, label='Blaze removed spectrum python')
# plt.legend(loc='lower right')
# plt.title("ALSFS Result")
# # 
# # if you want to output the result as a pandas dataframe
# # You will find a new csv file named result1.csv in your working directory
# # result1.csv contains two columns: wavelength and the blaze removed spectrum
# x=data["wv"].values
# df=pd.DataFrame({"wv":x,"intens":result})
# df.to_csv("result1.csv", index=False)
# =============================================================================



# =============================================================================
# # Read the left and right order in csv files
# # where left_data is an n1 by 2 dataframe, and right data is an n2 by 2 dataframe
# left_data= pd.read_csv('left_order.csv', sep=',')
# right_data= pd.read_csv('right_order.csv', sep=',')
# 
# # Run the boundary correction algorithm
# # result is a 2-element tuple that contains the corrected left_order and righr_order
# result= Boundary_correction(left_data,right_data)
# 
# # To retrieve the corrected left_order and right_order:
# left_order=result[0]
# right_order=result[1]
# 
# # output the corrected two orders into two csv files
# left_order.to_csv("corrected_left_order.csv", index=False)
# right_order.to_csv("corrected_right_order.csv", index=False)
# =============================================================================

data= pd.read_csv("RawLabSource.csv", sep=',')
result= LSS(data, 0.98, 0.25, 0.97)
