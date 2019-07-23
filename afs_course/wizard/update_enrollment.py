from odoo import models, fields, api, exceptions
from odoo.exceptions import RedirectWarning, UserError, ValidationError


class UpdateEnrollment(models.TransientModel):
    _name = 'update.enrollment.partner'
    _description = 'Update the enrollment information on partner'

    date_from = fields.Date('Date from')
    date_to = fields.Date('Date to')

    @api.multi
    def sync_enrollment(self):
        partner_id = self.env['course.participant'].search([(1, '=', 1)]).mapped('student_id')
        partner_id.update_partner_enrollment(date_from=self.date_from, date_to=self.date_to)
