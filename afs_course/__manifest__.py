# Copyright 2019 ALitec Pte Ltd
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Courses for Alliance Francaise Singapore',
    'version': '12.0.0.0.5',
    'category': 'AFS',
    'author': 'Alitec Pte Ltd',
    'license': 'AGPL-3',
    'summary': 'Courses.',
    'data': [
            'views/course.xml',
            'views/student.xml',
            'views/session.xml',
            'views/course_participant.xml',
            'views/course_term.xml',
            'views/partner.xml',
            'data/update_enrollment.xml',
            'security/ir.model.access.csv',
            'views/menu.xml',
    ],
    'depends': ['afs_master'],
    'installable': True,
}
