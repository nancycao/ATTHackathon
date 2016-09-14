#!/usr/bin/python
import re
import requests
import sys
import cgi
import cgitb
cgitb.enable()
reload(sys)
sys.setdefaultencoding('utf-8')

def FStoD():
    '''
        Converts cgi.FieldStorage() return value into a standard dictionary
        '''
    d = {}
    formData = cgi.FieldStorage()
    for k in formData.keys():
        d[k] = formData[k].value
    return d

d = {'txt01':'brooklyn', 'txt02':'next_week'}


city = "&venue.city=" + d['txt01']
time = "&start_date.keyword=" + d['txt02']
response = requests.get(
                        "https://www.eventbriteapi.com/v3/events/search/?sort_by=date&categories=110" + city + time,
                        headers = {
                        "Authorization": "Bearer BV442UWQUREICGJW7V2A",
                        },
                        verify = True,  # Verify SSL certificate
                        )

def genList():
    L = []
    for e in response.json()["events"]:
        entry = []
        line = str(e["description"]["text"])
        match = re.findall(r'[\w\.-]+@[\w\.-]+', line)
        #for i in match:
        #    print i
        url = e["url"]
        date = e["start"]["local"]
        if match == []:
            match = ["Go to URL"]
        entry.append(date)
        entry.append(e["name"]["html"].decode('utf-8').encode('utf-8')) #title
        entry.append(e["description"]["text"])
        entry.append(match) #email
        entry.append(url)
        L.append(entry)
    return L

mid = "<table style='width:75%'>"
mid += '''
    <tr>
    <th>Date</th>
    <th>Event Name</th>
    <th>Description</th>
    <th>Organizer Email</th>
    <th>Event URL</th>
    </tr>
    '''

for i in genList():
    mid += "<tr>"
    mid += "<td>" + str(i[0]) + "</td>"
    mid += "<td>" + str(i[1]) + "</td>"
    mid += "<td>" + str(i[2]) + "</td>"
    mid += "<td>" + str(i[3][0]) + "</td>"
    mid += "<td>" + "<a href='" + str(i[4]) + "'>link</a>" + "</td>"
    mid += "</tr>"
mid += "</table>"

# ======= Must be beginning of HTML string ========
htmlStr = "Content-Type: text/html\n\n" #NOTE there are 2 '\n's !!!
htmlStr += '''<html><head> <style>
    th, td {
    padding: 15px;
    text-align: left;
    }
    th {
    text-align: left;
    }
    table {
    border-collapse: collapse;
    }

    table, th, td {
    border: 1px solid black;
    }
    </style><title> INSERT TITLE HERE </title></head></html>\n'''
htmlStr += "<body> <center>"

# ~~~~~~~~~~~~~ HTML-generating code ~~~~~~~~~~~~~~
htmlStr += str( FStoD() )
htmlStr += "<button type='button'> Email all </button>"
htmlStr += str(d['txt01'])
htmlStr += str(d['txt02'])
htmlStr += mid

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

htmlStr += '''
</center> </body></html>'''


print htmlStr
