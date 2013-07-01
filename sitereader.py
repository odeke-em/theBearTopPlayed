#!/usr/bin/python3
#Author: Emmanuel Odeke <odeke@ualberta.ca>

import urllib.request
import re
import urllib.error

UBUNTU_UAGENT ='Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:13.0) Gecko/20100101 Firefox/13.0'

def site_opener( url,
		stderr,
		errorVerbosity, 
		user_agent=UBUNTU_UAGENT
		):
	#Our modified opener to enable the use of a fake user-agent
	modified_opener	 = urllib.request.build_opener()
	user_agent_tuple = ('user-agent',user_agent)
	modified_opener.addheaders = [user_agent_tuple]

	try:
		data = modified_opener.open(url)

	except Exception as e:
		if isinstance( e, urllib.error.URLError ):
			if ( errorVerbosity ):
				stderr.write( "URLError instance found on: %s\n"%( url ))
				stderr.flush()
		return None


	outdata = data.read()

	try:
		decoded_data = outdata.decode()
	except Exception as e:
		#Manage error later#
		if ( errorVerbosity ):
			stderr.write( "Decoding error: errorBelow: %s\n"%( e ))
			stderr.flush()
		return None

	return decoded_data
