from datetime import datetime ,timedelta
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_utils

class property(models.Model):
    
    #minimum definations
    _name = "estate.property"
    _description = "Real Estate"
    _rec_name = 'title'
    _order = "id asc"

    #models fields
    title= fields.Char('Title', required=True)
    sequence = fields.Integer('Sequence',default=1.0)
    description= fields.Char('Description')
    postcode = fields.Char('Post code', size = 6)
    date_availability=fields.Date("Available From",copy=False,default =datetime.now()+relativedelta(months=1))
    expected_price=fields.Float("Expected price",required = False)
    selling_price=fields.Float("Selling Price",copy=False,readonly=True)
    bedrooms=fields.Integer("Bedrooms",default=2)
    living_area=fields.Float("Living Area (sqm)")
    facades=fields.Integer() 
    garage=fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Float("Garden Area (sqm)")
    active = fields.Boolean(default=True)
    garden_orientation= fields.Selection([('North','North'),('South','South'),('East','East'),('West','West')])
    state = fields.Selection([('new','New'),('offer_received','Offer Received'),('offer_accepted','Offer Accepted'),('sold','Sold'),('canceled','Canceled')],default='new',required=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesman = fields.Many2one('res.users', string='Salesman')
    buyer = fields.Many2one('res.partner', string='Buyer')
    tag_ids = fields.Many2many('estate.property.tag', string="Property Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offer Id")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_best_offer")
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company , readonly=True)
    ending_date = fields.Date(compute="_compute_end_date",store=True)

    #Sql Constraints
    _sql_constraints=[('check_expected_price','CHECK (expected_price > 0)','A property expected price can t be empty and negetive '),
                    ('check_selling_price','CHECK(selling_price >= 0)','A property selling price must be positive')]

    @api.depends('date_availability')
    def _compute_end_date(self):
        for record in self:
            record.ending_date = record.date_availability + timedelta(days=7)

    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _best_offer(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price")) if record.offer_ids else 0.0 

    @api.onchange('garden')
    def onchange_garden(self):
        if self.garden:
            self.garden_area = 10.0
            self. garden_orientation = 'North'
        else :
            self.garden_area = 0.0
            self. garden_orientation = False

    def state_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("Canceled property can't sold")
            else:
                self.write({'state': 'sold'})

    def state_canceled(self):
        for record in self:
            if record.state=='sold':
                raise UserError("Sold property can't canceled")
            else:
                self.write({'state': 'canceled'})

    @api.constrains('selling_price')
    def check_selling_price(self):
        for record in self:
            if (not float_utils.float_is_zero(record.selling_price, precision_rounding=0.001) and float_utils.float_compare(record.selling_price,(0.9*(record.expected_price)),precision_rounding=0.01)<0):
                raise ValidationError("Selling price can't lessthan 90 percent of expected price")

    @api.ondelete(at_uninstall=False)
    def _parameter_for_deletion(self):
        for record in self:
            if not record.exists().state in ['new', 'canceled']:
                raise UserError("A state which is not in New or Canceled state can't be deleted")

    def unlink_rejected_offer(self):
        rejected_offers = self.offer_ids.search(["&",('property_id','=',self.id),('status', '=', "refused")])
        rejected_offers_counts = self.offer_ids.search_count(["&",('property_id','=',self.id),('status', '=', "refused")])

        for offer in rejected_offers:
            offer.unlink()

    def delete_property(self):
        delete = self.unlink()

    def duplicate(self):
        return self.name_create('title')

    def return_wizard(self):
        return {
                'type':'ir.actions.act_window',
                'res_model':'offer.wizard',
                'name':'Add Offer',
                'view_mode':'form',
                'target':'new',
                'flags': {'mode': 'readonly'},
                }

    def accepted_offer(self):
        customer = self.offer_ids.search(["&",('property_id','=',self.id),('status', '=', "accepted")])
        if customer:
            return {
                'type':'ir.actions.act_window',
                'res_model':'estate.property.offer',
                'name':'Accepted Offer',
                'view_mode':'form',
                'target':'new',
                'res_id': customer.id,
                'flags': {'mode': 'readonly'},
                }
        else :
            raise ValidationError("NO Accepted offers")



    def filtering(self):
        offers = self.offer_ids.search([('property_id','=',self.id)]).filtered(lambda r: r.price > self.expected_price)
        return {
                'type':'ir.actions.act_window',
                'res_model':'estate.property.offer',
                'name':'Total Offer',
                'view_type': 'tree,form',
                'view_mode':'tree,form',
                'target':'new',
                'domain': [('id', 'in', offers.ids)],
                }

    def browsing(self):
        all_records = self.env['res.company'].browse(self.company_id.id)
        for record in all_records:
            return {
                    'type':'ir.actions.act_window',
                    'res_model':'res.company',
                    'name':'Company Details',
                    'view_mode':'form',
                    'target':'new',
                    'res_id': self.company_id.id,
                    'flags': {'mode': 'readonly'},
                    }

    def sorted_off(self):
        sorted_offers=self.offer_ids.search([('property_id','=',self.id)]).sorted(key=lambda p:p.price, reverse=True)
        return {
                'type':'ir.actions.act_window',
                'res_model':'estate.property.offer',
                'name':'Offer with Higest price',
                'view_type': 'form',
                'view_mode':'form',
                'target':'new',
                'res_id': sorted_offers[0].id,
                'flags': {'mode': 'readonly'},
                }

    def total_offer(self,id):
        offers_counts = self.offer_ids.search_count([('property_id','=',int(self.id))])
        return offers_counts