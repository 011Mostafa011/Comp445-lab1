import socket
import json
import sys
import datetime 
from sys import argv



d = datetime.datetime.now()

class HTTPmessage:
    def __init__(self,request):
        self.CRLF= "\r\n\r\n"
        self.request_line = request
        # self.generalHeader = d.strftime('%c')
        self.requestHeader = {"Host":'',"User-Agent":"Mozilla/5.0"}    
        self.entityHeader  = None
        self.entityBody = None
        self.message = ""
        
        
    def setHost(self,host,port):
        self.requestHeader['Host'] = host + ':'+ str(port)
    
    def setEntityHeader(self,header):
        self.entityHeader = header
    
    def setEntityBody(self,data):
        self.entityBody = data 

        
    def buildMessage(self): 
        message = []
        message.append(str(self.request_line))
        for i in self.requestHeader:
            message.append(str(i+':'+self.requestHeader[i]+'\n'))

        if self.entityHeader is not None:   
            message.append(str(self.entityHeader))
        
        if self.entityBody is not None:
            message.append(str(self.entityBody))

        for i in  message:
            self.message += i

        self.message += self.CRLF
        return self.message.encode('utf-8')

class HTTPClient:
    def __init__(self,options, url):
        
        self.options = options
        
        if len(url.split(':')) > 1:
            self.host = url.split(':')[0]
            self.url = url.split(':')[1]
            self.port = url.split('/')[0]
            self.uri = '/'.join(url.split('/')[1:])
        
        else:
            self.port = 80
            self.host = url.split('/')[0]
            self.uri = '/'+url.split('/')[1]

        
        self.message = None
        

    def getHTTP(self):
        request_line = str.upper('get') +' '+self.uri+ ' '+ 'HTTP/1.0\n'
        #build message steps
        message = HTTPmessage(request_line)
        message.setHost(self.host,self.port)
        message.setEntityHeader(self.options.header)
        self.message= message.buildMessage()

    def postHTTP(self):
        request_line = str.upper('post') +' '+self.uri+ ' '+ 'HTTP/1.0\n'
        message = HTTPmessage(request_line)
        message.setHost(self.host,self.port)
        message.setEntityHeader(self.options.header)
        message.setEntityBody(self.options.data)
        
        self.message= message.buildMessage()

    def run_client(self):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            conn.connect((self.host,self.port))

            conn.sendall(self.message)
            # MSG_WAITALL waits for full request or error
            data =[]
            while True:
                response = conn.recv(4080, socket.MSG_WAITALL)
                if not response:
                    break

                data.append(response)

            sys.stdout.write("Replied: ")
            if self.options.verbose is True:
                for i in range(len(data)):
                    sys.stdout.write(data[i].decode('utf-8'))
                else:
                    for i in range(len(data)-1):
                        sys.stdout.write(data[i+1].decode('utf-8'))
                
        finally:
            conn.close()
