#!/bin/python3.5

'''
This code is for Check Point R80.10 GaiaOS API testing
@author: ivohrbacek@gmail.com and LAURA
'''


from pprint import pprint
import json
from connector import Connector
import sys



def push_data(data, connect):

    """
    go through JSON data and push them to API
    """


    """
    mapping list map JSON data filed to comand for API
    """

    mapping_list = [


        {"static_routes":"add-static-route"},
        {"default_gw":"set-default-gw"},
        {"name":"set-hostname"},
        {"vlans":"/set-interface/add-vlan"},
        {"interfaces":"set-interface"},
        {"dns":"set-dns"},
        {"ntp":"set-ntp/primary"},
        {"ntp_state":"set-ntp/state"}

    ]

    # go through list of dicts and map key and value to right possitions
    for item in mapping_list:
        # map key and value - data filed in json and appropriate command for API
        for data_field, command in item.items() :
            # if JSON is empty with data - its emty list od dicts
            if not data[data_field]: 
                pass
            else:
                # get dictionaries of all static routes in JSON and push them via API
                print("")
                print ("Adding:" + data_field)
                print ("CMD is:" + command)
                print("")
                for item in data[data_field]: 
                    pprint(item)
                    pprint(connect.send_cmd(command, item)) 
                    check = True
                    print("")
                    print("")



def show_data(connect):
    """
    show commands to verify results of changes or show commands
    """
    # payloads
    payload={}
    payload_vlan={"interface":"eth1"}
    paylod_interface={"interface": "eth1.100"}
    mapping_list = [


             {"static_routes":"show-static-routes"},
             {"default_gw":"show-default-gw"},
             {"name":"show-hostname"},
             {"vlans":"show-interface/vlans"},
             {"interfaces":"show-interfaces"},
             {"dns":"show-dns"},
             {"ntp_servers":"show-ntp/servers"},
             {"ntp_current":"show-ntp/current"},
             {"ntp_state":"show-ntp/state"},
             {"interface":"show-interface"}
    ]
    
    print("")
    print ("Showing data from firewall..")
    print("")
    print("")

    for item in mapping_list:
        for data_field, command in item.items():
            # if JSON is empty with data - its emty list od dicts
            # get dictionaries of all static routes in JSON and push them via API
            print("")
            print ("Show:" + data_field)
            print("")
            print("")
            if data_field == 'vlans':
                #process_interfaces()
                pprint(connect.send_cmd(command, payload_vlan))
            elif data_field == 'interface':
                pprint(connect.send_cmd(command, paylod_interface))
            elif data_field == 'interfaces':
                pprint(connect.send_cmd(command, {}))
            else:
                pprint(connect.send_cmd(command, payload))
                print("")
                print("")




def main():

    """
    main method, definition of url and credentials, calling connector object which handle connectivity to API,
    loading JSON data and pushing those to firewall..
    """
    
    # test fw ##
    url= 'https://192.168.0.251/gaia_api/'
    
    # credentials
    payload_list_common= {
	"user":"admin",
	"password":"checkpoint123"
    }
   
    # create connector instance
    connect = Connector(url, payload_list_common)
    
    # load JSON data into dics for pushing
    
    try:
        with open('data.json') as f:
            data = json.load(f)
            # call push method to add data to firewall
            push_data(data,connect)
            # show firewall data
            show_data(connect)

            #logout
            connect.logout()
            
            

    
    except json.decoder.JSONDecodeError:

        print("You have wrong JSON data file format")


    
    
if __name__ == "__main__":
    main()