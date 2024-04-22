# gurulab-erp/app.py
import cherrypy
import os
from webui.api_controller import API
from functools import wraps
from cherrypy._cpdispatch import RoutesDispatcher


from gurulab.user_controller import UserController
from gurulab.ticket_controller import TicketController


def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 检查会话中是否有 'username' 或其他用户标识
        if 'username' not in cherrypy.session:
            raise cherrypy.HTTPRedirect("/login")
        return func(*args, **kwargs)
    return wrapper


class WebApp:
    @cherrypy.expose
    def index(self):
        return open(os.path.join('webui', 'static', 'index.html'))

    @cherrypy.expose
    def login(self):
        return open(os.path.join('webui', 'static', 'login.html'))

    @cherrypy.expose
    def admin(self, sub_path=None):
        return open(os.path.join('webui', 'static', 'admin.html'))

    @cherrypy.expose
    def vue_test(self):
        return open(os.path.join('webui', 'static', 'vue_test.html'))

    # 这里我们将展示如何处理模板ID和工单ID的动态路径
    @cherrypy.expose
    @require_login
    def dashboard(self, path=None, id=None):
        if path == "my_tickets":
            return open(os.path.join('webui', 'static', 'my_tickets.html'))
        elif path == "ticket_template" and id:
            # 实际操作中，这里可能需要渲染模板页面，展示指定ID的工单模板
            return open(os.path.join('webui', 'static', 'ticket_template.html'))
        elif path == "ticket" and id:
            # 同样，这里可能需要渲染具体工单的页面
            return f"Ticket Page for ID: {id}"
        else:
            return open(os.path.join('webui', 'static', 'dashboard.html'))



def setup_routes():
    dispatcher = RoutesDispatcher()
    api = API()  # 实例化API类

    dispatcher.connect('api_login', '/login', controller=api, action='login', conditions=dict(method=['POST']))
    dispatcher.connect('api_logout', '/logout', controller=api, action='logout', conditions=dict(method=['POST']))
    dispatcher.connect('api_ticket_templates', '/ticket_templates', controller=api, action='ticket_templates',
                       conditions=dict(method=['GET']))
    dispatcher.connect('api_ticket_template', '/ticket_template/{name_or_id}', controller=api, action='ticket_template', conditions=dict(method=['GET']))

    return dispatcher


if __name__ == '__main__':
    webapp = WebApp()  # 实例化WebApp类
    api = API()  # 实例化API类

    cherrypy.tree.mount(webapp, '/', {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'webui/static'
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'webui/static'
        }
    })

    cherrypy.tree.mount(api, '/api', {
        '/': {
            'request.dispatch': setup_routes(),  # 使用自定义路由分发
            'tools.sessions.on': True,
            'tools.sessions.timeout': 36000,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')],
        }
    })

    cherrypy.config.update({'server.socket_port': 8080})
    cherrypy.engine.start()
    cherrypy.engine.block()
