'''
Created on Aug 4, 2015

@author: ronaldjosephdesmarais
'''
from c64utils import NullSerial as Serial

serial = Serial()

c1 = serial.getInterface()
c2 = serial.getInterface()


c1.write("c1 write")
c1.write("c1 hey")
c2.write("c2 write")

print "c1 reads"
print c1.read()

print "c2 reads"
print c2.read()
print c2.read()
