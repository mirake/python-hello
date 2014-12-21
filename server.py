import BaseHTTPServer
import urlparse
import time
import MySQLdb
import random

class WebRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        """
        """
        parsed_path = urlparse.urlparse(self.path)
        message_parts = [
                'CLIENT VALUES:',
                'client_address=%s (%s)' % (self.client_address,
                                            self.address_string()),
                'command=%s' % self.command,
                'path=%s' % self.path,
                'real path=%s' % parsed_path.path,
                'query=%s' % parsed_path.query,
                'request_version=%s' % self.request_version,
                '',
                'SERVER VALUES:',
                'server_version=%s' % self.server_version,
                'sys_version=%s' % self.sys_version,
                'protocol_version=%s' % self.protocol_version,
                '',
                'HEADERS RECEIVED:',
                ]
        for name, value in sorted(self.headers.items()):
            message_parts.append('%s=%s' % (name, value.rstrip()))
        message_parts.append('')
        message = '\r\n'.join(message_parts)
        message = showmysql(random.randint(1,3)) + "\r\n\r\n"
        self.send_response(200)
        self.end_headers()
        self.wfile.write(message)

def showmysql(uid):
    ret = ""
    try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='12345678',db='test',port=3306)
        cur=conn.cursor()
        cur.execute('select * from tmp where id=%d ' % uid)

        # results=cur.fetchmany(5)
        results = cur.fetchone()
        ret = results[1]

        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        ret = "exception"

    return ret

time.sleep(1)
print "Starting server..."
server = BaseHTTPServer.HTTPServer(('0.0.0.0',80), WebRequestHandler)
server.serve_forever()
print "Server started"

