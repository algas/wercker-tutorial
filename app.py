import tornado.ioloop
import tornado.web
import os
import pymysql
import logging
import json

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class UserHandler(tornado.web.RequestHandler):
    def initialize(self, connector):
        self.connector = connector

    def get(self, uid=None):
        cursor = self.connector.cursor(pymysql.cursors.DictCursor)
        if uid is None:
            cursor.execute('select * from user')
        else:
            cursor.execute('select * from user where id = %s', uid)
        self.write(json.dumps(cursor.fetchall()))
        cursor.close()

    def post(self):
        name = self.get_argument('name')
        cursor = self.connector.cursor(pymysql.cursors.DictCursor)
        res = cursor.execute('insert into user (name) values (%(name)s)', {'name':name})
        self.connector.commit()
        self.write('insert user: %s' % name)
        cursor.close()

    def put(self, uid):
        name = self.get_argument('name')
        cursor = self.connector.cursor(pymysql.cursors.DictCursor)
        res = cursor.execute('update user set name = %(name)s where id = %(uid)s', {'name':name, 'uid':uid})
        self.connector.commit()
        self.write('update user: %s' % name)
        cursor.close()

    def delete(self, uid):
        cursor = self.connector.cursor(pymysql.cursors.DictCursor)
        res = cursor.execute('delete from user where id = %(uid)s', {'uid':uid})
        self.connector.commit()
        self.write('delete user: %s' % uid)
        cursor.close()


class Application(tornado.web.Application):
    def __init__(self, **kwargs):
        options = {
            'mysql_host': os.environ.get('MYSQL_PORT_3306_TCP_ADDR', 'localhost'),
            'mysql_port': int(os.environ.get('MYSQL_PORT_3306_TCP_PORT', 3306)),
            'mysql_user': os.environ.get('MYSQL_ENV_MYSQL_USER', 'test'),
            'mysql_pass': os.environ.get('MYSQL_ENV_MYSQL_PASSWORD', 'secret'),
            'mysql_database': os.environ.get('MYSQL_ENV_MYSQL_DATABASE', 'user'),
        }
        connector = pymysql.connect(
                host=options['mysql_host'],
                port=options['mysql_port'],
                user=options['mysql_user'],
                passwd=options['mysql_pass'],
                db=options['mysql_database'])
        handlers = [
            (r"/", MainHandler),
            (r"/users", UserHandler, dict(connector=connector)),
            (r"/users/(.*)", UserHandler, dict(connector=connector)),
        ]
        super(Application, self).__init__(handlers, **kwargs)

def main(port):
    # app = make_app()
    logging.debug("start server")
    app = Application(autoreload=True)
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    port = int(os.environ.get('PORT', '8888'))
    main(port)
