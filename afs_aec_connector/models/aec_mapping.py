import requests
from odoo import models, fields, api, exceptions
from odoo.exceptions import RedirectWarning, UserError, ValidationError


class ModelMapping(models.Model):
    _name = 'table.mapping'
    _description = 'Model Mapping for Arc En Ciel'

    name = fields.Char('Mapping Name')
    model_id = fields.Many2one('ir.model', string='Model')
    aec_object_name = fields.Char('AEC Object Name')
    line_ids = fields.One2many('table.mapping.line', 'map_id', string='Line')
    pre_action_id = fields.Many2one('ir.actions.server', string='Pre Processing',
                                    domain=[('model_id.model', '=', 'connector.setting')])
    post_action_id = fields.Many2one('ir.actions.server', string='Post Processing')

    def get_key_field(self):
        """
        from a singleton, search the field that is used to map one external record to one odoo record
        :return:
        """
        self.ensure_one()
        selected_id = self.line_ids.filtered(lambda r: r.uniqueID)
        if len(selected_id) > 1:
            raise UserError('more than one key field found on mapping %s' % self.name)
        if len(selected_id) == 0:
            return False
        selected_id = selected_id[0]
        res = (selected_id.aec_field_name, selected_id.field_id)
        return res


class ModelMappingLine(models.Model):
    _name = 'table.mapping.line'
    _description = 'Model Mapping Line'

    map_id = fields.Many2one('table.mapping', string='Model', ondelete='cascade')
    field_id = fields.Many2one('ir.model.fields', 'Odoo Field')
    aec_field_name = fields.Char('AEC field name')
    uniqueID = fields.Boolean('Unique ID')
    mapping_id = fields.Many2one('table.mapping', string='Structured Field Mapping')


class IrModelFields(models.Model):
    _inherit = 'ir.model.fields'

    def name_get(self):
        result = []
        for record in self:
            if self.env.context.get('custom_name', True):
                result.append((record.id, record.name))
            else:
                result.append((record.id, record.field_description))
        return result
