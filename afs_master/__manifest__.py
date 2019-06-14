# Copyright 2019 ALitec Pte Ltd
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Partner Data for Alliance Francaise Singapore',
    'version': '12.0.0.0.1',
    'category': 'Membership',
    'author': 'Alitec Pte Ltd',
    'license': 'AGPL-3',
    'summary': 'Customisation on partner data model',
    'data': [
        'views/partner_base.xml',
        'views/menu.xml',
    ],
    'depends': ['partner_address_street3', 'partner_firstname'],
    'installable': True,
}
