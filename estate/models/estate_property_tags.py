from odoo import fields,models

class estate_property_tag(models.Model):
    
    # Minimun Defination
    _name="estate.property.tag"
    _description="Defining Property Tag"
    _order = "name"
    # Fields
    name=fields.Char('Name',required=True)
    color = fields.Integer()

    #Sql Constraints
    _sql_constraints=[('check_name','UNIQUE (name)','Each name must be unique')]