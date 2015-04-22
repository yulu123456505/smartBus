from http.server import HTTPServer,BaseHTTPRequestHandler  
import io,shutil
import time

#将带等号的字符串返回为元组
def param2tuple(s):
    return tuple(s.split('='))
#将路径返回为字典
def path2dict(s):
    p = s.split('?')
    if len(p) == 2:
        return dict(list(map(param2tuple, p[1].split(';'))))

class MyHttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        r_str="Hello World"
        r_str = r_str + time.strftime(' %Y-%m-%d %H:%M:%S')
        p = path2dict(self.path)
        if p != None:
            for key, value in p.items():
                r_str = r_str + "<br>" + key + "=" + value
        enc="UTF-8"  
        encoded = ''.join(r_str).encode(enc)  
        f = io.BytesIO()  
        f.write(encoded)  
        f.seek(0)  
        self.send_response(200)  
        self.send_header("Content-type", "text/html; charset=%s" % enc)  
        self.send_header("Content-Length", str(len(encoded)))  
        self.end_headers()  
        shutil.copyfileobj(f,self.wfile)  
  
httpd=HTTPServer(('127.0.0.1',8000),MyHttpHandler)
print("Server started on 127.0.0.1,port 8000.....")
httpd.serve_forever()




if __name__ == '__main__':
    a='\?id=1;name=2'
    b='\d.ico'
    print(path2dict(a))