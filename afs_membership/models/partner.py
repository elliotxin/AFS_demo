from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    membership_ids = fields.Many2many('afs.membership', 'list_member', 'member', 'membership', string='Membership(s)')
    membership_type_id = fields.Many2one('afs.membership.type', 'Membership Name')

