import cherrypy
from gurulab.user_controller import UserController
from gurulab.ticket_controller import TicketController


class API:
    exposed = True

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def login(self, **kwargs):
        input_data = cherrypy.request.json
        print(input_data)
        username = input_data.get("username")
        password = input_data.get("password")
        # 这里添加实际的验证逻辑
        if UserController.login(username=username, password=password):
            cherrypy.session['username'] = username
            return {"success": True, "message": "Login successful"}
        else:
            return {"success": False, "message": "Login failed"}

    @cherrypy.tools.json_out()
    def logout(self):
        if 'username' in cherrypy.session:
            # 移除会话中的用户名
            del cherrypy.session['username']
            # 返回登出成功的信息
            raise cherrypy.HTTPRedirect("/")
        else:
            # 如果用户未登录尝试登出，返回错误信息
            return {"success": False, "message": "No user currently logged in"}

    @cherrypy.tools.json_out()
    def ticket_templates(self, **kwargs):
        # Return all ticket_templates
        ticket_templates = TicketController.get_all_ticket_templates()
        if ticket_templates is not None:
            return [ticket_template.to_dict() for ticket_template in ticket_templates]

    @cherrypy.tools.json_out()
    def ticket_template(self, name_or_id=None):
        ticket_template = TicketController.get_ticket_template_by_name(name=name_or_id)
        if ticket_template is None:
            ticket_template = TicketController.get_ticket_template_by_id(ticket_template_id=name_or_id)

        if ticket_template is not None:
            return ticket_template.to_dict()
        else:
            return None
