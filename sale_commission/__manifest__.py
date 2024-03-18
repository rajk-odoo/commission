{
    'name' : "Sales Commission",
   'version' : "1.0",
   'summary' : "Track and manage sales commissions for sales teams.",
    'depends': ['sale', 'sale_management'],
    'data': [      
        'security/ir.model.access.csv',
        'views/sales_commission_plan_report_views.xml',
        'views/sales_targets_view.xml',  
        'views/sales_commissions_view.xml',   
        'views/sales_commission_plans_views.xml',
        'views/sales_commission_menu.xml',
        'views/sale_order_line.xml',
    ],
    'installable' : True,
    'auto_install' : False,
    'license' : "LGPL-3",
}
