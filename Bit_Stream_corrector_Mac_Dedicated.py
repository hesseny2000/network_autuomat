import telnetlib
import sys
import time
import re

#####################################################################################################
############ if you need to use a user respond, i will disabled when Script runs via Matrix    ######
############ Script written by : Mohamed hosseny 2016                                          ######
#####################################################################################################
#command1 = "service-port vlan 455"
#command1 = ("undo service-port port %s \n" %port )
HOST = raw_input("Enter Host IP:")
user = raw_input("Enter userName:")
password = raw_input("Enter password:")
port = raw_input("Enter port look like 1/1/1 :")
#####################################################################################################
 
#------Telne&login with kowning Data-------#
#HOST = "MSAN-M01H-CA-EG"
#user = "user"
#password = "password"
#port = "0/15/0"

#####################################################################################################

command = "enable \n config \n"
tn = telnetlib.Telnet(HOST)
tn.read_until("name:",5)
tn.write(user)
if password:
    tn.read_until("sword:",5)
    tn.write(password)
    tn.write(password.encode('ascii') + b"\n")
    #incase we found the MSAN cabinets Hostname end by E NOT EG
    tn.read_until(">",5)
    tn.write(command)
    tn.write("\n \n")
    tn.read_until("Command:",10)
    ##Check out if there is a  mac-address OR not##
tn.write("display mac-address port  %s \n" %port)
tn.write("\n \n")
mac_out=tn.read_until(")#",10)
#print mac_out
no_mac="Failure:"
if no_mac in mac_out:
    print ("There is no MAC address Found")
else:
    tn.write("\n")
    tn.write("display mac-address port  %s \n" %port)
    tn.write("\n \n")
    tn.read_until("dl ",10)
    mac_show = tn.read_until("dynamic",5)
    print ("MAC-address is found : \n %s " %mac_show[1:16])

## check the Stacking vlan ##
tn.write("display current-configuration section vlan-config | include vlan attrib 4\n")
tn.read_until("\n vlan attrib ",5)
out1=tn.read_until("stacking",5)
out1 = out1[0:3]
service = "inner-vlan"##
##check the configuration under port
out = tn.write("display current-configuration section bbs-config | include %s v\n" %port)
tn.read_until("service-port ",10)
out=tn.read_until("outbound",10)
#check if there is a configuration or not#
if service in out :
    print ("the port configured with Vlan: %s " %out[9:13])
    print ("the  stacking Vlan is : %s " %out1)
    undo = ("undo service-port %s \n " %out[0:4])
    set_vlan = "service-port %s vlan  " %out[0:4]+ out1 + " " + out[14:] + " " + "traffic-table index 6" + "\n"
    set_vlan1= set_vlan.replace("\r"+"\n",'')
    time.sleep(5)
    if out1 in out :
        print ("there is no Problem as the configured vlan on port is Correct: %s "%out1)
        tn.close()
    else:
        tn.write(undo)
        time.sleep(5)
        tn.write(set_vlan1)
        tn.write("\n \n")
        print ("Vlan has been changed from %s " %out[9:13]) + ("to vlan %s"%out1)
        tn.write("\n \n")
        tn.close()
else :
    print ("port not configured ")

tn.close()
