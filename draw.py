import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mc
import colorsys
from matplotlib import rcParams

def lighten_color(color, amount=0.5):

    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])
def draw_ARs(parameter_range,Algo_mean_list,Algo_std_list,Algo_Names,fname,x_label,y_label = 'Max Cover Time', position = None):
    plt.cla()

    color_list = ['k','g', 'b','r' ,'m', 'y',  'c','#D2691E','#CEFFCE']#['k','r','b', 'm', 'y', 'g',  ]
    marker_list = ['o', 'v', '^', '<', '>', 's','3','8','|','x'] #['o', 'v', '^', '<', '>', 's']
    plt.xlabel(x_label,fontsize=14)
    plt.ylabel(y_label,fontsize=14)

    for i in range(len(Algo_Names)):
        plt.errorbar(parameter_range, Algo_mean_list[i], yerr=np.array([x*0.1 for x in Algo_std_list[i]]),ecolor=color_list[i],fmt='none')

        plt.plot(parameter_range, Algo_mean_list[i], color=color_list[i],linestyle='-', linewidth=1,label = Algo_Names[i]) # marker=marker_list[i]


    if len(Algo_Names) > 1:
        if position == None:
            plt.legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0.2) #bbox_to_anchor=(0.2, 0.95))
        else:
            #plt.legend(loc=position,bbox_to_anchor=(0.2,0),fontsize=16)
            #plt.legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0.2)
            plt.legend(loc='upper left',fontsize=10)
    #plt.tight_layout()
    plt.savefig(fname, dpi=200,bbox_inches='tight')
    #plt.savefig(fname)

def draw_historgram(datasets,Algo_mean_list,Algo_Name,fname,x_label,y_label ='Max Cover Time' ):
    plt.cla()
    color_list = ['k', 'g','b','r' ,'c',  'm', 'y','#D2691E','#CEFFCE']#['k','r','b', 'm', 'y', 'g',  ]
    color_list = [lighten_color(c, 0.3) for c in color_list[:4]]

    plt.xlabel(x_label,fontsize=14)
    plt.ylabel(y_label,fontsize=14)
    x = range(len(datasets))

    for algo_index in range(len(Algo_Name)):
        rects = plt.bar(x=[i+algo_index*0.2 for i in x],height=[y[algo_index] for y in Algo_mean_list],width=0.2,color=color_list[algo_index],label=Algo_Name[algo_index])
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x()+rect.get_width()/2,height+1,str(height),ha='center',va='bottom')

    plt.xticks([index+0.3 for index in x],datasets)


    plt.legend(loc='upper right',fontsize=10)
    plt.savefig(fname, dpi=200,bbox_inches='tight')

