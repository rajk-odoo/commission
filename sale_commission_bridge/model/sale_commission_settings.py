from odoo import api, fields, models
from odoo.exceptions import UserError

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_sale_commission = fields.Boolean(string="Enable Sales Commission")
