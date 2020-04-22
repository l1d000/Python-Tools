#!/usr/bin/python
# coding:utf-8
import csv
import os
import sys
import xml.dom.minidom as xmldom

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')


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




def get_data_grep_commit (path, commit):
    final = []
    output=os.popen(' cd %s ;git show -s --pretty=raw %s | grep Reviewed-on '%(path, commit)).read().splitlines()
    output_patch = os.popen(' cd %s ;git format-patch -1  %s '%(path, commit)).read().splitlines()
    
    if output_patch:
        os.popen(' mv %s/%s  ./Review/Patches '%(path, output_patch[0])).read().splitlines()

    if output:
#        print(output[0].split('Reviewed-on:')[-1])
        return output[0].split('Reviewed-on:')[-1]
    elif output_patch:
        return output_patch[0].split('0001-')[-1]
    else:
        return "N/A"


def get_data(path):
    final = []

    output=os.popen(' cd %s ;git log --author=htc --pretty=format:"%%s == %%ae == %%H == %%cd"'%(path)).read().splitlines()
    for item_list in output:
        temp = []
        item=item_list.split('==')
        for n in item:
            temp.append(n)
        temp.append(get_data_grep_commit(path, temp[2])) 
        final.append(temp)
      
    return final

	

def write_data_html(data_list, name, path):
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
	     <font size="5" color="#FF0000">Total: """+bytes(len(data_list))+"""</font>"""
    for index, data in enumerate(data_list):
        message = message+"""<tr>"""
        message = message+"""<td style="padding-right:20px">"""+str(index)+"""</td>"""
        for n in data:
            if "http://" in n:
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

def wirte_summary_html(data_list, name, path):
    file_name = name+".html"
    f = open(file_name,'w')
    message ="""
             <html>
             <body>
             <font size="10" color="#008000">Bluetooth </font>
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
            if ".html" in n or  "0001" in n:
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

def grep_all_git(path1,git_list):
    data_list = []
    for git in git_list:
        compare_path1 ="" 
        compare_branch1 = ""
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

        if compare_path1:
             result = get_data(path1+compare_path1)
             html_name = 'Review/Detail_Links/review_'+(path1+compare_path1).split('/')[-3]+'_'+(path1+compare_path1).split('/')[-2]+'_'+(path1+compare_path1).split('/')[-1]
             write_data_html(result, html_name, compare_path1)
             compare_link = 'Detail_Links/review_'+(path1+compare_path1).split('/')[-3]+'_'+(path1+compare_path1).split('/')[-2]+'_'+(path1+compare_path1).split('/')[-1]+".html"

        if compare_branch1 :
            temp.append(git)
            temp.append(compare_path1)
            temp.append(compare_branch1) 
            temp.append(str(len(result)))
            temp.append(compare_link)          
            data_list.append(temp)

    wirte_summary_html(data_list, 'Review/review_home', path1)

if __name__ == '__main__':
        os.popen('rm Review -rf; mkdir Review; mkdir Review/Detail_Links; mkdir Review/Patches')
        grep_all_git(sys.argv[1], final_git_list)
