from odoo import fields,models

class res_user(models.Model):

    _inherit="res.users"

    property_ids = fields.One2many("estate.property", "salesman", string="Properties" , domain=[("state", "in", ("new", "offer received"))])

    # property_ids = fields.One2many("estate.property", "salesman", string="Properties" , domain=[("state", "not in", ["canceled"]),("state", "not in", ["sold"])])
