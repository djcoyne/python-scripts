# -*- coding: utf-8 -*-
"""
@author djcoyne

To implement this function, either copy the code directly into
your .py file or copy the file into your python path and 
import it. It will support up to 10 lines (more is just spaghetti)

    Multi-line time-series grapher
    
    Parameters
    --------------
    data: .csv file
        The file the grapher will pull graph data from
    
    title: string
        Graph title

    x: item
        Location in data for the x-axis variable (running time variable).
        Can be a number or a column header.
    
    y: list of strings
         Location and labels for y values for lines.
         Should take the format ['location = y1 loc, label=y1 label','location = y2 loc, label = y2 label',...]
     
    xti: string
         Title string for x-axis label
         
    yti: string
        Title string for y-axis label
        
    xline: list of strings
        Added x-lines
        Should take the format ["x=value, axvline options","x=value, axvline options",...]
        
    yline: list of strings
        Added y-lines
        Should take the format ["y=value, axhline options","y=value, axhline options",...]
        
    errorband: list of strings
        location of estimates, location of standard errors, and (optionally) CI for plotting.
        Should take the format ['est= est1 location, se= se1 location, ci = ci1',... ]
        ci can take values 90, 95, 99.
     
    Returns
    --------------
    fig: matplotlib figure
        Returned figure that can be saved, if desired


"""

import pandas as pd
import matplotlib.pyplot as plt
from sys import exit

def mltsgraph(data, xvar, yvar, title='', xti='', yti='', xline=None, yline=None, errorband=None):
    
    """
    Input arguments error handling phase
    """
            
    if not xvar:
        print('Error: No x variable defined!')
        exit(1)
    
    if not yvar:
        print('Error: No y variable defined!')
        exit(1)
        
    if not data:
        print('Error: No data file defined!')
        exit(1)
                    
    """
    Read in the data
    """
    
    try:
        df = pd.read_csv(data)
    except:
        print('Error: Data file "' +data+ '" not found!')
        exit(1)

    """
    Define the figure
    """         
    fig = plt.figure()
   
    """
    Add any added x or y lines
    """
    if xline:
        for x in xline:
            xarg = dict(e.split('=') for e in x.split(', '))
            xarg['x']=int(xarg['x'])
            plt.axvline(**xarg)
    if yline:
        for y in yline:
            yarg = dict(e.split('=') for e in y.split(', '))
            yarg['y']=int(yarg['y'])
            plt.axhline(**yarg)
        
    """
    Add the main lines
    """
    plotMap = ['color=maroon, marker=o, markersize=5',
               'color=blue, marker=s, markersize=5',
               'color=green, marker=^, markersize=5',
               'color=gold, marker=x, markersize=5',
               'color=darkorchid, marker=P, markersize=5',
               'color=deepskyblue, marker=D, markersize=5',
               'color=magenta, marker=*, markersize=5',
               'color=burlywood, marker=v, markersize=5',
               'color=chartreuse, marker=8, markersize=5',
               'color=tomato, marker=CARETRIGHT, markersize=5']
               

    estimates=[]    
    
    i=0
    for yv in yvar:
        yvarg = dict(e.split('=') for e in yv.split(', '))
        newY = yVar(**yvarg)
        estimates.append(newY.location)
        la = "label="+newY.label
        linearg = dict(e.split('=') for e in la.split(', '))        
        plotarg = dict(e.split('=') for e in plotMap[i].split(', '))
        plotarg['markersize']=int(plotarg['markersize'])
        plt.plot(df[xvar], df[newY.location], **linearg, **plotarg)
        i = i+1
        
    
    """
    Error Bar Section
    """
    
    if errorband:
        for eb in errorband:
            ebarg = dict(e.split('=') for e in eb.split(', '))
            eBand = errorBand(**ebarg)
            ebcolor = dict(e.split('=') for e in plotMap[estimates.index(str(eBand.est))].split(', '))['color']
            if eBand.ci == '95':
                c = 1.96
            elif eBand.ci == '99':
                c = 2.575
            else:
                c = 1.64
            plt.fill_between(df[xvar], df[eBand.est]+c*df[eBand.se], df[eBand.est]-c*df[eBand.se], alpha = 0.15, color=ebcolor)
        
    """
    Graph finishing and return
    """    
    plt.grid()
    plt.xlabel(xti)
    plt.ylabel(yti)
    plt.title(title)
    plt.legend(loc='best', fontsize='8')
    plt.show()
    return fig

class yVar(object): 
    def __init__(self, location='', label=''):
        self.location=location
        self.label=label     
        
class errorBand(object): 
    def __init__(self, est='', se='', ci='90'):
        self.est=est
        self.se=se
        self.ci=ci            
          
    
    
         
