# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name" : "Stop Auto Lot Allocation on Delivery Order",
    "version" : "13.0.0.2",
    "category" : "Warehouse",
    'summary': 'This App for allow manually lot selection on delivery order select lot number manually stop automatic lot number allocation on delivery stop auto lot selection on picking select lot number manually on picking stop auto lot selection on delivery order',
    "description": """
    
                stop auto lot,
                stop auto lot on stock,
                stop auto lot on delivery order,
                stop auto selection lot number,
                stop auto selection lot number on delivery order,
    
    """,
    "author": "BrowseInfo",
    "website" : "https://www.browseinfo.in",
    "price": 39,
    "currency": 'EUR',
    "depends" : ['base','stock','stock_account','sale_stock','sale_management'],
    "data": [
            'views/picking_inherit.xml',
            ],
    'qweb': [],
    "auto_install": False,
    "installable": True,
    "live_test_url":'https://youtu.be/l_w3XxRqvZQ',
    "images":["static/description/Banner.png"],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
