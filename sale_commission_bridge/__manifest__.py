{
    "name": "Sale Commission Bridge",
    "category": 'Sale/Settings/Commission',
    'version': '1.0',
    'license': 'LGPL-3',
    'summary': 'Bridge Module for sale commission' ,
    'depends': [
        "base",
        "sale_management",
    ],
    "installable" : True,
    "auto_install": True,
    'data' : [
        "views/res_config_settings_inherit.xml",
    ],
}
