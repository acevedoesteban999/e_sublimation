# -*- coding: utf-8 -*-
{
    'name': 'E-Sublimation',
    'version': '1.0.0',
    'summary': """ E-Sublimation Summary """,
    'author': 'acevedoesteban999@gmail.com',
    'website': '',
    'category': '',
    'depends': ['base', 'product'],
    "data": [
        "security/ir.model.access.csv",
        
        "data/data.xml",

        "views/sublimation.xml",
        "views/product_template.xml",
        
        "views/menu.xml",
    ],
    
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
