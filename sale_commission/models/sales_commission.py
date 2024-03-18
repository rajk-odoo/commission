from odoo import fields, models, api

class SalesCommissionsModel(models.Model):
    _name = 'sales.commissions'
    _description = 'Sales Commissions'
    min_achievement = fields.Float(string="Min. Achievement")
    commission_rate = fields.Float(string="Commission")
    commission_plan_id = fields.Many2one('sales.commissions.plans')
