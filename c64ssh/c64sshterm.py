'''
Created on Aug 2, 2015

@author: ronaldjosephdesmarais
'''

import time
import serial
import c64utils.ATPC as atpc
import subprocess,os

state=0
process=None

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=2400,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.SEVENBITS
)
try:
    ser.open()
    print "Try is Open"
    ser.isOpen()
except Exception as e:
    #ser.close()
    print "Opne serial error %s"%e
    
while 1:
    time.sleep(1)
    out =''
    while ser.inWaiting() > 0:
            b=ser.read()
            out += b
    if out != '':
        print "handling %s "%out
        if state == 0:
            print "Write Ready to C64"
            ser.write("READY\n")
            state = 1
        elif state == 1:
            print "Got response from Ready %s"%out
            if out == "OK\n":
                state = 2
            else:
                ser.write("READY\n")
        elif state == 2:
            if "ls" in out:
                print "Try to LS -al connection"
                process = subprocess.Popen(["ls","-al"],stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
                [err,out]=process.communicate()
                ser.write("%s\n"%out)
            if "exit" in out:
                state=0
                
        
                
        