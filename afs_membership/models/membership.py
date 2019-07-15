from odoo import api, fields, models


class MembershipType(models.Model):
    _name = 'afs.membership.type'
    _description = 'Membership Type'
    _order = 'name'

    name = fields.Char('Name')
    price = fields.Float('Price')
    note = fields.Text('Note')


class Membership(models.Model):
    _name = 'afs.membership'
    _description = 'Membership'
    _rec_name = 'aec_membershipID'

    aec_membershipID = fields.Char('Membership ID')
    membership_type_id = fields.Many2one('afs.membership.type', 'Membership Type')
    price = fields.Float('Price')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    description = fields.Text('Description')
    state = fields.Selection([('active', 'Active'),
                              ('expired', 'Expired')], string='Status', compute='_compute_membership_state')
    line_ids = fields.One2many('afs.membership.line', 'membership_id', string='Members')

    def _compute_membership_state(self):
        for rec in self:
            td = fields.Date.today()
            if not rec.end_date:
                rec.state = 'active'
                continue
            rec.state = rec.end_date >= td and 'active' or 'expired'


class MembershipLine(models.Model):
    _name = 'afs.membership.line'
    _description = 'Members'

    membership_id = fields.Many2one('afs.membership', 'Membership', ondelete='cascade')
    name = fields.Char('Membership Number')
    partner_id = fields.Many2one('res.partner', string='Member')
    familyID = fields.Char('Family ID')
    note = fields.Char('Comment')
