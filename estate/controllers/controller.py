from odoo import http

class Academy(http.Controller):

    @http.route('/real_estate/', auth='public')
    def index(self, **kw):
        
        Estate = http.request.env['real.estate.web']
        return http.request.render('estate.index', {
             'agents': Estate.search([])
         }) 