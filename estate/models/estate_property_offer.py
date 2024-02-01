from dateutil.relativedelta import relativedelta
from datetime import date
from odoo import fields,models,api
from odoo.exceptions import UserError

class estate_property_offer(models.Model):
    
    # Minimum defination
    _name="estate.property.offer"
    _description="Offers in property"
    _order = "price desc"

    # Fields
    price =fields.Float(string="Price",required=True)
    status = fields.Selection([('accepted','Accepted'),('refused','Refused')],copy = False)
    partner_id =fields.Many2one('res.partner',required=True)
    property_id = fields.Many2one('estate.property',required=True)
    validity = fields.Integer(string="Validity (days)",default=7)
    date_deadline = fields.Date(compute = '_date_deadline',inverse='_inverse_deadline')
    property_type_id = fields.Many2one("estate.property.type",related = 'property_id.property_type_id', store = True)
    create_date=fields.Date()

    #Sql Constraints 
    _sql_constraints=[('check_price','CHECK (price >= 0)','A offer price must be strictly positive')]

    @api.depends('create_date','validity')
    def _date_deadline(self) :
        for offer in self:
            offer.create_date = offer.create_date if offer.create_date else date.today()
            offer.date_deadline = fields.Datetime.add(offer.create_date, days=offer.validity)

    def _inverse_deadline(self):
        for offer in self:
            offer.create_date = offer.create_date if offer.create_date else date.today()
            offer.validity = (offer.date_deadline - offer.create_date).days

    def accepted_button(self):
        if 'accepted' in self.property_id.offer_ids.mapped('status') :
            raise UserError("An offer is already Accepted")
       
        self.status='accepted'
        self.property_id.state = 'offer_accepted' 
        self.property_id.selling_price = self.price
        self.property_id.buyer = self.partner_id.id

    def refused_button(self):
        self.status='refused'
        self.property_id.state = 'offer_received'
        self.property_id.selling_price = 0.0

    @api.model_create_multi
    def create(self, vals):
        offer = super(estate_property_offer, self).create(vals)
        for records in offer:
            if vals:
                records.property_id.state="offer_received"
        return offer

    def duplicating(self):
        for record in self:
            duplicate = record.copy(default = {'price': 12345 })