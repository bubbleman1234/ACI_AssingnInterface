import config
import xml.etree.ElementTree as ET
import Readfile
from pyaci import *
from termcolor import *
from Readfile import ReadData as ReadData
from colorama import Fore, Back, Style

def CreatePathConfig(pod, nodeA, nodeB, eth, vpc):
    #Check ETH Port
    if vpc == "" and eth != "":
        path = "topology/pod-" + str(pod) + "/paths-" + str(nodeA) + "/pathep-[eth" + eth + "]"
    #Check VPC Port
    elif vpc != "" and eth == "" and nodeB != "":
        path = "topology/pod-"+ str(pod) + "/protpaths-" + str(nodeA) + "-" + str(nodeB) + "/pathep-" + vpc
    else:
        path = "Invalid Path"
    return path

def SendConfigToAPIC(select_method, apic, configport):
    for value in configport:
        list_epg = Readfile.ReadEPG()
        vlan_list = value["VLAN"].split(",")

        for i in vlan_list:
            for j in list_epg:
                if j["Vlan"] == i:
                    tenant = j["Tenant"]
                    appprofile = j["AppProfile"]
                    epg = j["EPG Name"]
                    vlan = "vlan-" + str(j["Vlan"])
                    tDn = CreatePathConfig(value["POD"], value["nodeID_A"], value["nodeID_B"], value["Interface_ETH"], value["Interface_VPC"])
                    commit_config = apic.mit.polUni().fvTenant(tenant).fvAp(appprofile).fvAEPg(epg).fvRsPathAtt(encap=vlan, instrImedcy="immediate", tDn=tDn, status=select_method)

                    try:
                        result = commit_config.POST(format='xml')
                        print("Status Code: " + colored(str(result.status_code),
                                                        "green") + "\tMethod: " + select_method.upper())
                        print("Detail: " + "(Tenant) ===> " + colored(tenant, "yellow") + "\t(EPG) ===> " + colored(epg,"blue") + "\t(Path) ===> " + tDn)
                        print("---------------------------------")
                    except pyaci.errors.RestError as e:
                        parse = (ET.fromstring(str(e))).find('./error')
                        status = parse.attrib['code']
                        error = ((parse.attrib['text']).split("; "))[1]
                        print("Status code: " + colored(status,"red") + "\tMethod: " + select_method.upper() + "\nDetail: " + error)
                        print("---------------------------------")
                        continue

def LoginACI():
    apic = Node(config.apicserver)
    try:
        print("Loging in APIC Server: " + config.apicserver)
        response = apic.methods.Login(config.username, config.password).POST()
        return apic
    except Exception as e: #apic.methods.Login.POST().exceptions.ConnectionError as e:
        print(colored("Failed to Login!!!","red") + "\nReason: " + str(e))
        return "error"

if __name__ == '__main__':
    apic = LoginACI()
    if apic != "error":
        print(colored("Login Successful!!!","green"))
        while True:
            select_method = input("Select type of method (CREATED or DELETED): ")
            if select_method.upper() == "CREATED" or select_method.upper() == "C":
                method = "created"
                break
            elif select_method.upper() == "DELETED" or select_method.upper() == "D":
                method = "deleted"
                break
            else:
                print("Invalid input")
        configport = ReadData()
        SendConfigToAPIC(method, apic, configport)
    else:
        print("***** Cannot Connect APIC *****")