from twilio.rest import Client
import sys, warnings
import deepsecurity
from deepsecurity.rest import ApiException
from pprint import pprint
import os
import csv
from datetime import datetime
from datetime import timedelta 
print (datetime.now() + timedelta(days=1,minutes=5))

listoutput = ''
header = ["COMPUTER NAME","STATUS","PLATFORM","POLICY"]
header = str(header).replace('[', '')
header = header.replace("'", '')
header = header.replace("]", '')

account_sid = 'TWILIO SID'
auth_token = 'TWILIO TOKEN'
client = Client(account_sid, auth_token)

# Setup
if not sys.warnoptions:
	warnings.simplefilter("ignore")
configuration = deepsecurity.Configuration()
configuration.host = 'https://cloudone.trendmicro.com/api'

# Authentication
configuration.api_key['api-secret-key'] = 'API KEY'

# Initialization
# Set Any Required Values
api_instance = deepsecurity.ComputersApi(deepsecurity.ApiClient(configuration))
api_version = 'VERSION'
expand_options = deepsecurity.Expand()
expand_options.add(expand_options.none)
expand = expand_options.list()
overrides = False

try:
	file1 = open("csvfile.csv", "w") 
	api_response = api_instance.list_computers(api_version, expand=expand, overrides=overrides)
	
	file1.write(str(header) + "\n")
	for computer in api_response.computers:
		#computer.platform = "CloudOne"		#hardcoded because API not working
		output = str(computer.display_name) + ', ' + str(computer.computer_status) + ', ' + str(computer.platform) + ', '  + str(computer.policy_id)
		pprint(output)
		listoutput = listoutput + output
		file1.write(output + "\n")
	file1.close() 
except ApiException as e:
	print("An exception occurred when calling ComputersApi.list_computers: %s\n" % e)

message = client.messages \
                .create(
                     body="Message from TrendMicro" + listoutput,
				
                	 from_='TWILIO NUMBER',
                     to='MOBILE NUMBER'
                 )

print(message.sid)
