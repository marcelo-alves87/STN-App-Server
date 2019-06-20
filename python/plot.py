# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import csv
import sys
import os



style.use('dark_background')

def input_file_csv(type1):
   x,y = normalize_csv(os.path.dirname(os.path.abspath(__file__)) + '/' + type1)
   x = x[5:101]
   y = y[5:101]
   plt.plot(x,y,c='y')
   return min(x), max(x)

def normalize_csv(filename):
    xs = []
    ys = []
    end_index = 0
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            s = row[0]
            if s.find('END') >= 0:
               end_index += 1 
               #1 S11, 2 Phase, 3 SWR, 4 Real/Imaginary 
               if end_index == 1: 
                   break
               else:
                   xs = []
                   ys = []               
            elif(s.find('!') < 0 and s.find('BEGIN') < 0 and s.find('END') < 0):
                xs.append(row[0])
                if len(row) > 2:
                    #1 Real, 2 Imaginary
                    ys.append(row[1])
                else:
                    ys.append(row[1])
    return np.array(xs, dtype=np.float64), np.array(ys, dtype=np.float64)



minx, maxx = input_file_csv(str(sys.argv[1]))
#minx, maxx = input_file_csv('H2D100.csv')



plt.xticks(np.arange(minx, maxx,step=0.3))
plt.xlabel('Metros (m)')
plt.ylabel('VSWR')
#plt.title('AnÃ¡lise de Haste de Ã‚ncora')
plt.grid()
#plt.show()
plt.savefig(os.path.dirname(os.path.abspath(__file__)) + '/' + str(sys.argv[1]) + '.png')

