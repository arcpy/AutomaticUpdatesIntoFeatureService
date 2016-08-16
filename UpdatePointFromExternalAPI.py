"""
  This script updates a hosted feature service in ArcGIS.com (or a local Portal) from a 3rd party API or web service.
  An update is performed on the point at a given interval.
  Required inputs:
    +  URL to a Feature Service
    +  Username / password with administrator  rights for the feature service

  Doc Reference:  http://resources.arcgis.com/en/help/arcgis-rest-api/index.html#/Update_Features/02r3000000zt000000/
  Blog Reference: http://
"""

import urllib
import urllib2
import json
import sys
import time

# Credentials and feature service information
username = "    "
password = "     "    
service = "issLocation" 

# Note - the URL ends with "FeatureServer". The code below handles the /0 or /n for a given layer within the service
fsURL = "http://services1.arcgis.com/....."  # Example: fsURL = "http://services1.arcgis.com/aaa123/arcgis/rest/services/issLocation/FeatureServer"

# Service URL to get updates from
ISSURL = "http://api.open-notify.org/iss-now.json"

# How long to wait before updating again
pauseTime = 300  # 300 seconds = 5minutes

class AGOLHandler(object):    
    """
    ArcGIS Online handler class.
      -Generates and keeps tokens
      -template JSON feature objects for point
    """
    
    def __init__(self, username, password, serviceName):
        self.username = username
        self.password = password
        self.serviceName = serviceName
        self.token, self.http, self.expires= self.getToken(username, password)  

    def getToken(self, username, password, exp=60):  # expires in 60minutes
        """Generates a token."""
        referer = "http://www.arcgis.com/"
        query_dict = {'username': username,
                      'password': password,
                      'referer': referer}

        query_string = urllib.urlencode(query_dict)
        url = "https://www.arcgis.com/sharing/rest/generateToken"
        token = json.loads(urllib.urlopen(url + "?f=json", query_string).read())

        if "token" not in token:
            print(token['error'])
            sys.exit(1)
        else:
            httpPrefix = "http://www.arcgis.com/sharing/rest"
            if token['ssl'] is True:
                httpPrefix = "https://www.arcgis.com/sharing/rest"
            return token['token'], httpPrefix, token['expires'] 
        
        
    def jsonPoint(self, X, Y, ptTime):
        """Customized JSON point object for ISS schema"""
        return {
            "attributes": {
                "OBJECTID": 1,
                "TextDate": time.strftime('%m/%d/%Y %H:%MZ', time.gmtime(ptTime)),
                "Long": X,
                "Lat": Y
            },
            "geometry": {
                "x": X,
                "y": Y
            }
        }


def send_AGOL_Request(URL, query_dict, returnType=False):
    """
    Helper function which takes a URL and a dictionary and sends the request.
    returnType values = 
         False : make sure the geometry was updated properly
         "JSON" : simply return the raw response from the request, it will be parsed by the calling function
         else (number) : a numeric value will be used to ensure that number of features exist in the response JSON
    """
    
    query_string = urllib.urlencode(query_dict)

    jsonResponse = urllib.urlopen(URL, urllib.urlencode(query_dict))
    jsonOutput = json.loads(jsonResponse.read())
    
    if returnType == "JSON":
        return jsonOutput
    
    if not returnType:
        if "updateResults" in jsonOutput:
            try:            
                for updateItem in jsonOutput['updateResults']:                    
                    if updateItem['success'] is True:
                        print("request submitted successfully")
            except:
                print("Error: {0}".format(jsonOutput))
                return False
            
    else:  # Check that the proper number of features exist in a layer
        if len(jsonOutput['features']) != returnType:
            print("FS layer needs seed values")
            return False
            
    return True


def fillEmptyGeo(con, fsURL):
    """
    This function queries the service layer end points to ensure there is geometry as the
    script does an update on existing geometry.
    If there are no features, a dummy point is entered.
    """
        
    ptURL = fsURL + "/0/query"
    
    query_dict = {
        "f": "json",
        "where": "1=1",
        "token": con.token
    }

    # Check 1 point exists in the point layer (0), if not, add a value
    if (send_AGOL_Request(ptURL, query_dict, 1)) is False:
        
        ptGeoURL = fsURL + "/0/addFeatures"
        ptData = {
            "features": con.jsonPoint(0, 0, 1000000000),
            "f": "json",
            "token": con.token
        }
        
        if send_AGOL_Request(ptGeoURL, ptData):
            print("Inserted dummy point")
            
    return


def updatePoint(con, ptURL, X, Y, ptTime):
    """Use a URL and X/Y values to update an existing point."""
 
    try:
        # Always updates point #1.
        submitData = {
            "features": con.jsonPoint(X, Y, ptTime),
            "f": "json",
            "token": con.token
        }
        
        jUpdate = send_AGOL_Request(ptURL, submitData)          
  
    except:
        print("couldn't update point")

    return


if __name__ == "__main__": 

    # Initialize the AGOLHandler for token and feature service JSON templates
    con = AGOLHandler(username, password, service)
    
    try:
        
        # Check the Feature Service for the required layer and they have at least 1 point
        # This call can be removed if you're certain the layer exists with a point
        fillEmptyGeo(con, fsURL)       
        
        # Loop indefinitely  
        while True:
            
            # Get the current ISS location and read into memory
            req = urllib2.Request(ISSURL)
            response = urllib2.urlopen(req)
            
            issPoint = json.loads(response.read())  
            Y = issPoint['iss_position']['latitude']
            X = issPoint['iss_position']['longitude']
            ptTime = issPoint['timestamp']                 
           
            if ((con.expires / 1000) - 61) < int(time.time()):  # 60secs before token expires, get a new one
                con.getToken(username, password)
    
            # Update IIS location
            updatePoint(con, fsURL + "/0/updateFeatures", X, Y, ptTime)          
           
            time.sleep(pauseTime) 
                
            
    # Generic exception handling: simple message is printed to the screen so the script continues to run.
    # Additionally, an email or other action could be implemented below.
    except Exception as e:
        print("ERROR caught:  {0}".format(e))
