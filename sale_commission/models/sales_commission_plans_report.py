from odoo import fields, models, api
from datetime import datetime

class SaleCommissionPlan(models.Model):
    _name = "sales.commissions.plans.report"
    _description = "Sales Commission Plan Reports"
    _sql_constraints = [
        ('check_target_amount_positive', 'CHECK(target_amount >= 0)', 'Target amount must be positive.'), ]
    achieved_amount = fields.Float(default=0, compute='_compute_achieved_amount',store = True)
    target_amount = fields.Float(compute='_compute_target_amount',store = True)
    desired_commission_rate = fields.Float(string="Commission Rate", compute='_compute_desired_commission_rate')
    commission_plan_id = fields.Many2one('sales.commissions.plans', string="Commission Plan")
    target_id = fields.Many2one('sales.targets', string="Target Quarter")
    salesperson_id = fields.Many2one('res.users', string="Salesperson", compute='_compute_record_values')
    team_id = fields.Many2one('crm.team', string="Sales Team", compute='_compute_record_values')
    period = fields.Char(string='Period', compute='_compute_period', store=True)

    @api.depends('commission_plan_id.target_ids.target_amount')
    def _compute_target_amount(self):
        for record in self:
            record.target_amount = sum(record.commission_plan_id.target_ids.mapped('target_amount'))

    @api.depends('commission_plan_id', 'achieved_amount')
    def _compute_desired_commission_rate(self):
        for record in self:
            record.desired_commission_rate = 0
            if record.target_amount != 0:
                achievement_percent = (record.achieved_amount / record.target_amount) * 100
                for commission in record.commission_plan_id.commissions_ids.sorted(key=lambda c: c.min_achievement, reverse=True):
                    if commission.min_achievement <= achievement_percent:
                        record.desired_commission_rate = commission.commission_rate
                        break
    @api.depends('commission_plan_id', 'target_id')
    def _compute_achieved_amount(self):
        for record in self:
            price_line = self.env['sale.order.line'].search([
                ('plan.id', '=', record.commission_plan_id.id),
                ('order_id.user_id', 'in', [record.commission_plan_id.salesperson_id.id]),
                ('order_id.date_order', '>=', record.target_id.quarter_start_date),
                ('order_id.date_order', '<=', record.target_id.quarter_end_date),
            ])
            record.achieved_amount = sum(order.price_total for order in price_line)
    

    @api.depends('salesperson_id', 'commission_plan_id')
    def _compute_record_values(self):
        for record in self:
            record.salesperson_id = record.commission_plan_id.salesperson_id
            record.team_id = record.commission_plan_id.team_id
    
    @api.depends('target_id.quarter_period')
    def _compute_period(self):
        for record in self:
            current_year = datetime.now().year
            record.period = f'{record.target_id.quarter_period} {current_year}'
           
