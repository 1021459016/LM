
import requests
import urllib3
urllib3.disable_warnings()



url_request = 'https://10.66.245.94:8081/api/service/hasOpened'

try:
	request = requests.get(url=url_request,auth=('admin','Nsf0cus@123'),verify=False)
	print(request.text)
except Exception as e:
	print('请求失败',e)



