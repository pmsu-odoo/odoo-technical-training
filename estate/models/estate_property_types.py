from odoo import fields,models,api

class estate_property_type(models.Model):
    # minimum defination
    _name="estate.property.type"
    _description="Definres the property types"
    _order = "sequence,name"

    # Fields
    name = fields.Char('Name',required=True)
    sequence = fields.Integer('Sequence',default=1.0)

    offer_count = fields.Integer(compute='_total_offers')
    
    #Relational Feilds
    property_ids = fields.One2many('estate.property','property_type_id',string='Property')

    #Sql Constraints
    _sql_constraints=[('check_name','UNIQUE (name)','Each Type must be unique')]

    #Compute methods
    @api.depends('property_ids.offer_ids')
    def _total_offers(self):
        for record in self:         
            record.offer_count = len(record.property_ids.offer_ids)