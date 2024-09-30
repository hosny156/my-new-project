from odoo import models, fields, api
from odoo.exceptions import ValidationError


# property fields
class PropertyOne(models.Model):
    _name = 'property.one'
    _description = 'Property.one'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ref = fields.Char(default='New', readonly=True)
    name = fields.Char(required=True, default='New', size=99, translate=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Customer",
    )
    company_id = fields.Many2one('res.company', string='Company', ondelete='cascade', index=True,
                                 help="If set, action binding only applies for this company")
    user_id = fields.Many2one(
        'res.users', string='Buyer', index=True, tracking=True,
        default=lambda self: self.env.user, check_company=True)
    description: object = fields.Text(tracking=1)
    postcode = fields.Char(required=True)
    date_availability = fields.Date(tracking=1)
    expected_selling_date = fields.Date(tracking=1)
    is_late = fields.Boolean()
    expected_price = fields.Float()
    selling_price = fields.Float()
    diff = fields.Float(compute='_compute_diff')
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], default='north')
    owner_id = fields.Many2one('owner')
    tag_ids = fields.Many2many('tag')
    owner_address = fields.Char(related='owner_id.address')
    owner_phone = fields.Char(related='owner_id.phone')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed', 'Closed'),
    ], default='draft', string="state")
    property_id = fields.Many2one('property.one')
    area = fields.Float()
    area_m = fields.Float()
    description = fields.Char()

    # to change the state to draft
    def action_draft(self):
        for rec in self:
            rec.create_history_record(rec.state, 'draft')
            rec.state = 'draft'

    # to change the state to pending
    def action_pending(self):
        for rec in self:
            for line in rec.line_ids:
                if line.area != line.area_m:
                    return {
                        'name': 'Unarchive Tickets',
                        'view_mode': 'form',
                        'res_model': 'area.check.wizard',
                        # 'views': [(self.env.ref('pt_custom.action_area_check_wizard').id, 'form')],
                        'type': 'ir.actions.act_window',
                        'target': 'new',
                        'context': {
                            'default_property_id': self.id
                        }
                    }
            rec.create_history_record(rec.state, 'pending')
            rec.write({
                'state': 'pending'
            })

        # to change the state to sold

    def action_sold(self):
        for rec in self:
            rec.create_history_record(rec.state, 'sold')
            rec.state = 'sold'

    # to change the state to close
    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state, 'closed')
            rec.state = 'closed'
            template = self.env.ref('pt_custom.email_template_name')
            template.send_mail(self.id, force_send=True)

    # history
    def create_history_record(self, old_state, new_state, reason=""):
        for rec in self:
            rec.env['property.history'].create({
                'user_id': rec.env.uid,
                'property_id': rec.id,
                'old_state': old_state,
                'new_state': new_state,
                'reason': reason or "",
                'line_ids': [(0, 0, {'description': line.description, 'area': line.area, 'area_m': line.area_m}) for
                             line in rec.line_ids],
            })

    # action history wizard
    def action_open_change_state_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('pt_custom.change_state_wizard_action')
        action['context'] = {'default_property_id': self.id}
        return action

    def action_change_state_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('pt_custom.action_area_check_wizard')
        action['context'] = {'default_property_id': self.id}
        return action

    # def action_change_area_wizard(self):
    #     action = self.env['ir.actions.actions']._for_xml_id('pt_custom.action_area_check_wizard')
    #     action['context'] = {'default_property_id': self.id}
    #     return action

    # def action_open_change_area_wizard(self):
    #     action = self.env['ir.actions.actions']._for_xml_id('pt_custom.change_area_wizard_action')
    #     action['context'] = {'default_line_ids': self.id}
    #     return action

    _sql_constraints = [
        ('unique_name', 'unique("name")', 'This name is exist!')
    ]

    line_ids = fields.One2many('property.line', 'property_id')
    active = fields.Boolean(default=True)

    # compute fields
    @api.depends('expected_price', 'selling_price', 'owner_id.phone')
    def _compute_diff(self):
        for rec in self:
            print("inside _compute_diff method")
            rec.diff = rec.expected_price - rec.selling_price

    # to compute the price
    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for rec in self:
            return {
                'warning': {'title': 'warning', 'message': 'negative value.', 'type': 'notification'}
            }

    # to check bedrooms has valid
    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError('Please add valid number of bedrooms!')

    # cron jop
    def check_expected_selling_date(self):
        property_ids = self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
                rec.is_late = True

    def action(self):
        print(self.env['property.one'].search([]))

    # create a seq
    @api.model
    def create(self, vals):
        res = super(PropertyOne, self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('property_seq')
        return res

    # action for smart button
    def action_open_related_owner(self):
        action = self.env['ir.actions.actions']._for_xml_id('pt_custom.owner_action')
        view_id = self.env.ref('pt_custom.owner_view_form').id
        action['res_id'] = self.owner_id.id
        action['views'] = [[view_id, 'form']]
        return action


class PropertyLine(models.Model):
    _name = 'property.line'

    property_id = fields.Many2one('property.one')
    area = fields.Float()
    area_m = fields.Float()
    description = fields.Char()


