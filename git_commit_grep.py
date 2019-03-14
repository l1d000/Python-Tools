#!/usr/bin/python
# coding:utf-8
import csv
import os
import sys
import xml.dom.minidom as xmldom



def get_data(path, commit_grep, keyword):
    path = path+'/'+commit_grep
    final = []
    output=os.popen(' cd %s ;git log --author=htc  --pretty=format:"%%s == %%ae == %%H == %%cd"'%(path)).read().splitlines() 
#    output=os.popen(' cd %s ;git log --pretty=format:"%%s = %%ae = %%H = %%cd"'%(path)).read().splitlines()
    for item_list in output:
        temp = []
        item=item_list.split('==')
        for n in item:
            temp.append(n)

        for item in temp:
            if keyword in item:
                 temp.insert(0,commit_grep)
                 final.append(temp)
                 print("temp:"+item) 
                 break;
        
    return final

	

def write_data_html(data, name, path ):
    file_name = name+".html"
    f = open(file_name,'w')
    message ="""
             <html>
             <body>
             <font size="10" color="#008000">Keywords</font>
             <font size="4" color="#008000">("""+path+""")</font></br></br>
             <table border="1" cellspacing="0">
             <tr bgcolor="#008000">
             <th>Index</th>
             <th>Path</th>
             <th>Title</th>
             <th>Author</th>
             </tr>
	     <font size="5" color="#FF0000">Grep '"""+name +"""' Total: """+bytes(len(data))+"""</font>"""
    
    for index, n in enumerate(data):
        message = message+"""<tr>"""
        message = message+"""<td style="padding-right:20px">"""+str(index)+"""</td>"""   
        message = message+"""<td style="padding-right:20px">"""+n[0]+"""</td><td style="padding-right:20px">"""+n[1]+""" """+"""</td>"""
        message = message+"""<td style="padding-right:20px">"""+n[2]+"""</td>"""
        message = message+"""</tr>"""

    message = message+"""</table>
             </br></br>
             <div style="float:right;">
             <font size="4 style="padding-right:20px" color="#008000">HTC SSD BT</font>
             </div>
             </body>
             </html>"""
    f.write(message)
    f.close()


def commit_grep (path, keyword):
    result = []
    xmlfilepath = os.path.abspath(path+'/.repo/manifest.xml')
    domobj = xmldom.parse(xmlfilepath)
    elementobj = domobj.documentElement
    subElementObj = elementobj.getElementsByTagName("project")
    for item in subElementObj:
        commit_grep = item.getAttribute("path")
        temp_list = get_data(path, commit_grep, keyword)
        for temp in temp_list:
            result.append(temp)
    write_data_html(result, keyword, path)
 

if __name__ == '__main__':
        print("Path:")
        print(sys.argv[1])
        print("keyword:")
        print(sys.argv[2])
        commit_grep(sys.argv[1], sys.argv[2])
