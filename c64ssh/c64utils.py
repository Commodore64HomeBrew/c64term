'''
Created on Aug 3, 2015

@author: ronaldjosephdesmarais
'''

import types,thread,time
from threading import Condition

class Protocol(object):
    def __init__(self,rules):
        print "Protocol Init %s"%rules
        self.state=1
        #print "Try to call init function %s"%rules[self.state](self)
        rules[self.state](self)
    
    def process_message(self,msg):
        return self.rules[self.state](self,msg)
        
        

class SSHProtocol(Protocol):
    
    def __init__(self,proxy):
        print "SShProtocol %s"%self.rules
        Protocol.__init__(self,self.rules)
        self.proxy=proxy
        self.cv=Condition()
        
    def init(self):
        print "OK initialized"
        self.state=2
          
    def handle(self,msg):
        print "handle message %s"%msg
        if msg['type'] == "send":
            thread.start_new_thread(self.send, (msg,))
            
    def send(self,message):
        print "Sending Message %s"%message
        self.release()
    
    def release(self):
        self.cv.acquire()
        self.cv.notify()
        self.cv.release()
        
    def wait(self):
        self.cv.acquire()
        self.cv.wait()
        self.cv.release()
            
    rules={1:init,2:handle}
    
class SerialProxy():
    def __init__(self):
        self.protocol=SSHProtocol(self)
    
    def write(self,msg):
        msg_obj={'type':'send','message':msg}
        self.protocol.process_message(msg_obj)
        self.protocol.wait()
        
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
    
        
        
        
        
        