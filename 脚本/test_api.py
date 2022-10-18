import hashlib
import time
import random

uid = 'admin'
token = 'eb155cf1-f497-4f52-ac10-b82579cb9cfe'
nonce = '3084'
timestamp = '1640072091'


url = 'https://172.20.91.5:8000/api/v1/object/networks/ippool'
hash1_str = url.split('api/v1')[1].encode('utf8')
m1 = hashlib.md5()
m1.update(hash1_str)
hash1_ret = m1.hexdigest()

# get hash2
hash2_str = ''


# get hash2
body = '{"endIp": "172.31.255.254","beginIp": "172.16.0.0","name": "ippool"}'.encode('utf-8')

m1 = hashlib.md5()
hash3_str = body
hash3_ret = ''
m1.update(hash3_str)
hash3_ret = m1.hexdigest()



hash_all_str = ''.join(sorted([hash1_ret, hash2_str, hash3_ret, uid, token, nonce, timestamp])).encode("utf-8")
#print(hash_all_str)
m2 = hashlib.sha1()
m2.update(hash_all_str)
hash_all_ret = m2.hexdigest()

print(hash_all_ret)
