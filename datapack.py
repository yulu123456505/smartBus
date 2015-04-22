from struct import *
from functools import reduce

def a(s):
    if isinstance(s,bytes):
        s = bytes.decode(s)
        return reduce(lambda x,y:x+y,[i for i in s if i != '\0'])
    else:
        return s
if __name__ == '__main__':
    p = pack('10s10s3d',b'phoneid',b'time',0.1,0.2,0.3)
    print(p)
    m = unpack('10s10s3d',p)
    print(list(map(a,m)))