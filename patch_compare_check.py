#!/usr/bin/python
# coding:utf-8
import csv
import os
import sys
import xml.dom.minidom as xmldom

final_git_list = [
    'local/platform/vendor/qcom-opensource/system/bt',
    'local/platform/vendor/qcom-proprietary/bt/btmultisim',
    'local/platform/vendor/qcom-proprietary/bt/dun',
    'local/platform/vendor/qcom-proprietary/ship/bt/hci_qcomm_init',
    'local/platform/vendor/qcom-opensource/bluetooth',
    'local/platform/vendor/qcom-opensource/bluetooth_ext',
    'local/platform/vendor/qcom-proprietary/bluetooth',
    'local/platform/vendor/qcom-opensource/system/bt',
    'local/platform/hardware/qcom/bt',
    'local/platform/packages/apps/Bluetooth',
    'common/customize/bluetooth',
    'common/android/platform/system/bt',
    'local/platform/system/bt']

def get_data(path1, path2):
    final = []
    final_path1 = []
#    output=os.popen(' cd %s ;git log --author=htc  --pretty=format:"%%s = %%ae = %%H = %%cd"'%(path1)).read().splitlines() 
    output=os.popen(' cd %s ;git log --pretty=format:"%%s = %%ae = %%H = %%cd"'%(path1)).read().splitlines()
    for item_path1 in output:
        temp = []
        item=item_path1.split('=')
        for n in item:
            temp.append(n)
#            if 'xxxxx' in n:
#                return final
        final_path1.append(temp)
      
    output=os.popen(' cd %s ;git log --pretty=format:"%%s = %%ae = %%H = %%cd"'%(path2)).read().splitlines()
 
    for item_path2 in output:
        temp = []
        item=item_path2.split('=')
        find_temp = []
        for n in item:
            temp.append(n)

        for item_path1 in final_path1 :
            if item[2] == item_path1[2] :
                find_temp = item
                break;
        if not find_temp :
             if not 'htc' in temp[1] and not 'Merge' in temp[0]:
                 final.append(temp)

    return final

	

def write_data_html(data, name, path):
    file_name = name+".html"
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
	     <font size="5" color="#FF0000">Total: """+bytes(len(data))+"""</font>"""
    for index, n in enumerate(data):
        message = message+"""<tr>"""
        message = message+"""<td style="padding-right:20px">"""+str(index)+"""</td>"""
        message = message+"""<td style="padding-right:20px">"""+n[0]+"""</td><td style="padding-right:20px">"""+n[1]+""" """+"""</td>"""
        message = message+"""<td style="padding-right:20px">"""+n[2]+"""</td><td style="padding-right:20px">"""+n[3]+""" """+"""</td>"""
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
             <font size="10" color="#008000">Compare Codebase</font>
             </br></br>
             <table border="1" cellspacing="0">
             <tr bgcolor="#008000">
             <th>Git</th>"""
    message = message+ """<th align="left" bgcolor="#EE9A00">"""+"Path"+"""</th>"""
    message = message+ """<th align="left" bgcolor="#EE9A00">"""+"p-rel_shep_qct8998.xml"+"""</th>"""
    message = message+ """<th align="left" bgcolor="#EE9A00">"""+"p-rel_shep_qct845.xml"+"""</th>"""
    message = message+ """<th align="left" bgcolor="#EE9A00">"""+"Add Patches"+"""</th>"""
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

def compare_git(path1, path2, git_list):
    data_list = []
    for git in git_list:
        compare_path1 ="" 
        compare_path2 ="" 
        compare_branch1 = ""
        compare_branch2 = ""
        compare_link = "" 
        temp = []

        xmlfilepath = os.path.abspath(path1+'/.repo/manifest.xml')
        domobj = xmldom.parse(xmlfilepath)
        elementobj = domobj.documentElement
        subElementObj = elementobj.getElementsByTagName("project")
        for item in subElementObj:
            if item.getAttribute("name") == git :                        
                compare_path1 = item.getAttribute("path")
                compare_branch1 = item.getAttribute("revision")
                
        xmlfilepath = os.path.abspath(path2+'/.repo/manifest.xml')
        domobj = xmldom.parse(xmlfilepath)
        elementobj = domobj.documentElement
        subElementObj = elementobj.getElementsByTagName("project")
        for item in subElementObj:
            if item.getAttribute("name") == git :                        
                compare_path2 = item.getAttribute("path")
                compare_branch2 = item.getAttribute("revision")

        if compare_path1 and compare_path2:
             result = get_data(path1+compare_path1, path2+compare_path2)
             html_name = 'CompareCodebase/Detail_Links/compare_'+(path1+compare_path1).split('/')[-3]+'_'+(path1+compare_path1).split('/')[-2]+'_'+(path1+compare_path1).split('/')[-1]
             write_data_html(result, html_name, compare_path1)
             compare_link = 'Detail_Links/compare_'+(path1+compare_path1).split('/')[-3]+'_'+(path1+compare_path1).split('/')[-2]+'_'+(path1+compare_path1).split('/')[-1]+".html"

        if compare_branch1 and compare_branch2:
            temp.append(git)
            temp.append(compare_path1)
            temp.append(compare_branch1)
            temp.append(compare_branch2)  
            temp.append(str(len(result)))
            temp.append(compare_link)          
            data_list.append(temp)

    wirte_summary_html(data_list, 'CompareCodebase/compare_home', path1)

if __name__ == '__main__':
        print("Path1:")
        print(sys.argv[1])
        print("Path2:")
        print(sys.argv[2])
        os.popen('rm CompareCodebase -rf; mkdir CompareCodebase; mkdir CompareCodebase/Detail_Links')
        compare_git(sys.argv[1], sys.argv[2], final_git_list)
