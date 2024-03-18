from odoo import fields, models, api
from datetime import datetime

class SalesCommissionsModel(models.Model):
    _name = 'sales.targets'
    _description = 'Sales Targets'
    QUARTER_SELECTION = [
        ('Q1', 'Q1'),
        ('Q2', 'Q2'),
        ('Q3', 'Q3'),
        ('Q4', 'Q4'),
    ]
    quarter_period = fields.Selection(QUARTER_SELECTION, string="Quarter", required=True)
    quarter_start_date = fields.Date(string="Start Date", compute='_compute_dates', store=True)
    quarter_end_date = fields.Date(string="End Date", compute='_compute_dates', store=True)
    target_amount = fields.Integer(string="Amount")
    commission_plan_id = fields.Many2one('sales.commissions.plans')
    
    @api.depends('quarter_period')
    def _compute_dates(self):
        for record in self:
            current_year = datetime.now().year
            if record.quarter_period == 'Q1':
                record.quarter_start_date = datetime(current_year, 1, 1)
                record.quarter_end_date = datetime(current_year, 3, 31)
            elif record.quarter_period == 'Q2':
                record.quarter_start_date = datetime(current_year, 4, 1)
                record.quarter_end_date = datetime(current_year, 6, 30)
            elif record.quarter_period == 'Q3':
                record.quarter_start_date = datetime(current_year, 7, 1)
                record.quarter_end_date = datetime(current_year, 9, 30)
            elif record.quarter_period == 'Q4':
                record.quarter_start_date = datetime(current_year, 10, 1)
                record.quarter_end_date = datetime(current_year, 12, 31)
