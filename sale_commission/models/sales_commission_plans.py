from odoo import fields, models, api
from odoo.exceptions import ValidationError

class SalesCommissionsPlans(models.Model):
    _name = "sales.commissions.plans"
    _description = "Sales Commission Plans"
    name = fields.Char(string="Commission Plan", required=True)
    start_date = fields.Date(required=True, default=fields.date.today())
    end_date = fields.Date(required=True)
    target = fields.Integer(string="Target", compute="_compute_total_target")
    active = fields.Boolean(default=True)
    stage = fields.Selection([('draft', "Draft"), ('approved', "Approved"), ('done', "Done"), ('cancelled', "Cancelled")], default="draft")
    product_ids = fields.Many2many('product.product', string="Products")
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    team_id = fields.Many2one('crm.team', string="Sales Team", required=True)
    salesperson_id = fields.Many2one('res.users', string="Salesperson")
    commissions_ids = fields.One2many('sales.commissions', 'commission_plan_id', string="Commissions")
    target_ids = fields.One2many('sales.targets', 'commission_plan_id', string="Targets")

    @api.depends('target_ids.target_amount')
    def _compute_total_target(self):
        for plan in self:
            plan.target = sum(plan.target_ids.mapped('target_amount'))

    def _check_stage(self, disallowed_stages):
        for plan in self:
            if plan.stage in disallowed_stages:
                raise ValidationError(f"This operation is not allowed on commission plans in {', '.join(disallowed_stages)} stage(s).")

    def action_stage_approve(self):
        self._check_stage(['cancelled', 'approved', 'done'])
        self.stage = 'approved'

    def action_stage_cancelled(self):
        self._check_stage(['done'])
        self.stage = 'cancelled'
