import requests,time

fp = open("proxylist.txt", 'r')
lines = fp.readlines()
print(lines)
for ip in lines[0:]:
      ip = ip.strip('\n')
      print("当前代理IP :\t" + ip)
      proxy = {'http':'http://{}'.format(ip)}

      url = "http://icanhazip.com"
      res = requests.get(url, proxies=proxy)
      print(res.status_code)
      print(res.text)
      print("通过")
      time.sleep(2)
