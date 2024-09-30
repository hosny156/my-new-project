from odoo import models, fields


class Stock(models.Model):
    _inherit = 'stock.picking'
    # to make the field related from stock to sale
    property_id = fields.Many2one('property.one', related='sale_id.property_id')

    # def _get_new_picking_values(self):
    #     res = super(StockPicking, self)._get_new_picking_values(related='property')
    #     res.update({'note': self.group_id.property_id.note})
    #     return res
    #
    # def _get_new_picking_values(self):
    #     vals = super(StockPicking, self)._get_new_picking_values()
    #     property_id = self.group_id.stock.view_picking_form.property_id.id
    #     vals['property_id'] = any(rule.propagate_property for rule in self.rule_id) and property_id
    #     return vals

    def action_confirm(self):
        res = super(Stock, self).action_confirm()
        print("inside action_confirm method")
        return res
