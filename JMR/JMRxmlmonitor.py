import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import hashlib,os
'''
time: 2022-11-11
author: zhaojiahao
'''

xml_file = f'{os.path.dirname(__file__)}\\VDB_201911081615.xml'

tree = ET.parse(xml_file) #读取xml文档
root = tree.getroot() #获取根节点

def get_CT_md5():
    CT_filemd5 = []
    for i in root:
        CT_filemd5.append(i.text)
    return CT_filemd5

def QuerySql(filename):
    # 定义文件名
    txtName = filename
    # 打印文本MD5
    md5_hash = hashlib.md5()
    with open(txtName,"rb") as f:
        for byte_block in iter(lambda: f.read(4096),b""):
            md5_hash.update(byte_block)
        # print("\n文件的MD5(大写的32位)：" + (md5_hash.hexdigest()).upper())
        # print("\n文件的MD5(小写的32位)：" + (md5_hash.hexdigest()).lower())
        # print("\n文件的MD5(大写的16位)："+(md5_hash.hexdigest())[8:-8].upper())
        # print("\n文件的MD5(小写的16位)：" + (md5_hash.hexdigest())[8:-8].lower())
        return md5_hash.hexdigest().lower()

if __name__ == '__main__':
    CT = get_CT_md5()
    filemd5 = QuerySql('D:\绿盟工作材料\TDC\TDC\僵木蠕\VDB\拨测专用\\JMRDownloadDir\\021e5a34bdcae49bab7a68b9d7b23fd38ce3d4d1')
    if filemd5 in CT:
        index = CT.index(filemd5)
        print(index)
        print(CT[index])
        print('True')
    else:
        print('False')
    