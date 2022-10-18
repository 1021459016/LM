#!/usr/bin/python
#web is null
#python lmt_tools_xml_json_parse.py path
import os
import sys
import json
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
LOG_PATH = "/tmp/"

NO_REPAIR = ['/opt/nsfocus/etc/field.xml','/opt/nsfocus/etc/vty_config.xml','/opt/nsfocus/etc/furlfilter/urlsysconfig.xml']

def parseFile(fileName):
    parser = make_parser()
    parser.setContentHandler(ContentHandler())
    parser.parse(fileName)

def repair_file(fileName):
    orig_file = '/mnt/cf/orig/' + fileName[5:]
    if os.path.exists(orig_file) and fileName not in NO_REPAIR:
        try:
            os.system('mv %s %s.bak' %(fileName,fileName))
            os.system('cp /mnt/cf/orig/%s %s' %(fileName[5:],fileName[0:17]))
            print('%s is successes'%fileName)
        except Exception as e:
            print('Error')
    else:
        print('%s File does not exist' %fileName)

if __name__ == "__main__":
    args = sys.argv
    dst_path = args[1]
    file_repair = []
    for root,dirs,files in os.walk(dst_path): 
        #for dir in dirs: 
            #print os.path.join(root,dir).decode('gbk').encode('utf-8'); 
        for file in files:
            if file.endswith(".xml"):
                #print os.path.join(root,file).decode('gbk').encode('utf-8')
                try:
                    parseFile(os.path.join(root,file))
                    #print('\n\t:), %s is OK!\n' % os.path.join(root,file).decode('gbk').encode('utf-8'))
                except Exception as e:
                    print('Error: %s is syntax error !\n' % os.path.join(root, file).decode('gbk').encode('utf-8'))
                    file_repair.append(str(os.path.join(root, file).decode('gbk').encode('utf-8')))
            elif file.endswith(".json"):
                #print os.path.join(root,file).decode('gbk').encode('utf-8')
                with open(os.path.join(root,file), "r+") as one_file:
                    try:
                        json.load(one_file)
                    except Exception as e:
                        print('Error: %s is syntax error !\n' % os.path.join(root, file).decode('gbk').encode('utf-8'))
    while True:
        chooes = raw_input('Whether to repair the fault?(y/n):')
        if chooes == 'y':
            for i in file_repair:
                repair_file(i)
                print('repair successes')
            break
        elif chooes == 'n':
            print('system exit')
            break
        else:
            print('input error')
