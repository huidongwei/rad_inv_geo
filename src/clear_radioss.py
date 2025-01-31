# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 11:26:59 2025

@author: Huidong
"""
import os
import glob
    
def del_radioss_rst():

    cwd = os.getcwd()
    
    for item in os.listdir(cwd):
        
        if item.endswith(".rst") or item.endswith(".tmp"):
        
            os.remove(os.path.join(cwd, item))
            
    pattern = r"*DESKTOP*"
    
    for item in glob.iglob(pattern, recursive=True):
        
        os.remove(item)
            
del_radioss_rst()