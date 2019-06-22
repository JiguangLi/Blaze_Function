#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 11:08:55 2019

@author: jiguangli
"""

import pandas as pd
import matplotlib.pyplot as plt

data= pd.read_csv('result_comparision.csv', sep=',')
print(data)

x=data["wv"]
y_1=data["AFS.py"]
y_2=data["AFS.R"]
y_3=data["AFS_rpy2.py"]
plt.clf()
plt.plot(x, y_1, 'b', linewidth=1, label='Normalization using python')
plt.plot(x, y_3, 'y', linewidth=1, label='Normalization using ryp2 python')
plt.plot(x, y_2, 'r', linewidth=1, label='Normalization using R')
plt.legend(loc='lower right')
plt.title("Result Comparision in Blaze Remove Spectrum")

