from jinja2 import Environment, PackageLoader
import http.server as hs
import sys, os
 
env = Environment(loader=PackageLoader('template'))    # 创建一个包加载器对象
template = env.get_template('index.html')    # 获取一个模板文件

    
class RequestHandler(hs.BaseHTTPRequestHandler):
    def write_header(self, type, len, status):
        self.send_response(status)
        self.send_header("Content-type", type)
        self.send_header("Content-Length", str(len))
        self.end_headers()

    def send_content(self, page, status = 200):
        self.write_header("text/html", len(bytes(page)), status)
        self.wfile.write(bytes(page))
        #print(len(bytes(page)))
    
    def send_img_content(self, content, status = 200):
        self.write_header("image/jpg", len(bytes(content)), status)
        self.wfile.write(bytes(content))

    def get_path(self, parent, sub, dic):
        dir = os.path.join(parent, sub)
        for _,dirnames,_ in os.walk(dir):
            for name in dirnames:
                dic.append(name)
            dic.sort(reverse = True)
        return dir

    def get_filename(self, parent, sub, dic):
        dir = os.path.join(parent, sub)
        for _,_,filenames in os.walk(dir):
            for name in filenames:
                dic.append(name)
            dic.sort(reverse = True)
        return dir

    def write_page(self):
        date_dic = []
        img_dir = self.get_path(os.getcwd(), 'img', date_dic)
        print(date_dic)
        img_name = {}
        for date in date_dic:
            img_name[date] = []
            self.get_filename(img_dir, date, img_name[date])
        print(img_name)
        self.send_content(template.render(date_list = date_dic, img_name = img_name, img_prefix = '/img').encode('utf-8'))

    def write_image(self, full_path):
        print(full_path)
        try:
            with open(full_path, 'rb') as file:
                content = file.read()
                self.send_img_content(content)
                print("write done")
        except IOError as msg:
            print(msg)

    def do_GET(self):
        full_path = os.getcwd() + self.path
        if os.path.isfile(full_path):
            self.write_image(full_path)
        else:
            self.write_page()

if __name__ == '__main__': 
    httpAddress = ('', 8030)
    httpd = hs.HTTPServer(httpAddress, RequestHandler)
    httpd.serve_forever()