import requests
from odoo import models, fields, api, exceptions
from odoo.tools.profiler import profile
import logging
from odoo.exceptions import RedirectWarning, UserError, ValidationError
_logger = logging.getLogger(__name__)


class ConnectorSetting(models.Model):
    _name = 'connector.setting'
    _description = 'Connector Settings'
    _order = 'sequence,name,id'
    _rec_name = 'mapping_id'

    name = fields.Char('Object Name (in url)')
    data_name = fields.Char('Data name (in response)')
    end_point = fields.Char('url end point')
    api_key = fields.Char('API Key')
    date_filter = fields.Datetime('Date from')
    date_filter_to = fields.Datetime('Date to')
    mapping_id = fields.Many2one('table.mapping', 'Mapping')
    note = fields.Text('Note')
    sequence = fields.Integer('Sequence', default=10)
    loop = fields.Boolean('Loop', default=True, help='Uncheck to run only a single page')
    loop_count = fields.Integer('Number of Pages')

    @api.multi
    def action_get(self):
        test = self._context.get('test', False)
        self.ensure_one()
        url = "/".join([self.end_point, self.name])
        base_url = self.date_filter and "/".join([url, fields.Datetime.to_string(self.date_filter)]) or url
        api_key = self.api_key
        headers = {'api_key': api_key}

        total_loop = 1
        payload = {'page': total_loop}
        if self.date_filter_to:
            payload['modifiedTo'] = self.date_filter_to

        next_ok = True
        while next_ok and total_loop <= 4000:
            res = requests.get(base_url, headers=headers, params=payload)

            data_list = res.json()[self.data_name]
            next_page = res.json()['pagging']['next']
            self.write({'note': data_list})

            ctx = {'active_id': self.id,
                   'active_model': 'connector.setting'}
            action_id = self.with_context(ctx).mapping_id.pre_action_id
            action_id.run()

            if not test:
                # updated_data = eval(self.note)
                updated_data = data_list
                self.process_list(updated_data)
            self.env.cr.commit()

            next_ok = len(next_page) > 0
            total_loop += 1
            payload['page'] = total_loop

        self.write({'loop_count': total_loop-1})
        return

    @api.multi
    def action_test(self):
        return self.with_context(test=True).action_get()

    def process_list(self, data_list):
        self.ensure_one()

        if not self.mapping_id or not self.mapping_id.model_id:
            raise UserError('object %s is badly mapped' % self.name)
        mapping_id = self.mapping_id
        model_name = mapping_id.model_id.model

        unique_line = mapping_id.line_ids.filtered(lambda r: r.uniqueID)
        if len(unique_line) > 1:
            raise UserError('object %s has more than one unique identifier' % self.name)

        # external_name is the name of the field in the external system
        # field_name is the name of the field in odoo

        if len(unique_line) == 1:
            external_key_external_name = unique_line.aec_field_name
            external_key_field_name = unique_line.field_id.name

            for record_vals in data_list:
                domain = [(external_key_field_name, '=', record_vals[external_key_external_name])]
                to_update = self.env[model_name].search(domain)
                if len(to_update) == 0:
                    self.create_record(record_vals, mapping_id)
                else:
                    self.update_record(record_vals, to_update[0], mapping_id)
        else:
            for record_vals in data_list:
                self.create_record(record_vals, mapping_id)

    @api.model
    def create_record(self, record_vals, mapping_id):
        model_name = mapping_id.model_id.model
        vals = {}
        for key, val in record_vals.items():
            vals = self.mapping_field(mapping_id, vals, (key, val))
        odoo_rec_id = self.env[model_name].create(vals)
        ctx = {'active_id': odoo_rec_id.id,
               'active_model': model_name}
        action_id = self.with_context(ctx).mapping_id.post_action_id
        action_id.run()

    @api.model
    def update_record(self, record_vals, record_id, mapping_id):
        model_name = mapping_id.model_id.model
        odoo_rec_id = record_id
        vals = {}
        for key, val in record_vals.items():
            vals = self.mapping_field(mapping_id, vals, (key, val), odoo_rec_id)
        odoo_rec_id.write(vals)
        ctx = {'active_id': odoo_rec_id.id,
               'active_model': model_name}
        action_id = self.with_context(ctx).mapping_id.post_action_id
        action_id.run()

    @api.model
    def mapping_field(self, mapping_id, input_dict, vals_to_map, odoo_rec_id=False):
        """
        :param mapping_id is the mapping record
        :param input_dict: {key: val} where key = name of the field in odoo
        :param vals_to_map: tuple(key, value) where key is the external_name of the field, and value the value to be inserted in the inpput_dict
        :return: the result is the input_dict with added key2: values, where key2 is the odoo field name
        """

        external_name = vals_to_map[0]
        value = vals_to_map[1]
        line_id = mapping_id.line_ids.filtered(lambda r: r.aec_field_name == external_name)
        if len(line_id) == 0:
            return input_dict
        elif len(line_id) > 1:
            raise UserError('External field %s is mapped more than once' % external_name)
        field_name = line_id.field_id and line_id.field_id.name or False
        field_type = field_name and line_id.field_id.ttype or False

        # if the external field is mapped to a simple odoo field (same type !!)
        if field_name and not line_id.mapping_id:
            input_dict[field_name] = value

        # if the external field is mapped as a many2one to an odoo record
        if field_type == 'many2one':
            model_name = line_id.mapping_id.model_id and line_id.mapping_id.model_id.model or False
            if not model_name:
                raise UserError('no model defined for %s in the mapping %s' % (external_name, line_id.mapping_id.name))

            # Find the odoo record corresponding to the external key
            index_line_id = line_id.mapping_id.line_ids and line_id.mapping_id.line_ids.filtered(lambda r: r.aec_field_name == external_name)
            odoo_field_name = index_line_id and index_line_id.field_id and index_line_id.field_id.name or False
            if not odoo_field_name:
                raise UserError('Field %s is not correctly mapped' % external_name)

            search_domain = [(odoo_field_name, '=', value)]
            record_id = self.env[model_name].search(search_domain)

            # if there is no odoo record
            if len(record_id) == 0:
                return input_dict

            # if more than one odoo record are found, generate an error
            if len(record_id) > 1:
                raise UserError(
                    'duplicated entry for a %s = %s - it should be unique' % (field_name, value[external_name]))

            # one odoo record is found, pass it in the result dictionary
            record_id = record_id[0]
            input_dict[field_name] = record_id.id

        # if the external field is linked as a many2many to a odoo field
        if field_type == 'many2many':
            if not isinstance(value, list):
                raise UserError('the field %s is not a list' % external_name)
            sub_mapping_id = line_id.mapping_id
            sub_model_name = sub_mapping_id.model_id and sub_mapping_id.model_id.model or False
            if not sub_model_name:
                raise UserError('mapping %s is not linked to a odoo model' % sub_mapping_id.name)
            key = sub_mapping_id.get_key_field()
            aec_field_name = key[0]
            odoo_field_id = key[1]

            vals = []
            for list_item in value:
                external_value = aec_field_name in list_item and list_item[aec_field_name] or False
                if not external_value:
                    continue
                domain = [(odoo_field_id.name, '=', external_value)]
                mapped_record_id = self.env[sub_model_name].search(domain, limit=1)
                if len(mapped_record_id) == 1:
                    vals.append((4, mapped_record_id.id, 0))
                else:
                    val_dct = {}
                    for k, v in list_item.items():
                        val_dct = self.mapping_field(sub_mapping_id, val_dct, (k, v))
                    vals.append((0, 0, val_dct))

            input_dict[field_name] = vals

        # if the external field is synced to a one2many field - all the one2many are created
        if field_type == 'one2many':
            if not isinstance(value, list):
                raise UserError('the field %s is not a list' % external_name)
            sub_mapping_id = line_id.mapping_id
            sub_model_name = sub_mapping_id.model_id and sub_mapping_id.model_id.model or False
            if not sub_model_name:
                raise UserError('mapping %s is not linked to a odoo model' % sub_mapping_id.name)
            vals = []
            for list_item in value:
                val_dct = {}
                for k, v in list_item.items():
                    val_dct = self.mapping_field(sub_mapping_id, val_dct, (k, v))
                vals.append((0, 0, val_dct))

            # delete all existing one2many records
            if odoo_rec_id:
                to_delete_id = odoo_rec_id.mapped(field_name)
                to_delete_id.unlink()

            input_dict[field_name] = vals

        # if the external field is not mapped to a single odoo field, instead mapped as a list of fields (in the same model)
        if not field_name and line_id.mapping_id:
            if not isinstance(value, dict):
                raise UserError('the field %s is not a structured data' % external_name)
            for key, val in value.items():
                input_dict = self.mapping_field(line_id.mapping_id, input_dict, (key, val))

        return input_dict

