import requests
from odoo import models, fields, api, exceptions
from odoo.exceptions import RedirectWarning, UserError, ValidationError


class ConnectorSetting(models.Model):
    _name = 'connector.setting'
    _description = 'Connector Settings'

    name = fields.Char('Object Name')
    end_point = fields.Char('url end point')
    api_key = fields.Char('API Key')
    date_filter = fields.Datetime('Date filter')
    note = fields.Text('Note')

    @api.multi
    def action_get(self):
        self.ensure_one()
        url = "/".join([self.end_point, self.name])
        url = self.date_filter and "/".join([url, 'updated', fields.Datetime.to_string(self.date_filter)]) or url
        api_key = self.api_key
        headers = {'api_key': api_key}
        res = requests.get(url, headers=headers)
        self.write({'note': res.json()[self.name]})
        return


class ModelMapping(models.Model):
    _name = 'table.mapping'
    _description = 'Model Mapping for Arc En Ciel'

    name = fields.Char('Name')
    model_id = fields.Many2one('ir.model', string='Model')
    aec_object_name = fields.Char('AEC Object Name')
    line_ids = fields.One2many('table.mapping.line', 'map_id', string='Line')


class ModelMappingLine(models.Model):
    _name = 'table.mapping.line'
    _description = 'Model Mapping Line'

    map_id = fields.Many2one('afs.table.mapping', string='Model', ondelete='cascade')
    field_id = fields.Many2one('ir.model.fields', 'Field')
    aec_field_name = fields.Char('AEC field name')
