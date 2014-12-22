import BaseHTTPServer
import urlparse
import time
import MySQLdb
import random
import argparse
import os


db_host = ""
db_port = 0
db_user = ""
db_pwd  = ""
db_database = ""

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
        conn=MySQLdb.connect(host=db_host, user=db_user, passwd=db_pwd, db=db_database, port=db_port)
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



if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument("-host", "--mysqlip", help='mysql ip')
    # parser.add_argument("-port", "--mysqlport", help='mysql port')
    # parser.add_argument("-u", "--mysqluser", help='mysql username')
    # parser.add_argument("-p", "--mysqlpwd", help='mysql user password')
    # parser.add_argument("-db", "--mysqldb", help='mysql database')
    # args = parser.parse_args()
    # print args

    # db_host = args.mysqlip or "172.31.20.234"
    # db_port = int(args.mysqlport) or 3306
    # db_user = args.mysqluser or "root"
    # db_pwd  = args.mysqlpwd or "12345678"
    # db_database = args.mysqldb or "test"

    db_host = os.getenv("DBHOST", "172.31.20.234")
    db_port = int(os.getenv("DBPORT", "3306"))
    db_user = os.getenv("DBUSER", "root")
    db_pwd = os.getenv("DBPWD", "12345678")
    db_database = os.getenv("DBNAME", "test")

    # print showmysql(random.randint(1,3))
    # time.sleep(1)
    print "Starting server..."
    server = BaseHTTPServer.HTTPServer(('0.0.0.0',80), WebRequestHandler)
    server.serve_forever()
    print "Server starte"


