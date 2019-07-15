import requests
from odoo import models, fields, api, exceptions
from odoo.exceptions import RedirectWarning, UserError, ValidationError


class ExtSynchronisation(models.Model):
    _name = 'ext.synchronisation'
    _description = 'External Synchronisation'

    name = fields.Char('Sync Order')
    line_ids = fields.One2many('ext.synchronisation.line', 'sync_id', 'Synced Items')

    @api.multi
    def action_execute(self):
        self.ensure_one()
        for c in self.line_ids:
            c.connector_id.action_get()


class ExtSynchronisationLine(models.Model):
    _name = 'ext.synchronisation.line'
    _description = 'External Synchronisation Item'
    _order = "sequence,id"
    _rec_name = 'connector_id'

    sync_id = fields.Many2one('ext.synchronisation', 'Synchronisation Order', ondelete='cascade')
    sequence = fields.Integer('Sequence', default=10)
    connector_id = fields.Many2one('connector.setting', 'Connection name', required=True)
