import odoo
from odoo import http
from odoo.http import request

class Agents(http.Controller):

    @http.route('/real_estate/', auth='public',website='True', type="http", csrf=False)
    def index(self, **kw):
        Estate = request.env['real.estate.web']
        breakpoint()
        return request.render('estate.controllers_index', {
             'agents': Estate.search([])
         })

    @http.route('/real_estate/<model("real.estate.web"):agent>/', auth='public', website=True, csrf=False)
    def agents(self, agent):
        return http.request.render('estate.biography', {
            'person': agent
        })