import odoo
from odoo import http
from odoo.http import request

class Properties(http.Controller):

    @http.route('/properties/', auth='public',website='True', type="http", csrf=False)
    def property(self, id=False, **kw):
        properties = request.env['estate.property']
        if id:
            id = int(id)
            properties.browse(id)
        return request.render('estate.controllers_properties_template', {
             'properties': properties.search([])
         })