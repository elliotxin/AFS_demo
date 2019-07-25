# Copyright 2019 ALitec Pte Ltd
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Membership Module for Alliance Francaise Singapore',
    'version': '12.0.0.0.8',
    'category': 'AFS',
    'author': 'Alitec Pte Ltd',
    'license': 'AGPL-3',
    'summary': 'Membership module',
    'data': [
        'views/partner.xml',
        'views/menu.xml',
        'views/membership.xml',
        'security/ir.model.access.csv',
        'data/ir.cron.xml'
    ],
    'depends': ['base', 'afs_master'],
    'installable': True,
}
