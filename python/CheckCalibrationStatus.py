import pyvisa as visa
import os
import time
from datetime import datetime
import struct
import numpy as np
import pandas as pd
import csv
import xlsxwriter
import sys
import pdb
import traceback
import shutil

ADDRESS = '169.254.120.255'

def initial_cal_and_open(device):
    temp_values = device.query_ascii_values(':SENSe:CORRection:COLLect:GUIDed:SCOunt?')
    print(temp_values)
    device.query(':SENSe:CORRection:COLLect:GUIDed:STEP:PROMpt? %d' % (1))

def initial_acquire_and_prompt(device, start, stop):
    device.write(':SENSe:CORRection:COLLect:GUIDed:STEP:ACQuire %d' % (start))
    print('insert_short')
    device.query(':SENSe:CORRection:COLLect:GUIDed:STEP:PROMpt? %d' % (stop))

def save_cal(device):
    device.write('*OPC')
    time.sleep(3)
    device.write(':SENSe:CORRection:COLLect:SAVE %d' % (0))
    device.write('*OPC')
    time.sleep(3)    
    device.write(':MMEMory:STORe:STATe "%s"' % ('Pi.sta'))
    device.write('*OPC')
    time.sleep(3)
    data = device.query_binary_values(':MMEMory:DATA? "%s"' % ('Pi.sta'),'B',False)
        
    new_file = open('/home/pi/Documents/STN_Server/python/Pi.sta', "w+")
    new_file.write(str(data))
    new_file.close()
    
    
    new_file1 = open('/home/pi/Documents/STN_Server/python/calstatus.txt', "w+")
    new_file1.write(datetime.today().strftime('%d/%m/%Y'))
    new_file1.close()


def check_cal_already_saved(device):
    try:
        device.write('*OPC')
        time.sleep(1)
        device.query_binary_values(':MMEMory:DATA? "%s"' % ('Pi.sta'),'B',False)
        new_file1 = open('/home/pi/Documents/STN_Server/python/calstatus.txt', "r")
        print(new_file1.read())
        new_file1.close()
    except:
        print('0.1.0')
    
def extract_data(device):
    try:
        device.write(':MMEMory:LOAD:STATe "%s"' % ('Pi.sta'))
        device.write('*OPC')
        time.sleep(1)
        device.write(':MMEMory:STORe:FDATA "%s"' % ('Pi.csv'))
        device.write('*OPC')
        time.sleep(1)
        filedata = device.query_binary_values(':MMEMory:DATA? "%s"' % ('Pi.csv'))
        
        new_file = open('/home/pi/Documents/STN_Server/python/Pi.csv', 'wb')
        for fl in filedata:
            new_file.write(bytearray(struct.pack('f', fl)))    
            
        new_file.close()
        
          
        print('5.1')
    except:    
        print('5.0')
        
def extract_data_corr(device, i):
    
        device.write(':MMEMory:LOAD:STATe "%s"' % ('Pi.sta'))
        device.write('*OPC')
        time.sleep(1)
        device.write(':MMEMory:STORe:FDATA "%s"' % ('Pi.csv'))
        device.write('*OPC')
        time.sleep(1)
        filedata = device.query_binary_values(':MMEMory:DATA? "%s"' % ('Pi.csv'))
        
        new_file = open('/home/pi/Documents/STN_Server/python/Pi'+ str(i) +'.csv', 'wb')
        for fl in filedata:
            new_file.write(bytearray(struct.pack('f', fl)))    
            
        new_file.close()
        main_corr(i)
        
def GeraMatrizCorrelacoes(dataset, qde_medicoes):
    matrizCorr = np.zeros((qde_medicoes, qde_medicoes))
    for i in range(qde_medicoes):
        m1 = dataset.iloc[i, :].values
        for j in range (qde_medicoes):
            m2 = dataset.iloc[j, :].values
            matrizCorr[i][j] = np.corrcoef(m1, m2)[0][1]
    return(matrizCorr)
            
def ZeraMenoresCorrelacoes(matrizCorr, min_corr, qde_medicoes):
    #pdb.set_trace()
    matrizCorrZerada = np.copy(matrizCorr)
    corr = 1
    if matrizCorr[qde_medicoes -2][qde_medicoes -1] < min_corr:
        corr = (matrizCorr[qde_medicoes -2][qde_medicoes -1])
    
    
    for i in range(qde_medicoes):
        for j in range (qde_medicoes):
            if (matrizCorr[i][j] < min_corr):
                matrizCorrZerada[i][j] = 0
                
                
    return(matrizCorrZerada, corr)    

def ListadeZeros(matrizCorrZerada, qde_medicoes):
    qdeZeros = []
    for i in range(qde_medicoes):
        nzeroslinha = 0
        for j in range(qde_medicoes):
            if (matrizCorrZerada[i][j] == 0):
                nzeroslinha += 1
        qdeZeros.append(nzeroslinha)
    return(qdeZeros)
    
def ColetaPrimeiraMedição(plan_dados):
    #Carrega arquivo
    dataset = pd.read_excel(plan_dados)
    #Extrai dados
    qde_medicoes = dataset.shape[0]
    qde_parametros = dataset.shape[1]
    return(dataset, qde_medicoes, qde_parametros)

def ColetaNovaMedição(plan_dados, dataset):
    #Carrega arquivo
    novaLinha = pd.read_excel(plan_dados)
    dataset = pd.concat([dataset, novaLinha])
    #Extrai dados
    qde_medicoes = dataset.shape[0]
    qde_parametros = dataset.shape[1]
    return(dataset, qde_medicoes, qde_parametros)

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

def main_convert_to_xlsx(index1):
    #pdb.set_trace()
    xlsx_default = r'/home/pi/Documents/STN_Server/python/Pi.xlsx'
    xlsx_name = r'/home/pi/Documents/STN_Server/python/Pi'+ str(index1) +'.xlsx'
    if os.path.isfile(xlsx_name) == True:
        os.remove(xlsx_name)
    if os.path.isfile(xlsx_default) == True:
        os.remove(xlsx_default)    
    wb = xlsxwriter.Workbook(xlsx_name)
    ws = wb.add_worksheet('Plan1')

    header_format = wb.add_format()
    header_format.set_bold()
    header_format.set_align('center')
    #header_format.set_num_format('#.#0')

    data_format = wb.add_format()
    data_format.set_align('center')
    #data_format.set_num_format('#0.#####0')
    path1 = r'/home/pi/Documents/STN_Server/python/Pi' + str(index1) + '.csv'
    for j in range(1,2):
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

#         #SWR
        x, y1 = normalize_csv(path1, 3, 1)

        for i, yi in enumerate(y1):
            ws.write(0, 2*len(y2) + i, convert_to_mhz(x[i]), header_format)
            ws.write(j, 2*len(y2) + i, yi, data_format)
#             
#         #Real
        x, y2 = normalize_csv(path1, 4, 1)

        for i, yi in enumerate(y2):
            ws.write(0, 3*len(y1) + i, convert_to_mhz(x[i]), header_format)
            ws.write(j, 3*len(y1) + i, yi, data_format)
# 
#         #Img
        x, y1 = normalize_csv(path1, 4, 2)

        for i, yi in enumerate(y1):
            ws.write(0, 4*len(y2) + i, convert_to_mhz(x[i]), header_format)
            ws.write(j, 4*len(y2) + i, yi, data_format)
              
#         ws.write(j, 5*len(y2), ' ')
#         ws.write(j, 5*len(y2) + 1,  0, data_format)
#         ws.write(j, 5*len(y2) + 2, '1A', header_format)

    wb.close()
    shutil.copy(xlsx_name,xlsx_default)
    
def main_corr(index1):
    #pdb.set_trace()
    n_samples = 3 #Quantidade de amostras válidas desejada
    min_corr = 0.95
    qdeMaximaMedicoes = 6
    index1 = int(index1)
    
   
    if index1 == 1:
        #main_convert_to_xlsx(1)
        print(0)
    else:    
        #/home/pi/Documents/STN_Server/python/Pi'+ str(i) +'.csv'
        
        if os.path.isfile('/home/pi/Documents/STN_Server/python/Pi1.xlsx') == True:
            dataset, qde_medicoes, qde_parametros = ColetaPrimeiraMedição('/home/pi/Documents/STN_Server/python/Pi1.xlsx')  
            #main_convert_to_xlsx(index1)
            for i in range(1, index1):                
                if os.path.isfile('/home/pi/Documents/STN_Server/python/Pi' + str(i+1) + '.xlsx') == True:
                    dataset, qde_medicoes, qde_parametros = ColetaNovaMedição('/home/pi/Documents/STN_Server/python/Pi' + str(i+1) + '.xlsx', dataset)
                else:
                    print('erro')
                    sys.exit()
            
            matrizCorr = GeraMatrizCorrelacoes(dataset, qde_medicoes)    
            matrizCorrZerada, corr = ZeraMenoresCorrelacoes(matrizCorr, min_corr, qde_medicoes)
            qdeZeros = ListadeZeros(matrizCorrZerada, qde_medicoes)
            
            if qde_medicoes > n_samples:
                qdeZerosTemp = qdeZeros[:]
                for i in range(len(qdeZeros)):
                    if(sum(qdeZerosTemp) == 0):
                        break
                    else:
                        #pdb.set_trace()
                        indicePiorMedicao = qdeZeros.index(max(qdeZerosTemp))
                        matrizLimpaTemp = np.delete(matrizCorrZerada, indicePiorMedicao, axis = 0)
                        matrizLimpaTemp = np.delete(matrizLimpaTemp, indicePiorMedicao, axis = 1)
                        qdeZerosTemp = ListadeZeros(matrizLimpaTemp, matrizLimpaTemp.shape[0])
                qdeZeros = qdeZerosTemp
                
            qdeMedValidas = 0    
            for elemento in qdeZeros:
                if (elemento == 0):
                    qdeMedValidas += 1
                    
            qdeMedRealizadas = index1
            if qdeMedValidas < n_samples and qdeMedRealizadas < qdeMaximaMedicoes:
                if corr >= min_corr:
                    print(0)
                else:
                    print(corr)
            elif qdeMedValidas >= n_samples and qdeMedRealizadas < qdeMaximaMedicoes:
                #novaMedicao = input("Ainda não há medições válidas. Carregue a próxima medição\n")
                #dataset, qde_medicoes, qde_parametros = ColetaNovaMedição(novaMedicao, dataset)
                #qdeMedRealizadas += 1
                
                #matrizCorr = GeraMatrizCorrelacoes(dataset, qde_medicoes)    
                #matrizCorrZerada = ZeraMenoresCorrelacoes(matrizCorr, min_corr, qde_medicoes)
                #qdeZeros = ListadeZeros(matrizCorrZerada, qde_medicoes)
                
                #qdeZerosTemp = qdeZeros[:]
#                 for i in range(len(qdeZeros)):
#                     if(sum(qdeZerosTemp) == 0):
#                         break
#                     else:                        
#                         indicePiorMedicao = qdeZeros.index(max(qdeZerosTemp))
#                         matrizLimpaTemp = np.delete(matrizCorrZerada, indicePiorMedicao, axis = 0)
#                         matrizLimpaTemp = np.delete(matrizLimpaTemp, indicePiorMedicao, axis = 1)
#                         qdeZerosTemp = ListadeZeros(matrizLimpaTemp, matrizLimpaTemp.shape[0])
#                     
#                 qdeMedValidas = 0    
#                 for elemento in qdeZerosTemp:
#                     if (elemento == 0):
#                         qdeMedValidas += 1
            
                if (qdeMedValidas >= n_samples):
                    print(1)
            elif qdeMedRealizadas >= qdeMaximaMedicoes:
              print('semCorrelacao')
        else:    
            print('erro')
try:         
    rm = visa.ResourceManager()
    device = rm.open_resource('TCPIP0::' + ADDRESS + '::inst0::INSTR')
    input1 = '-1'
    input2 = '-1'
    if len(os.sys.argv) > 1:
        input1 = os.sys.argv[1]
    if len(os.sys.argv) > 2:   
        input2 = os.sys.argv[2]

    if input1 == '0':
        initial_cal_and_open(device)
    elif input1 == '0.1':
        check_cal_already_saved(device)
    elif input1 == '1':
        initial_acquire_and_prompt(device,1,2)
    elif input1 == '2':
        initial_acquire_and_prompt(device,2,3)
    elif input1 == '3':
        device.write(':SENSe:CORRection:COLLect:GUIDed:STEP:ACQuire %d' % (3))   
    elif input1 == '4':
        save_cal(device)
    elif input1 == '5':
        extract_data(device)
    elif input1 == '6':
        extract_data_corr(device, input2)
        
        
    device.close()
    rm.close()
except:
    traceback.print_exc()
