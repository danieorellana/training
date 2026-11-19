from odoo import fields, models, api

class Temario(models.Model):
    _name = 'academia.temario'
    _description = 'Temario de un curso'

    name = fields.Char(string='Nombre')
    curso_id = fields.Many2one(comodel_name="academia.curso", string="Curso")
    descripcion = fields.Text(string='Descripción')