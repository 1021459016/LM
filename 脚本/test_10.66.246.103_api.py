import hashlib
import requests
import urllib3
import json
urllib3.disable_warnings()

#--------------获取key-------------------------------------------------------------
#适用于5.6.11版本
cookie = ''

def get_key(dev_ip):
	url = 'https://%s:8081/api/system/account/login/login'%dev_ip
	params = '{"username": "admin","password": "5cf781c4c8aafd258411bcbeccada5761a63194490c0d27e0e0fe6c101122503295b378b6023d93a7b5e2e6b54f68bbb4ceaa1da8b8ef46749284cdee0a2dc6805daf48b17b61e4eab897eccbad7e44fda85a4aa7b6de2d7e324abd7b9422edbaf1626194e074209f9ee5337bbeb6f453db34b7de11697e6a694ab1d6ce938c72d4e83f46e2b715b3f8e7525d5d029b0a4b9c94e06c61662c02e05777096b13108203afc1ca26c36ee0f7edbb2b9b7e1a54b0faaa20cefd87d5e15dd7ce4522dc3e209ccc3626230b4d10fb33b8889f1d775824f0440cd38ff89c5be1000815a83f6a989d2307dd66771c676b0581dd78e8f881b5008bac5984672ecb1cc7d63","lang": "zh_CN"}'
	resp = requests.post(url,params,verify=False)
	resp_dict = json.loads(resp.text)
	global cookie 
	cookie = resp.cookies
	return (resp_dict['data']['security_key'],resp_dict['data']['api_key'])
#适用于5.6.10版本


#------------------------------设置参数----------------------------------------------
dev_ip = '10.66.246.93'
security_key, api_key = get_key(dev_ip)
accountId = 'admin'
time = '1640330445060'



#------------------------------计算密钥---------------------------------------------
url = 'https://%s:8081/api/network/bypass/getInternalBypass'%dev_ip
rest_api= url.split('8081')[1]
jm = 'security-key:%s;api-key:%s;time:%s;rest-uri:%s' %(security_key,api_key,time,rest_api)
m1 = hashlib.sha256(jm.encode("utf-8"))
sign = m1.hexdigest()
url_request = '%s?sign=%s&apikey=%s&time=%s'%(url, sign, api_key, time)


#-------------------------------发送请求---------------------------------------------
try:
	request = requests.get(url=url_request,cookies=cookie,verify=False)
	print(request.text)
except Exception as e:
	print('请求失败',e)





