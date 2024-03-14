from odoo import api, fields, models
from odoo.exceptions import UserError

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_commission_bridge = fields.Boolean(string="Enable Sales Commission", store=True)

    @api.onchange('sale_commission_bridge')
    def onchange_sale_commission_bridge(self):
        if self.sale_commission_bridge:
            self.install_commission_module()

    def install_commission_module(self):
        module_commission = self.env['ir.module.module'].search([('name', '=', 'commission')], limit=1)
        if not module_commission:
            raise UserError("Commission module not found.")
        if module_commission.state != 'installed':
            module_commission.button_immediate_install()

