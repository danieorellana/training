# -*- coding: utf-8 -*-
{
    'name': 'Academia',
    'summary': 'Módulo de ejemplo de la capacitación técnica básica en Odoo',
    'description': """
Módulo de ejemplo de RG Ingenieros
==================================
Reúne los ejemplos de la capacitación:

* Modelos nuevos (_name) y extendidos (_inherit)
* Tipos de campos, relaciones y restricciones
* Métodos ORM: search, create, write, unlink
* Botones con acciones
* Vistas: tree, form, kanban, search, calendar y graph
* Gestión de permisos: grupos, acceso a modelos y reglas de registro
* Controladores JSON y HTML
* Reporte PDF con QWeb
""",
    'author': 'RG Ingenieros',
    'website': 'https://rgingenierossv.odoo.com',
    'category': 'Education',
    'version': '15.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['base', 'web'],
    'data': [
        # Primero la seguridad: los grupos deben existir antes que los accesos
        'security/academia_security.xml',
        'security/ir.model.access.csv',
        # Vistas, acciones y menús
        'views/curso_views.xml',
        'views/sesion_views.xml',
        'views/res_partner_views.xml',
        'views/menus.xml',
        # Plantilla HTML del controlador y reporte QWeb
        'views/templates.xml',
        'report/curso_report.xml',
    ],
    'demo': [
        'data/demo.xml',
    ],
    'installable': True,
    'application': True,
}
