from odoo import models, fields, api

class Agents(models.Model):
    _name = 'real.estate.web'
    _description = 'Real Estate Web'

    name = fields.Char()
    biography = fields.Html()