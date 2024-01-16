from odoo import models,fields,Command
from datetime import date

class inherit_estate_property(models.Model):

    _inherit = "estate.property" 

    def state_sold(self):
        invoice = super().state_sold()
        print("Override is complete")
       
        for record in self:
            print(record.selling_price)
            self.env["account.move"].create(
                                            {   "partner_id": record.buyer.id,
                                                "move_type": "out_invoice",
                                                "invoice_date":date.today(),
                                                "invoice_line_ids":[
                                                                    Command.create({
                                                                        "name":record.title,
                                                                        "quantity": 1.0,
                                                                        "price_unit": (record.selling_price * 0.06 )
                                                                    }),
                                         
                                                                   Command.create({
                                                                        "name": "Administrative fees",
                                                                        "quantity": 1.0,
                                                                        "price_unit": 100.0
                                                                    })]
                                                }
                                    )

        return invoice