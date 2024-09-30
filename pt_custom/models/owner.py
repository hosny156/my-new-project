from odoo import models, fields


# the owner
class Owner(models.Model):
    _name = 'owner'

    name = fields.Char(required=True)
    phone = fields.Char()
    address = fields.Char()
    property_ids = fields.One2many('property.one', 'owner_id')
