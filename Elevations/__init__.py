# Name: Elevations
# Author: Elad Salomons
# Email: selad@optiwater.com
# License: MIT

# This plugin will import junctions elevation data from Google Maps

from PyQt4.QtGui import QMessageBox
from urllib2 import Request, urlopen
import xml.etree.ElementTree as ET

plugin_name = 'Elevations'
plugin_create_menu = True
__all__ = {"Get elevations":1}

## Get your Google API key here: https://console.developers.google.com/apis/
API_KEY='GET YOUR OWN API KEY FROM GOOGLE'

number_of_coords_per_api_call = 300

def run(session=None, choice=None):
    ltopTitle = 'Elevations by Elad Salomons'

    if choice is None:
        choice = 99

    # main menus
    if choice == 1:
        txt=''
        n=0
        i=0
        junctions_list = session.project.junctions.value[:]
        for j in junctions_list:
          n=n+1
          lat=str(j.y)
          lon=str(j.x)
          txt=txt+lat + ',' + lon + '|'
          j.elevation=0
          if (n % number_of_coords_per_api_call==0) or (n==len(junctions_list)):
            txt = txt[:-1]
            request = Request('https://maps.googleapis.com/maps/api/elevation/xml?locations=' + txt + '&key=' + API_KEY)
            response = urlopen(request).read()
            tree = ET.fromstring(response)
            k=0
            for ee in tree.iter('elevation'):
              junctions_list[i+k].elevation = ee.text
              k=k+1
            i=i+number_of_coords_per_api_call
            txt=''
            print n
        QMessageBox.information(None, ltopTitle, 'Elevations imported', QMessageBox.Ok)
        pass
    elif choice == 99:
        pass
    else:
        pass


