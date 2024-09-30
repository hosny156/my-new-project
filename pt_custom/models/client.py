from odoo import models


# clint field
class Client(models.Model):
    _name = 'client'
    _inherit = 'owner'
