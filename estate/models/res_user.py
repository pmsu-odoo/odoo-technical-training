from odoo import fields,models

class res_user(models.Model):

    _inherit="res.users"

    #Fields
    property_ids = fields.One2many("estate.property", "salesman", string="Properties" , domain=[("state", "in", ["new", "offer_received"])])        # breakpoint()
