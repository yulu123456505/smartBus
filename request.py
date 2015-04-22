import urllib.request
import time

def urlRequest(s):
    r = urllib.request.urlopen(s)
    return r.read()

if __name__ == '__main__':
    while 1==1:
        url = 'http://127.0.0.1:8000/?id=1;name=2'
        r = urlRequest(url)
        print(r)
        time.sleep(1)