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
                              ('expired', 'Expired')], string='Status', default='active')
    line_ids = fields.One2many('afs.membership.line', 'membership_id', string='Members')

    @api.model
    def update_membership_state(self):
        td = fields.Date.today()
        membership_id_to_expire_id = self.env['afs.membership'].search([('state', '=', 'active'), ('end_date', '<', td)])
        membership_id_to_expire_id.write({'state': 'expired'})


class MembershipLine(models.Model):
    _name = 'afs.membership.line'
    _description = 'Members'

    membership_id = fields.Many2one('afs.membership', 'Membership', ondelete='cascade')
    name = fields.Char('Membership Number')
    partner_id = fields.Many2one('res.partner', string='Member')
    familyID = fields.Char('Family ID')
    price = fields.Float('Price')
    comment = fields.Char('Comment')
    start_date = fields.Date(related='membership_id.start_date', readonly=True)
    end_date = fields.Date(related='membership_id.end_date', readonly=True)
    membership_type_id = fields.Many2one(related='membership_id.membership_type_id')
