# Copyright 2019 ALitec Pte Ltd
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Partner Data for Alliance Francaise Singapore',
    'version': '12.0.0.0.2',
    'category': 'Membership',
    'author': 'Alitec Pte Ltd',
    'license': 'AGPL-3',
    'summary': 'Customisation on partner data model',
    'data': [
        'views/partner_base.xml',
        'views/company_size.xml',
        'views/partner_job_level.xml',
        'views/staff_view.xml',
        'views/menu.xml',
        'security/ir.model.access.csv'
    ],
    'depends': ['contacts', 'partner_address_street3', 'partner_firstname'],
    'installable': True,
}
