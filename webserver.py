
# server imports
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from traceback import print_list
from socketserver import ThreadingMixIn

class ThreadHTTPServer(ThreadingMixIn, HTTPServer):
    "This is an HTTPServer that supports thread-based concurrency."

class WebServerHandler(BaseHTTPRequestHandler):
    # list of attributs
    # main html form content
    index_form_header = ''
    index_form_footer = ''

    dummy_header = '''<html>
                        <head>
	                        <title>Dummy form</title>
                        </head>
                        <body>
                            <h1> Temporary page </h1>'''
    dummy_footer = '''</body>'''                    

    # css file content
    css_cont = ''

    def do_GET(self):
        path = self.path[1:]
        path_splt = path.split('/')
        ## print(path_splt)
        
        if self.path.endswith("/hello"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><body>"
            output += "<h1>Hello!</h1>"
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'>
                            <h2>What would you like me to say?</h2>
                            <input name="message" type="text" >
                            <input type="submit" value="Submit">
                         </form>'''
            output += "</body></html>"
            self.wfile.write(output.encode())
            ##print(output)
            return

        if self.path.endswith("/restaurants"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # if initial start - read all repeated files
            #if not self.index_form_header:
            if True:
                # opent html header content
                try:                    
                    with open('restaurants/index_header.tmplt', 'r') as fin:
                        self.index_form_header = fin.read()
                except:
                    self.index_form_header = self.dummy_header    
            
                # opent html footer content
                try:
                    with open('restaurants/index_footer.tmplt', 'r') as fin:
                        self.index_form_footer = fin.read()
                except:
                    self.index_form_footer = self.dummy_footer

                # opent css content
                try:
                    with open('restaurants/css/styles.css', 'r') as fin:
                        self.css_cont = fin.read()
                except:
                    pass
            # end of initialization   
            
            html_cont = self.index_form_header

            html_cont += self.index_form_footer

            # sent to client
            self.wfile.write(html_cont.encode())
            print(html_cont)
            return

        if 'img' in path_splt[0]:
            self.send_response(200)
            self.send_header('Content-type', 'image/jpg')
            self.end_headers()
            
            #open image content for binary read
            try:
                with open('restaurants/' + path, 'rb') as fin:
                    img_cont = fin.read()
            except:     # no image - use default picture
                print('error: no requested file', 'restaurants/' + path)
                with open('restaurants/img/no_image.jpg', 'rb') as fin:
                    img_cont = fin.read()
            
            self.wfile.write(img_cont)
            ##print(path)
            return

        if 'css' in path_splt[0]:
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            
            # if default style.css file
            if 'restaurants/' + path == 'restaurants/css/styles.css':
                # if initial start - read scc file (static thml)
                #if not self.css_cont:
                if True: 
                    # opent css content
                    try:
                        with open('restaurants/css/styles.css', 'r') as fin:
                            self.css_cont = fin.read()
                    except:
                        print('error: no requested file', 'restaurantss/' + path)
                # end of initialization 
                css_cont = self.css_cont
            else:
                try:
                    #opent requested css content
                    with open('restaurants/' + path, 'r') as fin:
                        css_cont = fin.read()
                except:
                    print('error: no requested file', 'restaurants/' + path)
                    css_cont = ''
            
            self.wfile.write(css_cont.encode())
            ## print(css_cont)
            return

        # redirect to static html template
        if self.path.endswith("/"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            try:                    
                with open('restaurants/index0.html', 'r') as fin:
                    message = fin.read()
            except:
                message += "<html><body>Empty for now</body></html>"
            self.wfile.write(message.encode())
            ##print(message)
            return

        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        #try:
            # get content_type and length
            content_type = self.headers.get('Content-type', 0)
            content_len = int(self.headers.get('Content-length', 0))
            
            # split data 
            ctype, pdict = cgi.parse_header(content_type)
            # convert messages content to bytes and add length
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            pdict['content-length'] = content_len

            if ctype == 'multipart/form-data':
                # get messages content (if several)
                fields = cgi.parse_multipart(self.rfile, pdict)
                # get only message (binary)
                messagecontent = fields.get('message')
                # select first and decode
                messagecontent = messagecontent[0].decode()
            
            output = ""
            output += "<html><body>"
            output += " <h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "</body></html>"
            
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(output.encode())
            ##print(output)
        #except:
        #    pass


def main():
    try:
        port = 8080
        # server = HTTPServer(('', port), WebServerHandler)
        # port = int(os.environ.get('PORT', 8001))   # Use PORT if it's there.
        server_address = ('', port)
        server = ThreadHTTPServer(server_address, WebServerHandler)

        print("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print(" ^C entered, stopping web server....")
        server.socket.close()

if __name__ == '__main__':
    main()