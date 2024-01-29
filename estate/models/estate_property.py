from datetime import datetime
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

    date_availability=fields.Date("Available From",copy=False,default =datetime.now()+relativedelta(months=3))

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

    state = fields.Selection([('new','New'),('offer received','Offer Received'),('offer accepted','Offer Accepted'),('sold','Sold'),('canceled','Canceled')],default='new',required=True)
    
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")

    salesman = fields.Many2one('res.users', string='Salesman')

    buyer = fields.Many2one('res.partner', string='Buyer')

    tag_ids = fields.Many2many('estate.property.tag', string="Property Tags")

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offer Id")

    total_area = fields.Float(compute="_compute_total_area")

    best_price = fields.Float(compute="_best_offer")

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company , readonly=True)

 
    #Sql Constraints
    _sql_constraints=[('check_expected_price','CHECK (expected_price > 0)','A property expected price can t be empty and negetive '),
                    ('check_selling_price','CHECK(selling_price >= 0)','A property selling price must be positive')]

 
    #Calculating total area:
    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _best_offer(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price")) if record.offer_ids else 0.0 

        
    def Browse(self):
        all_records = self.env['res.company'].browse(self.company_id.id)                            #bROWSE METHOD
        
        for record in all_records:
            print("###Company name :",record.name)


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
                self.write({'state': 'sold'})                                   #write method


    def state_canceled(self):
        for record in self:
            if record.state=='sold':
                raise UserError("Sold property can't canceled")
            else:
                self.write({'state': 'canceled'})                               #write method


    
    @api.constrains('selling_price')
    def check_selling_price(self):
        for record in self:
            if (not float_utils.float_is_zero(record.selling_price, precision_rounding=0.001) and float_utils.float_compare(record.selling_price,(0.9*(record.expected_price)),precision_rounding=0.01)<0):
                raise ValidationError("Selling price can't lessthan 90 percent of expected price")

    @api.ondelete(at_uninstall=False)
    def _parameter_for_deletion(self):
        # if any(record.state not in ['new', 'canceled'] for record in self):

        if not self.exists().state in ['new', 'canceled'] :                                                     #exist() method
            raise UserError("A state which is not in New or Canceled state can't be deleted")
        


    def return_wizard(self):
        return {
                'type':'ir.actions.act_window',
                'res_model':'offer.wizard',
                'name':'Add Offer',
                'view_mode':'form',
                'target':'new',
                
        }


    #search method
    def accepted_offer(self):
        customer = self.env['estate.property.offer'].search(["&",('property_id','=',self.id),('status', '=', "accepted")])
        print(customer.id)
        print("Price:",customer.price)
        print("\nProperty:",customer.partner_id.name)
        print("\nCustomer:",customer.property_id.title)

        # return self.env.ref('estate_property_offer').fields_view_get(view_id=customer.id)
        return {
                'type':'ir.actions.act_window',
                'res_model':'estate.property.offer',
                'name':'Accepted Offer',
                'view_mode':'form',
                'target':'new',
                'res_id': customer.id ,
                'context' : {'test':True}
                
        }

    #unlink
    def unlink_rejected_offer(self):
        rejected_offers = self.env['estate.property.offer'].search(["&",('property_id','=',self.id),('status', '=', "refused")])
        
        #search count
        rejected_offers_counts = self.env['estate.property.offer'].search_count(["&",('property_id','=',self.id),('status', '=', "refused")])

        print(rejected_offers_counts,"============================================================================")

        for offer in rejected_offers:
            offer.unlink()
    
    #Unlink the property
    def delete_property(self):
        aaa = self.unlink()
        print(aaa)
    def duplicate(self):
        return self.name_create('title')

    #Filtered Method
    def Filter(self):
        offers = self.env['estate.property.offer'].search([('')]).filtered(lambda r: r.property_id == self)
        for offer in offers:
            print("=================",offer.price)

    #sorted Method
    def sorted_off(self):
        sorted_offers=self.env['estate.property.offer'].search([('property_id','=',self.id)]).sorted(key=lambda p:p.price, reverse=True)
        for a in sorted_offers:
            print('=====================================',a.price)