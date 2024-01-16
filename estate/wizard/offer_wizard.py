from odoo import fields, models, api

class offer_wizard(models.TransientModel):
    
    _name="offer.wizard"
    _description="this is the wizard for offers"

    price = fields.Float(string="Price",required=True)
    
    buyer = fields.Many2one('res.partner', string='Buyer') 

    validity = fields.Integer(string="Validity (days)",default=7)

    def wizard_action(self):
        for record in self:
            context = record.env.context.get('context_id')
            print(context,)
            offer = self.env['estate.property.offer'].browse(context)
            
            offer.price = self.price
            offer.partner_id = self.buyer
            offer.validity = self.validity
            offer.property_id = context