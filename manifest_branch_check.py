#!/usr/bin/python
# coding:utf-8
import csv
import os
import sys
import xml.dom.minidom as xmldom

final_git_list = [
    'local/platform/vendor/qcom-opensource/bluetooth',
    'local/platform/vendor/qcom-opensource/bluetooth_ext',
    'local/platform/vendor/qcom-opensource/bluetooth-commonsys-intf',
    'local/platform/vendor/qcom-opensource/system/bt',
    'local/platform/vendor/qcom-proprietary/bluetooth', 
    'local/platform/vendor/qcom-proprietary/bluetooth-commonsys-intf',
    'local/platform/vendor/qcom-proprietary/bt/btmultisim',
    'local/platform/vendor/qcom-proprietary/bt/dun',
    'local/platform/vendor/qcom-proprietary/ship/bt/hci_qcomm_init',
    'local/platform/hardware/qcom/bt',
    'local/platform/packages/apps/Bluetooth',
    'common/customize/bluetooth',
    'common/android/platform/system/bt',
    'local/platform/system/bt']


def wirte_summary_html(data_list, name, manifest1, manifest2):
    file_name = name+".html"
    f = open(file_name,'w')
    print("Path2:"+file_name)
    message ="""
             <html>
             <body>
             <font size="10" color="#008000">Compare Manifest</font>
             </br></br>
             <table border="1" cellspacing="0">
             <tr bgcolor="#008000">
             <th>Git</th>"""
    
    message = message+ """<th colspan="2" align="center" bgcolor="#008000">"""+manifest1+"""</th>"""
    message = message+ """<th colspan="2" align="center" bgcolor="#008000">"""+manifest2+"""</th>"""
    message =message+ """
             <tr>
             <th></th>"""
    
    message = message+ """<th align="center" bgcolor="#EE9A00">"""+"Path"+"""</th>"""
    message = message+ """<th align="center" bgcolor="#EE9A00">"""+"Branch"+"""</th>"""
    message = message+ """<th align="center" bgcolor="#EE9A00">"""+"Path"+"""</th>"""
    message = message+ """<th align="center" bgcolor="#EE9A00">"""+"Branch"+"""</th>"""

    

    for data in data_list:
        message = message+"""</tr><tr>"""
        for n in data:
            if "N" in n:
                message = message+"""<td><font style="padding-right:20px" color="#EE0000">"""+n+"""</td>"""
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

def compare_git(manifest1, manifest2, git_list):
    data_list = []
    for git in git_list:
        compare_path1 ="" 
        compare_path2 ="" 
        compare_branch1 = ""
        compare_branch2 = ""
        temp = []
        
        xmlfilepath = os.path.abspath(manifest1)  
        domobj = xmldom.parse(xmlfilepath)
        elementobj = domobj.documentElement
        subElementObj = elementobj.getElementsByTagName("project")
        for item in subElementObj:
            if item.getAttribute("name") == git :                        
                compare_path1 = item.getAttribute("path")
                compare_branch1 = item.getAttribute("revision")

        xmlfilepath = os.path.abspath(manifest2)        
        domobj = xmldom.parse(xmlfilepath)
        elementobj = domobj.documentElement
        subElementObj = elementobj.getElementsByTagName("project")
        for item in subElementObj:
            if item.getAttribute("name") == git :                        
                compare_path2 = item.getAttribute("path")
                compare_branch2 = item.getAttribute("revision")

#        if compare_branch1 and compare_branch2:
        temp.append(git)

        if compare_path1:
            temp.append(compare_path1)
        else:
            temp.append("N/A")

        if compare_branch1:
            temp.append(compare_branch1)
        else:
            temp.append("N/A")

        if compare_path2:
            temp.append(compare_path2)
        else:
            temp.append("N/A")

        if compare_branch2:
            temp.append(compare_branch2)
        else:
            temp.append("N/A")   

        data_list.append(temp)

    wirte_summary_html(data_list, 'Manifest_Compare', manifest1.split('/')[-1], manifest2.split('/')[-1])

if __name__ == '__main__':
        print("Path1:")
        print(sys.argv[1])
        print("Path2:")
        print(sys.argv[2])
        os.popen('rm Manifest_Compare.html -rf;')
        compare_git(sys.argv[1], sys.argv[2], final_git_list)
