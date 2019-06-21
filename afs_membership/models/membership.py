from odoo import api, fields, models


class MembershipType(models.Model):
    _name = 'afs.membership.type'

    name = fields.Char('Name')
    price = fields.Float('Price')
    note = fields.Text('Note')


class Membership(models.Model):
    _name = 'afs.membership'

    partner_id = fields.Many2one('res.partner', 'Member')
    membership_type_id = fields.Many2one('afs.membership.type', 'Membership Type')
    price = fields.Float('Price')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    description = fields.Text('Description')
    state = fields.Selection([('active', 'Active'),
                              ('expired', 'Expired')], string='Status', compute='_compute_membership_state')

    def _compute_membership_state(self):
        for rec in self:
            rec.state = True
