# -*- coding: utf-8 -*-
from odoo import fields, models


class Sesion(models.Model):
    _name = 'academia.sesion'
    _description = 'Sesión de un curso'
    _order = 'fecha, id'

    name = fields.Char(string='Nombre', required=True)
    # Many2one: lado "muchos" de la relación con academia.curso.
    # ondelete='cascade' borra las sesiones si se borra el curso.
    curso_id = fields.Many2one(
        'academia.curso', string='Curso', required=True, ondelete='cascade')
    fecha = fields.Datetime(string='Fecha y hora', default=fields.Datetime.now)
    duracion = fields.Float(string='Duración (horas)', default=1.0)
    # Campo relacionado: lee un valor del curso
    instructor_id = fields.Many2one(
        related='curso_id.instructor_id', string='Instructor', store=True)
