from odoo import fields, models, api

class offer_wizard(models.TransientModel):
    
    #Minimum defination
    _name="offer.wizard"
    _description="this is the wizard for offers"

    #Fields
    price = fields.Float(string="Price",required=True)
    buyer = fields.Many2one('res.partner', string='Buyer') 
    validity = fields.Integer(string="Validity (days)",default=7)

    def wizard_action(self):
        active_ids = self.env.context.get('active_ids')
        for record in active_ids:
            self.env['estate.property.offer'].create({
                'price':self.price,
                'partner_id' : self.buyer.id,
                'validity' : self.validity,
                'property_id' : record
            })
