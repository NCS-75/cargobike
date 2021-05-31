from odoo import fields, models

class ResCompany(models.Model):
    _inherit = "res.company"

    bg_image = fields.Many2one('ir.attachment',string="Background Image",help="Attach Background Image")
