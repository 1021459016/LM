import hashlib
import time
import random
import request
import urllib3
urllib3.disable_warnings()

accountId = 'admin'
token = '6409f767-3216-4e4d-8e11-f959fda50aba'    
nonce = '3084'               #随机数
timestamp = '1640072091'     #时间戳


url = 'https://10.66.254.1/api/v1/devices'


#get hashstr1
hash1_str = url.split('api/v1')[1].encode('utf8')    #截取api/v1前后字符生成一个列表
m1 = hashlib.md5()
m1.update(hash1_str)
hash1_ret = m1.hexdigest()

# get hashstr2  暂无使用场景，一般为空
hash2_str = ''



# get hashstr3
hash3_ret = ''
# m1=''
# m1 = hashlib.md5()
# body = '{"app": "", "scmProfile": "", "appFilter": "", "id": "1", "trackBegin": "false", "service": "310001", "profileGroup": "", "dstObject": "110001", "urlProfile": "", "sessionTimeout": "", "trackEnd": "true", "trackNumber": "", "dstZone": "global", "customUser": "", "ipsProfile": "2", "user": "0", "appGroup": "", "srcZone": "global", "name": "ftp", "enabled": "true", "srcObject": "110001", "time": "343001", "action": "accept", "antivirusProfile": "", "trackAll": "false"}'.encode('utf-8')
# hash3_str = body
# hash3_ret = ''
# m1.update(hash3_str)
# hash3_ret = m1.hexdigest()

#get signature
hash_all_str = ''.join(sorted([hash1_ret, hash2_str, hash3_ret, accountId, token, nonce, timestamp])).encode("utf-8")
m2 = hashlib.sha1()
m2.update(hash_all_str)
signature = m2.hexdigest()


#requets
url = "%s?signature=%s&nonce=%s&timestamp=%s&accountId=%s" %(url, signature, nonce, timestamp, accountId)


try:
	request = request.get(url=url,verify=False)
	print(request.text)
except Exception as e:
	print('请求失败',e)

