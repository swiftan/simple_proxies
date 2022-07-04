import requests
from lxml import etree
import random
import time
import os
import threading
import json
mutex = threading.Lock() #注意互斥关系
def get_proxy():    
    mod_time = time.mktime(time.localtime(os.stat("proxies.txt").st_mtime))
    right_time = time.time()
    if (right_time-mod_time)/60 >= 2:   
        response1 = requests.get('https://free-proxy-list.net/')
        html1 = etree.HTML(response1.content)
        response2 = requests.get('https://www.sslproxies.org/')
        html2 = etree.HTML(response2.content)
        json_data = requests.get('https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=lastChecked&sort_type=desc&protocols=http').content
        data = json.loads(json_data)
        my_proxy1 = ''
        my_proxy2 = ''
        my_proxy3 = ''
        mutex.acquire()
        f = open("proxies.txt", 'r+')
        f.truncate(0) #清空上一次刷新内容
        for i in range(1, 41):
            proxy_ip1 = html1.xpath('//*[@id="list"]/div/div[2]/div/table/tbody/tr['+ str(i) + ']/td[1]/text()')[0]
            proxy_port1 = html1.xpath('//*[@id="list"]/div/div[2]/div/table/tbody/tr['+ str(i) + ']/td[2]/text()')[0]
            my_proxy1 = proxy_ip1+':'+proxy_port1
            f.write(my_proxy1+'\n')

            proxy_ip2 = html2.xpath('//*[@id="list"]/div/div[2]/div/table/tbody/tr['+ str(i) + ']/td[1]/text()')[0]
            proxy_port2 = html2.xpath('//*[@id="list"]/div/div[2]/div/table/tbody/tr['+ str(i) + ']/td[2]/text()')[0] 
            my_proxy2 = proxy_ip2+':'+proxy_port2
            f.write(my_proxy2+'\n')

            proxy_ip3 = data['data'][i]['ip']
            proxy_port3 = data['data'][i]['port']
            my_proxy3 = proxy_ip3+':'+proxy_port3
            f.write(my_proxy3+'\n')

        f.close()
        mutex.release()
    mutex.acquire()
    f = open("proxies.txt", 'r')
    my_data = f.readlines()
    f.close()
    mutex.release() 
    return random.choice(my_data).replace('\n', '')