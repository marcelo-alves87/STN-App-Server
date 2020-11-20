import pyvisa as visa
import time

ADDRESS = '192.168.0.173'

def write_command(device, command, retry=True):
    try:
       device.write(command)
       return True
    except visa.VisaIOError:
       if(retry): 
           time.sleep(1)
           device.write('*OPC')
           write_command(device, command, False)
       else: 
           return False

def config(device):
    device.timeout = 5000
    device.read_termination = '\r'
    b = write_command(device,':INSTrument:SELect "%s"' % ('NA')) and write_command(device,':SENSe:FREQuency:STOP %G' % (1000000000.0)) and write_command(device,':SENSe:FREQuency:STARt %G' % (2000000.0)) and write_command(device,':SENSe:SWEep:POINts %d' % (1001)) and write_command(device,':FORMat:DATA %s,%d' % ('REAL', 64)) and write_command(device,':SENSe:CORRection:COLLect:CONNector %d,"%s"' % (1, 'Type-N -F-,50')) and write_command(device, ':SENSe:CORRection:COLLect:CKIT:LABel %d,"%s"' % (1, '85032F')) and write_command(device,':SENSe:CORRection:COLLect:METHod:SOLT1 %s' % ('1'))
    time.sleep(1)
    return b
    
try:
    rm = visa.ResourceManager()
    device = rm.open_resource('TCPIP0::' + ADDRESS + '::inst0::INSTR')
    idn = device.query('*IDN?')
    print(idn)
    config(device)
    device.close()
    rm.close()
except:
    print('erro')

# rm = visa.ResourceManager()
# device = rm.open_resource('TCPIP0::169.254.120.255::inst0::INSTR')
# 
# idn = device.query('*IDN?')
# print(idn)
# #config(device)
# device.close()
# rm.close()

