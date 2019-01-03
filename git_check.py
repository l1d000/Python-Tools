#!/usr/bin/python
# coding:utf-8
import xml.dom.minidom as xmldom
import csv
import os
import sys

final_git_list = [
    'sss',
    'sss',
    'sss',
    'sss']

final_manifest_list = [
    'sss.xml',
    'sss.xml',
    'sss.xml',
    'sss.xml'
    ]


def get_data(path, git_list):
    final = []
    manifests_subElementObj = []
    if os.path.exists(path+'/.repo/manifests/'):
        for manifest in final_manifest_list:
            if os.path.exists(path+'/.repo/manifests/'+manifest):
                xmlfilepath = os.path.abspath(path+'/.repo/manifests/'+manifest)
                domobj = xmldom.parse(xmlfilepath)
                elementobj = domobj.documentElement
                subElementObj = elementobj.getElementsByTagName("project")
                manifests_subElementObj.append(subElementObj)
  
        for git in git_list:
            temp = []
            temp.append(git)
            for subElementObj in manifests_subElementObj :
                git_name = ""
                for item in subElementObj:
                    if item.getAttribute("name") == git :                        
                        git_name = item.getAttribute("revision")
                if git_name:
                    temp.append(git_name)  
                else:
                    temp.append("N/A")     
            final.append(temp)                          
    else:
         print("Path "+path+" Not Exist")     
    return final


def write_data_html(data_list, name, path):
    file_name = name+"/codebase.html"
    print (file_name)
    f = open(file_name,'w')
    message ="""
             <html>
             <body>
             <font size="10" color="#008000">Bluetooth Codebase git & branch</font>
             </br></br>
             <table border="1" cellspacing="0">
             <tr bgcolor="#008000">
             <th>Git</th>"""
    for manifest in final_manifest_list:
         message = message+ """<th bgcolor="#EE9A00">"""+manifest+"""</th>"""
	   
    for data in data_list:
        message = message+"""</tr><tr>"""
        for n in data:
            message = message+"""<td style="padding-right:20px">"""+n+"""</td>"""
        message = message+"""</tr>"""

    message = message+"""</table>
             </br></br>
             <div style="float:right;">
             <font size="4 style="padding-right:20px" color="#008000">SSD</font>
             </div>
             </body>
             </html>"""
    f.write(message)
    f.close()
                 
if __name__ == '__main__':
        if len(sys.argv) > 1:
            result = get_data(sys.argv[1], final_git_list)
            if result:
                write_data_html(result, os.getcwd() , sys.argv[1])
        else:
            print("Please input: ./git_check.py codebase path")   
