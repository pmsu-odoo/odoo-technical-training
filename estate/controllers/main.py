import odoo
from odoo import http
from odoo.http import request

class Agents(http.Controller):

    @http.route('/real_estate/', auth='public',website='True', type="http")
    def index(self, **kw):
        Estate = request.env['real.estate.web']
        return request.render('estate.controllers_index', {
             'agents': Estate.search([])
         })  

    # @http.route('/real_estate/<name>/', auth='public', website=True)
    # def agent(self, name):
    #     return '<h1>{}</h1>'.format(name)

    # @http.route('/real_estate/<int:id>/', auth='public', website=True)
    # def agent(self, id):
    #     return '<h1>{} ({})</h1>'.format(id, type(id).__name__)
    
    @http.route('/real_estate/<model("real.estate.web"):agent>/', auth='public', website=True)
    def agents(self, agent):
        return http.request.render('estate.biography', {
            'person': agent
        })