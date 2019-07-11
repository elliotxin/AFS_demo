from odoo import models, fields, api, exceptions
from odoo.exceptions import RedirectWarning, UserError, ValidationError


class AfsModelMapping(models.Model):
    _name = 'table.mapping'
    _description = 'Model Mapping for Arc En Ciel'

    name = fields.Char('Name')
    model_id = fields.Many2one('ir.model', string='Model')
    aec_object_name = fields.Char('AEC Object Name')
    line_ids = fields.One2many('table.mapping.line', 'map_id', string='Line')


class AfsModelMappingLine(models.Model):
    _name = 'table.mapping.line'
    _description = 'Model Mapping Line'

    map_id = fields.Many2one('afs.table.mapping', string='Model', ondelete='cascade')
    field_id = fields.Many2one('ir.model.fields', 'Field')
    aec_field_name = fields.Char('AEC field name')
