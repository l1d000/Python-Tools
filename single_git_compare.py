#!/usr/bin/python
# coding:utf-8
import csv
import os
import sys
import xml.dom.minidom as xmldom

def get_data(path1, path2):
    final = []
    final_item_list1 = []

    output1=os.popen(' cd %s ;git log --pretty=format:"%%s = %%ae = %%H = %%cd"'%(path1)).read().splitlines()
    for item_list1 in output1:
        temp1 = []
        item1=item_list1.split('=')
        for n in item1:
            temp1.append(n)
        final_item_list1.append(temp1)
      
    output2=os.popen(' cd %s ;git log --pretty=format:"%%s = %%ae = %%H = %%cd"'%(path2)).read().splitlines()
 
    for item_list2 in output2:
        temp2 = []
        item2=item_list2.split('=')
        find_temp = []
        for n in item2:
            temp2.append(n)

        for item1 in final_item_list1 :
            if item2[2] == item1[2] :
                find_temp = item2
                break;
        if not find_temp :
             if not 'htc' in temp2[1] and not 'Merge' in temp2[0] and not 'Snap for' in temp2[0]:
                 final.append(temp2)

    return final

	

def write_data_html(data, name, path1, path2):
    file_name = name+".html"
    f = open(file_name,'w')
    message ="""
             <html>
             <body>
             <font size="10" color="#008000">Patch Compare</font></br></br>
             <font size="4" color="#008000">(Path1:"""+path1+""")</font></br>
             <font size="4" color="#008000">(Path2:"""+path2+""")</font></br></br>
             <table border="1" cellspacing="0">
             <tr bgcolor="#008000">
             <th>Index</th>
             <th>Title</th>
             <th>Author</th>
             <th>Commit ID</th>
             <th>Date</th>
             </tr>
	     <font size="5" color="#FF0000">Add: """+bytes(len(data))+"""</font>"""
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


def compare_git(path1, path2):
        result = get_data(path1, path2)
        html_name = 'Compare Result'
        write_data_html(result, html_name, path1, path2)
 
if __name__ == '__main__':
        print("Path1:")
        print(sys.argv[1])
        print("Path2:")
        print(sys.argv[2])    
        compare_git(sys.argv[1], sys.argv[2])
