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

    xvar: item
        Location in data for the x-axis variable (running time variable).
        Can be a number or a column header.
    
    yvar: list of strings
         Location and labels for y values for lines.
         Should take the format ["location = 'y1 loc', label='y1 label'","location = 'y2 loc', label = 'y2 label'",...]
     
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
        
    errorband: list of tuples
     
    Returns
    --------------
    fig: matplotlib figure
        Returned figure that can be saved, if desired


"""

import pandas as pd
import matplotlib.pyplot as plt

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
        exit(2)

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
               

    i=0
    for yv in yvar:
        yvarg = dict(e.split('=') for e in yv.split(', '))
        newY = yVar(**yvarg)
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
        errorBand(errorband)
        
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
    
def errorBand():
    print('ERRORBAND!')     
    
    
         
