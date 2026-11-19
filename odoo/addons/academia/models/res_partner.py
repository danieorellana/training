# -*- coding: utf-8 -*-
from odoo import fields, models


class Partner(models.Model):
    """Ejemplo de EXTENSIÓN de un modelo existente con _inherit.

    No se crea una tabla nueva: se agregan columnas a res_partner.
    """
    _inherit = 'res.partner'

    es_instructor = fields.Boolean(string='Es instructor')
    curso_instructor_ids = fields.One2many(
        'academia.curso', 'instructor_id', string='Cursos que imparte')
