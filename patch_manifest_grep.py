#!/usr/bin/python
# coding:utf-8
import csv
import os
import sys
import xml.dom.minidom as xmldom

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')


def get_data(path):
    final = []

    output=os.popen(' cd %s ;git log --author=x-thinks --pretty=format:"%%s == %%ae == %%H == %%cd"'%(path)).read().splitlines()
    for item_list in output:
        temp = []
        item=item_list.split('==')
        for n in item:
            if n:
                temp.append(n)
            else: 
                temp.append("N\A")   
        final.append(temp)
      
    return final

	

def write_data_html(data_list, name, path):
    file_name = name+".html"
    print(path)
    print(name)
    f = open(file_name,'w')
    message ="""
             <html>
             <body>
             <font size="10" color="#008000">Patch</font>
             <font size="4" color="#008000">("""+path+""")</font></br></br>
             <table border="1" cellspacing="0">
             <tr bgcolor="#008000">
             <th>Index</th>
             <th>Title</th>
             <th>Author</th>
             <th>Commit ID</th>
             <th>Date</th>
             </tr>
	     <font size="5" color="#FF0000">Total: """+bytes(len(data_list))+"""</font>"""
    for index, data in enumerate(data_list):
        message = message+"""<tr>"""
        message = message+"""<td style="padding-right:20px">"""+str(index)+"""</td>"""
        print(path)
        print(data)
#        message = message+"""<td style="padding-right:20px">"""+n[0]+"""</td><td style="padding-right:20px">"""+n[1]+""" """+"""</td>"""
#        message = message+"""<td style="padding-right:20px">"""+n[2]+"""</td><td style="padding-right:20px">"""+n[3]+""" """+"""</td>"""
        for n in data:
            message = message+"""<td style="padding-right:20px">"""+n+"""</td>"""
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

def wirte_summary_html(data_list, name, path):
    file_name = name+".html"
    f = open(file_name,'w')
    message ="""
             <html>
             <body>
             <font size="10" color="#008000">review Codebase</font>
             </br></br>
             <table border="1" cellspacing="0">
             <tr bgcolor="#008000">
             <th>Git</th>"""
    message = message+ """<th align="left" bgcolor="#EE9A00">"""+"Path"+"""</th>"""
    message = message+ """<th align="left" bgcolor="#EE9A00">"""+"Branch"+"""</th>"""
    message = message+ """<th align="left" bgcolor="#EE9A00">"""+"Patches"+"""</th>"""
    message = message+ """<th align="left" bgcolor="#EE9A00">"""+"Link"+"""</th>"""
    for data in data_list:
        message = message+"""</tr><tr>"""
        for n in data:
            if ".html" in n:
                message = message+"""<td style="padding-right:20px">"""+"""<p><a href=" """+n+""" ">"""+n.split('/')[-1]+"""</a></p>"""+"""</td>"""
            else:
                message = message+"""<td style="padding-right:20px">"""+n+"""</td>"""
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

def review_git(path):
    data_list = []

    xmlfilepath = os.path.abspath(path+'/.repo/manifest.xml')
    path = path+'/'
    domobj = xmldom.parse(xmlfilepath)
    elementobj = domobj.documentElement
    subElementObj = elementobj.getElementsByTagName("default")

    default_review_branch = "" 
    for item in subElementObj: 
        default_review_branch = item.getAttribute("revision")

    subElementObj = elementobj.getElementsByTagName("project")
    for item in subElementObj: 
        review_path ="" 
        review_link = "" 
        git = ""
        temp = []   
        git = item.getAttribute("name")                  
        review_path = item.getAttribute("path")
        review_branch = item.getAttribute("revision")
        father_path = os.path.dirname(path.rstrip('/'))

        if review_path :
             result = get_data(path+review_path)
             html_name = father_path+'/Review/Detail_Links/review_'+(path+review_path).split('/')[-3]+'_'+(path+review_path).split('/')[-2]+'_'+(path+review_path).split('/')[-1]
             write_data_html(result, html_name, review_path)
             review_link = 'Detail_Links/review_'+(path+review_path).split('/')[-3]+'_'+(path+review_path).split('/')[-2]+'_'+(path+review_path).split('/')[-1]+".html"

        if review_branch.strip()=="":
           review_branch = default_review_branch

        if review_branch and len(result) :  #if the manifest didn't set sub  revision, will remove it, the number of patches is not 0
             temp.append(git)
             temp.append(review_path)
             temp.append(review_branch) 
             temp.append(str(len(result)))
             temp.append(review_link)         
             data_list.append(temp)

    wirte_summary_html(data_list, father_path+'/Review/review_home', path)

if __name__ == '__main__':
        print(sys.argv[1])
        if sys.argv[1].endswith('/') :
            os.popen('cd %s ; rm Review -rf; mkdir Review; mkdir Review/Detail_Links'%(os.path.dirname(sys.argv[1].rstrip('/'))))
            review_git(sys.argv[1].rstrip('/'))
        else:
            os.popen('cd %s ; rm Review -rf; mkdir Review; mkdir Review/Detail_Links'%(os.path.dirname(sys.argv[1])))
            review_git(sys.argv[1])







