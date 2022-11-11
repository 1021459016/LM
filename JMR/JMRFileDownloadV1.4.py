import requests
from bs4 import BeautifulSoup
import os,re,time
from JMRxmlmonitor import get_CT_md5,QuerySql
'''
time: 2022-11-11
author: zhaojiahao
'''


JMR_CT = get_CT_md5()
filter_href = ('Name','Last modified','Size','Description','Parent Directory','readme.txt','nohup.out')

class JmrFileDownload():
    def __init__(self,url,file_witre_dir) -> None:
        self.url = url
        self.file_witre_dir = file_witre_dir
    
    def download_file(self,file_path,file_witre_path):
        start = time.time()
        size = 0
        chunk_size = 1024 #每次下载的数据大小
        res = requests.get(url=file_path,stream=True)
        content_size = int(res.headers['content-length'])
        if res.status_code == 200:
            print('[文件大小]: %0.2f MB' % (content_size/chunk_size/1024))
            with open(file_witre_path, 'wb') as f:
                for data in res.iter_content(chunk_size=chunk_size):
                    f.write(data)
                    size += len(data)  # 已下载文件大小
                    # \r 指定第一个字符开始，搭配end属性完成覆盖进度条
                    print('\r'+ '[下载进度]: %s%.2f%%' % ('>'*int(size*50/content_size), float(size/content_size*100)), end='')
            end = time.time()
            print('\n' + "下载完成！用时%s.2f秒" % (end - start))
        else:
            print('无此文件')

    def get_file_name_list(self):
        file_list = []
        s = requests.session()
        res = s.get(self.url).content
        soup = BeautifulSoup(res, "html.parser")
        for i in soup.find_all('a'):
            if i.string not in filter_href:  #过滤返回上级目录的标签
                file_list.append(i.string)
        return file_list

    def if_CT(self,filemd5,file_witer_path):
        if filemd5 in JMR_CT:
            return True
        else:
            return False

    def start_download(self):
        list = []
        count = 1
        if not os.path.exists(self.file_witre_dir):
            os.mkdir(self.file_witre_dir)
        file_list = self.get_file_name_list()
        print('文件数量为：{}'.format(len(file_list)))
        start_time = time.time()
        for i in file_list:
            file_path = f'{self.url}{i}'
            file_witre_path = f'{self.file_witre_dir}\\{i}'
            print('正在下载中{}：{}'.format(count,i))
            try:
                self.download_file(file_path=file_path,file_witre_path=file_witre_path)
                filemd5 = QuerySql(file_witre_path)
                l = self.if_CT(filemd5=filemd5,file_witer_path=file_witre_path)
                if l:
                    print('[此文件MD5在CT库中]')
                else:
                    print(f'此文件不在CT库中，建议添加，文件MD5值为：{filemd5}')
                    list.append(filemd5)
            except Exception as e:
                print('下载文件异常',e)
            # l = if_CT(file_witre_path)
            # if l:
            #     print('[此文件MD5在CT库中]')
            # else:
            #     list.append(l)
            count+=1
        end_time = time.time()
        print('下载完成，共计下载文件数量为：{}，共计下载时间为：{}'.format(count,end_time-start_time))
        print('下列MD5不在CT库中：')
        for i in list:
            print(i)

if __name__ == '__main__':
    url = 'http://49.232.12.2:8000/'
    file_witre_dir = f'{os.path.dirname(__file__)}\\JMRDownloadDir'
    JMR_file_download = JmrFileDownload(url=url,file_witre_dir=file_witre_dir)
    JMR_file_download.start_download()