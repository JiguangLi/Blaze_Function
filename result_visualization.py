#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 11:08:55 2019

@author: jiguangli
"""

import pandas as pd
import matplotlib.pyplot as plt

data= pd.read_csv('ALSFS_result_comparision.csv', sep=',')
print(data)

x=data["wv"]
y_1=data["ALSFS.py"]
y_2=data["ALSFS.R"]

plt.clf()
plt.plot(x, y_1, 'b', linewidth=1, label='Blaze removed spectrum python')
plt.plot(x, y_2, 'r', linewidth=1, label='Blaze removed spectrum R')
plt.legend(loc='lower right')
plt.title("Result Comparision in ALSFS")

