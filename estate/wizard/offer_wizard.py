from odoo import fields, models, api

class offer_wizard(models.TransientModel):
    
    _name="offer.wizard"
    _description="this is the wizard for offers"

    price = fields.Float(string="Price",required=True)
    
    buyer = fields.Many2one('res.partner', string='Buyer') 

    validity = fields.Integer(string="Validity (days)",default=7)

    def wizard_action(self):
        active_ids = self.env.context.get('active_ids')
        print("=================",active_ids)
        for record in active_ids:
            # context = record.env.context.get('context_id')
            # print(self._context.get_context('active_ids', false))
            # offer = self.env['estate.property.offer'].browse(record)
             
            # offer.price : self.price
            # offer.partner_id = self.buyer
            # offer.validity = self.validity
            # offer.property_id = record

            self.env['estate.property.offer'].create({
                'price':self.price,
                'partner_id' : self.buyer.id,
                'validity' : self.validity,
                'property_id' : record
            })
