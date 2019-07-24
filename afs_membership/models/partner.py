from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    membership_ids = fields.One2many('afs.membership.line', 'partner_id', string='Membership(s)')
    membership_type_id = fields.Many2one('afs.membership.type', 'Membership Name')


