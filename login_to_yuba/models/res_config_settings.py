from odoo import api, fields, models

class ResConfigSettingsYuba(models.TransientModel):
    _inherit = 'res.config.settings'
    
    bg_image = fields.Many2one('ir.attachment', related="company_id.bg_image", string="Background Image",help="Attach background Image", readonly=False)