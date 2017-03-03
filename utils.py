# -*- coding: utf-8 -*-


def plotvars(ax,varnames,res, color = None, legend = True, style="-"):
    num = len(varnames)
    for i,name in zip(res[varnames].view((float,num)).T,varnames):
        #print("bla"+str(i))
        if not legend: name = None
        if color: ax.plot(res['t'],i, label = name, color = color, linestyle=style)#, marker=style, markersize=10)
        else: ax.plot(res['t'],i, label = name)
    if legend: ax.legend(loc='best',fancybox=True, framealpha=0.8, prop={'size':9})



