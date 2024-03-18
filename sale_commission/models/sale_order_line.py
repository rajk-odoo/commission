from odoo import models, fields,api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    plan = fields.Many2many('sales.commissions.plans', string='Commission Plan')

    def _get_commission_plan(self):
        for line in self:
            product = line.product_id
            plans = self.env['sales.commissions.plans'].search([('product_ids', 'in', product.ids)])
            line.plan = [(6, 0, plans.ids)]

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self._get_commission_plan()
