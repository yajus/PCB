import requests

SUBMIT_URL = 'http://172.91.1.12:9090/ad/hacker/submit/submitCode'

SUBMIT_TIMEOUT=5

headers = {
      'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
      'Origin': 'http://172.91.1.12:9090',
      'Referer': 'http://172.91.1.12:9090/arace/index?'
}


COOKIES = {
      'JSESSIONID': '33217438A9E87E26137E9E3891FA61AE'
}
def get_flag(ip):
      import random
      hexdigits = '0123456789abcdef'
      return ''.join(random.choice(hexdigits) for _ in range(32))

flag = get_flag('172.91.1.31')
data = {'flag': flag}
print(data)
r = requests.post(SUBMIT_URL, data=data, headers=headers,timeout=SUBMIT_TIMEOUT, cookies=COOKIES)
print(r.content.decode('utf-8'))