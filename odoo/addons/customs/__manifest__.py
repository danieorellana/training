# -*- coding: utf-8 -*-
{
    'name': 'Customs',
    'summary': 'Módulo de ejemplo de RG Ingenieros',
    'description': """
Módulo de ejemplo de RG Ingenieros
==================================
""",
    'author': 'RG Ingenieros',
    'website': 'https://rgingenierossv.odoo.com',
    'category': '',
    'version': '15.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['base', 'stock'],
    'data': [
        # Primero la seguridad: los grupos deben existir antes que los accesos
        'views/customs.xml',
        'reports/products_info.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
}
