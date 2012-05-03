'''
Modified from example

v1.0
@author: @rifti

requirements:
1. python 2.6
2. zabbix api https://github.com/gescheit/scripts
3. the `username` privilege set in Zabbix web GUI (find it in menu:
   Administration->Users->API access)
   i.e. set to username=admin in below
   
usage:

Change server, user_name, and password definition and then:
# python zabbix_event_print_example.py <optional trigger ID>
i.e.
# python zabbix_event_print_example.py 13027
or
# python zabbix_event_print_example.py

trigger ID can be checked from each individual host Trigger list
(in Zabbix web GUI menu: Configuration->Host->Trigger(in the relevant host column)) 

for debugging change log_level to 6 to see JSON RPC conversation

notes:
I already tried to combine `triggerids` with other i.e. `value`,
`acknowledged` but it only works alone

You can't get some event with specific trigger with certain PROBLEM/OK
status and/or acknowledgement status 
'''

import sys
from zabbix_api import ZabbixAPI

try:
	triggerID=sys.argv[1]
except:
	triggerID=0

server="http://127.0.0.1/"
username="admin"
password="somepassword"

# zabbix api with log_level=0
zapi = ZabbixAPI(server=server, path="", log_level=0)
zapi.login(username, password)

# get acknowledged events
ack_events=zapi.event.get({"acknowledged":[1]})

# get events with status PROBLEM
problem_events=zapi.event.get({"value":[1]})

# get the first acknowledged events with status PROBLEM
try:
	eventid=zapi.event.get({"acknowledged":[1],"value":[1]})[0]["eventid"]
except:
	# no event with such filter found:
	eventid=0
	
print '\nAcknowleged'
print ack_events

print '\nEvent ID of the 1st Acknowledged event with status=PROBLEM'
print eventid

print '\nEvent with status=PROBLEM'
print problem_events

if triggerID>0:
	events_with_triggerid=zapi.event.get({"triggerids":[triggerID]})
	print '\nEvent with Trigger %s' % triggerID 
	print events_with_triggerid
