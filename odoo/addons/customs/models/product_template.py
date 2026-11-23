from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    notas_fabricante = fields.Text(string='Notas del fabricante', help='Notas o comentarios del fabricante del producto.')
    notas_cliente = fields.Text(string='Notas del cliente', help='Notas o comentarios del cliente sobre el producto.')