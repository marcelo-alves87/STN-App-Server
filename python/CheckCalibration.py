import visa
import time
import os.path

if(os.path.isfile(os.path.abspath('./python/calstatus.txt')) and  os.path.abspath('./python/CEXP.sta')):
     file = open(os.path.abspath('./python/calstatus.txt'),'r') 
     data = file.read()
     print(data)
     file.close()
else:
    print('erro')



