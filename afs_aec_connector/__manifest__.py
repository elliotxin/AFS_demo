# Copyright 2019 ALitec Pte Ltd
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Arc en Ciel connector for Alliance Francaise Singapore',
    'version': '12.0.0.0.04',
    'category': 'AFS',
    'author': 'Alitec Pte Ltd',
    'license': 'AGPL-3',
    'summary': 'Arc En Ciel Connector',
    'data': [
            'security/ir.model.access.csv',
            'views/menu.xml',
            'views/model_mapping.xml',
            'views/connector_setting.xml',
            'views/synchronisation.xml',
            'data/initial_import.xml'
    ],
    'depends': ['afs_master'],
    'installable': True,
}
