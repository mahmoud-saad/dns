#!/usr/bin/python


#1- script_name  zone_name
#2- will check it's  current ns and add automatically 
#3- reload the named service and make it master zone 
#4- check zone and remove first two origin 
#5- if it has 4 ns it will remove one of them
#6- it will sync the zone 

import os, sys, subprocess


zone_name = sys.argv[1]
get_ns = subprocess.Popen("dig  %s  -t ns   +noall +answer |grep NS |sort|awk '{ print $NF }'| grep ^ns[0-9] |head -n 1" %zone_name, shell=True ,stdout = subprocess.PIPE).communicate()[0].strip('\n')

def reload_named():
    subprocess.call("service named reload", shell=True)
    return
#open named.conf for read.
cfg_read   = open('/etc/named.conf', 'r+')
#open named.conf for write.
cfg_append = open('/etc/named.conf', 'a')

#check the current NSs for the domain
if get_ns == "ns3.link.net."  or get_ns == "ns4.link.net.":
    #check if zone already exists in named.conf file.
    for lines in cfg_read:
	
        if zone_name in lines:
	    print zone_name, "already exists" 
            cfg_read.close()
	    break
    # if zone is not defined at named.conf script will add new defination for it.
    else:
        cfg_append.write('zone "%s"  { \n      type slave;\n      file "/var/named/%s.db";\n       masters { 214.131.64.19; };\n };\n' % (zone_name, zone_name)) 
        print "zone '%s' added to named.conf" % zone_name
        reload_named()
	#check if zone is transferd correctly
        if os.path.exists('/var/named/%s.db' % zone_name ) :
            print "zone transfred successfuly"
        else:
            print "zone not trasfred"

elif get_ns == "ns1.link.net."  or get_ns == "ns2.link.net."  or get_ns == "ns5.link.net." : 
    #check if zone already exists in named.conf file.
    for lines in cfg_read:
        if zone_name in lines:
            print zone_name, "already exists"
            cfg_read.close()
            break
    # if zone is not defined at named.conf script will add new defination for it.
    else:
        cfg_append.write('zone "%s"  { \n      type slave;\n      file "/var/named/%s.db";\n       masters { 214.131.64.2; };\n };\n' % (zone_name, zone_name))
	print "zone '%s' added to named.conf" % zone_name
        reload_named()
        #check if zone is transferd correctly
        if os.path.exists("/var/named/%s.db" %zone_name ):
            print "zone transfred successfuly"
        else:
            print "zone not trasfred"


 

elif get_ns == "ns10.link.net."  or get_ns == "ns11.link.net." or get_ns == "ns12.link.net.":
    print "it's already on %s" %get_ns
else:
    print "we are not the autoritative for this domain" 	


