'''
Created on Aug 3, 2015

@author: ronaldjosephdesmarais
'''

import types
class Protocol(object):
    def __init__(self,rules):
        print "Protocol Init %s"%rules
        self.state=0
        self.rules=rules
    
    def process_message(self,msg):
        return self.rules[self.state](msg)
        

class SSHProtocol(Protocol):
    
    def __init__(self):
        #rules={1:"init",2:"ready"}
        print "SShProtocol %s"%self.rules
        Protocol.__init__(self,self.rules)
        
    def init(self,msg):
        print "init got %s"%msg
        self.state=2
        return "OK initialized"
    
    def ready(self,msg):
        print "Read got %s"%msg
        self.state=1
        return "OK Ready"
    
    rules={1:init,2:ready}
    
class SerialProxy():
    def __init__(self):
        self.protocol=SSHProtocol()
    
    def write(self,msg):
        self.write_proxy(msg)
        
    def read(self):
        return self.read_proxy()
        
class NullSerial():
    c1=None
    c2=None
    
    def __init__(self):
        self.inqueue=[]
        self.outqueue=[]
        #return self.getInterface()
    
    def getInterface(self):
        if self.c1 is None:
            #self.c1=SerialInterface()
            self.c1=SerialProxy()
            self.c1.write_proxy=types.MethodType(self.in_q_enq,self.c1)
            self.c1.read_proxy=types.MethodType(self.out_q_deq,self.c1)
            return self.c1
        if self.c2 is None:
            self.c2=SerialProxy()
            self.c2.write=types.MethodType(self.out_q_enq,self.c2)
            self.c2.read=types.MethodType(self.in_q_deq,self.c2)
            return self.c2
            
    def in_q_enq(self,client,msg):
        print "written %s"%msg  
        self.inqueue.insert(0,msg)
        
    def in_q_deq(self,client):
        return self.inqueue.pop()
             
    def out_q_enq(self,client,msg):
        print "written %s"%msg  
        self.outqueue.insert(0,msg)
        
    def out_q_deq(self,client):
        return self.outqueue.pop()
    
        
        
        
        
        