import numpy as np
import csv
import xlsxwriter
import pdb

def convert_to_mhz(data):
    return data / 10 ** 6

def normalize_csv(filename,param1, param2):
    
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
               if end_index == param1: 
                   break
               else:
                   xs = []
                   ys = []               
            elif(s.find('!') < 0 and s.find('BEGIN') < 0 and s.find('END') < 0 and s.find('EN') < 0):
                
                xs.append(row[0])
                if len(row) > 2:
                    #1 Real, 2 Imaginary
                    ys.append(row[param2])
                else:
                    ys.append(row[1])
    return np.array(xs, dtype=np.float64), np.array(ys, dtype=np.float64)

wb = xlsxwriter.Workbook(r'/home/pi/Documents/STN_Server/python/Pi.xlsx')
ws = wb.add_worksheet('Plan1')

header_format = wb.add_format()
header_format.set_bold()
header_format.set_align('center')
#header_format.set_num_format('#.#0')

data_format = wb.add_format()
data_format.set_align('center')
#data_format.set_num_format('#0.#####0')
path1 = r'/home/pi/Documents/STN_Server/python/Pi.csv'
for j in range(1,10):
    #S11
    x, y1 = normalize_csv(path1, 1, 1)

    for i, yi in enumerate(y1):
        ws.write(0, i, convert_to_mhz(x[i]), header_format)
        ws.write(j, i, yi, data_format)

    #Phase
    x, y2 = normalize_csv(path1, 2, 1)

    for i, yi in enumerate(y2):
        ws.write(0, len(y1) + i, convert_to_mhz(x[i]), header_format)
        ws.write(j, len(y1) + i, yi, data_format)

    #SWR
    x, y1 = normalize_csv(path1, 3, 1)

    for i, yi in enumerate(y1):
        ws.write(0, 2*len(y2) + i, convert_to_mhz(x[i]), header_format)
        ws.write(j, 2*len(y2) + i, yi, data_format)
        
    #Real
    x, y2 = normalize_csv(path1, 4, 1)

    for i, yi in enumerate(y2):
        ws.write(0, 3*len(y1) + i, convert_to_mhz(x[i]), header_format)
        ws.write(j, 3*len(y1) + i, yi, data_format)

    #Img
    x, y1 = normalize_csv(path1, 4, 2)

    for i, yi in enumerate(y1):
        ws.write(0, 4*len(y2) + i, convert_to_mhz(x[i]), header_format)
        ws.write(j, 4*len(y2) + i, yi, data_format)
          
    ws.write(j, 5*len(y2), ' ')
    ws.write(j, 5*len(y2) + 1,  0, data_format)
    ws.write(j, 5*len(y2) + 2, '1A', header_format)

wb.close()

