import requests
from odoo import models, fields, api, exceptions
from odoo.exceptions import RedirectWarning, UserError, ValidationError
from dateutil.relativedelta import relativedelta


class ExtSynchronisation(models.Model):
    _name = 'ext.synchronisation'
    _description = 'External Synchronisation'

    name = fields.Char('Sync Order')
    line_ids = fields.One2many('ext.synchronisation.line', 'sync_id', 'Synced Items')
    date_from = fields.Datetime('Date from')
    date_to = fields.Datetime('Date to')

    sync_all = fields.Boolean('Sync All')
    stop_date = fields.Datetime('End Date')
    step = fields.Integer('Step in month')
    active = fields.Boolean('Active', default=True)

    @api.multi
    def action_execute(self):
        self.ensure_one()

        if self.sync_all and self.date_to > self.stop_date:
            return

        connector_id = self.line_ids.mapped('connector_id')
        connector_id.write({'date_filter': self.date_from,
                            'date_filter_to': self.date_to})

        for c in self.line_ids:
            c.connector_id.action_get()

        if self.sync_all:
            new_date = self.step and self.date_to + relativedelta(months=self.step) or False
            self.write({'date_from': self.date_to,
                        'date_to': new_date})


class ExtSynchronisationLine(models.Model):
    _name = 'ext.synchronisation.line'
    _description = 'External Synchronisation Item'
    _order = "sequence,id"
    _rec_name = 'connector_id'

    sync_id = fields.Many2one('ext.synchronisation', 'Synchronisation Order', ondelete='cascade')
    sequence = fields.Integer('Sequence', default=10)
    connector_id = fields.Many2one('connector.setting', 'Connection name', required=True)
