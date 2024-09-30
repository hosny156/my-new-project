from odoo import models, fields, api

class AreaCheckWizard(models.TransientModel):
    _name = 'area.check.wizard'
    _description = 'Check Area Wizard'

    property_id = fields.Many2one('property.one')
    line_ids = fields.One2many('property.line', 'property_id')
    area = fields.Float(related='line_ids.area', string='Current Area', readonly=True)
    area_m = fields.Float(string='Reference Area m')
    state = fields.Selection([
        ('pending', 'Pending'),
        ('sold', 'Sold'),
    ], default='pending', string="state")
    reason = fields.Selection([
        ('quantity increased', 'Quantity Increased'),
        ('quantity incomplete', 'Quantity Incomplete'),
        ('quantity damaged', 'Quantity Damaged'),
    ], default='quantity increased')



    def check_area(self):
        property = self.property_id
        property.state = self.state
        self.property_id.create_history_record('draft', self.state, self.reason)
        self.property_id.state = self.state
