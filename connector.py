from pprint import pprint
import json
import requests
import urllib3
import sys

class Connector():

    
       
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def __init__(self, url, payload):


        self.sid=""
        #self.task = ""

        # default header without SID
        self.headers_default = {
             'content-type': "application/json",
              'Accept': "*/*",
             }
        # headers for usage in instance methods - with self.SID     - will be filled up in constructor
        self.headers = {}
        self.url=url
        self.payload_list = payload # default only username and passowrd
        try:
             self.response = requests.post(self.url+"login", json=self.payload_list, headers=self.headers_default, verify=False) # verify=False - will work without ssl certificate
             
             if self.response.status_code == 200:
                 sid_out=json.loads(self.response.text)
                 #print sid_out
                 self.sid = sid_out['sid']
                 self.headers = {
                        'content-type': "application/json",
                        'Accept': "*/*",
                        'x-chkp-sid': self.sid,
                 }
                 print("")
                 print("")
                 print ("Connection to gateway is okay..")
                 print("")
                 print("")
                 

             else:
                 print("")
                 print("")
                 print ("There is no SID, connection problem to gateway")
                 print("")
                 print("")
                 print (self.response.status_code)
                 sys.exit(1)

        except requests.exceptions.RequestException:
            print("")
            print("")         
            print ("can not connect to server for some reason, check connectivity or ssl certificates!!!")
            print("")
            print("")
            print (self.response.status_code)
            sys.exit(1)
    

    def logout(self):
        # avoid connectovity interruption - thats why try except here
        done=False
        while not done:
            try:
                payload_list={}
                self.response = requests.post(self.url+"logout", json=payload_list, headers=self.headers, verify=False)
                print ("logout from gw is okay..")
                return self.response
            except:
                print ("connection to gw broken, trying again")
            else:
                done=True
        
        

    def send_cmd(self, cmd, payload):
        # avoid connectovity interruption - thats why try except here
        done=False
        while not done:
            try:
                payload_list=payload
                print (self.url + cmd)
                print (payload_list)
                self.response = requests.post(self.url + cmd, json=payload_list, headers=self.headers, verify=False)
                #pprint (self.response.json())
                #print (self.response.status_code)
                return self.response.json()
            except:
                print ("connection to mgmt server broken, trying again")
            else:
                done=True