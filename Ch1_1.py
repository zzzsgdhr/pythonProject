import lxml.html,requests
url = 'https://www.python.org/dev/peps/pep-0020/'
xpath = '//*[@id="the-zen-of-python"]/pre/text()'
res = requests.get(url)
ht = lxml.html.fromstring(res.text)
text = ht.xpath(xpath)
print('Hello,\n'+''.join(text))
