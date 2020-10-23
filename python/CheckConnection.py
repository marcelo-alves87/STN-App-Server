import visa
import time

def config(device):
    device.timeout = 5000
    device.read_termination = '\r'
    time.sleep(1)
    
##try:
##    rm = visa.ResourceManager()
##    device = rm.open_resource('TCPIP0::192.168.0.173::inst0::INSTR')
##    idn = device.query('*IDN?')
##    print(idn)
##    config(device)
##    device.close()
##    rm.close()
##except:
##    print('erro')

print('ok')
