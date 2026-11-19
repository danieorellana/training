# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class Curso(models.Model):
    """Ejemplo de CREACIÓN de un modelo nuevo con _name.

    Odoo crea la tabla academia_curso en PostgreSQL.
    """
    _name = 'academia.curso'
    _description = 'Curso'
    _order = 'fecha_inicio desc, name'

    # ------------------------------------------------------------------
    # Campos y sus tipos
    # ------------------------------------------------------------------
    # Char: texto corto
    name = fields.Char(string='Nombre', required=True)
    # Text / Html: texto largo
    descripcion = fields.Text(string='Descripción')
    # Integer / Float: números
    horas = fields.Float(string='Horas', default=4.0)
    color = fields.Integer(string='Color')  # usado por la vista kanban
    # Boolean: sí o no
    active = fields.Boolean(default=True)
    # Date / Datetime: fechas
    fecha_inicio = fields.Date(string='Fecha de inicio', default=fields.Date.context_today)
    fecha_fin = fields.Date(string='Fecha de fin')
    # Selection: lista fija de opciones
    estado = fields.Selection(
        [('borrador', 'Borrador'),
         ('confirmado', 'Confirmado'),
         ('terminado', 'Terminado')],
        string='Estado', default='borrador', required=True)

    # ------------------------------------------------------------------
    # Relaciones entre modelos
    # ------------------------------------------------------------------
    # Many2one: muchos cursos -> un instructor
    instructor_id = fields.Many2one(
        'res.partner', string='Instructor',
        domain=[('es_instructor', '=', True)])
    # Many2one: usado por la regla de registro ("solo mis cursos")
    responsable_id = fields.Many2one(
        'res.users', string='Responsable', default=lambda self: self.env.user)
    # One2many: un curso -> muchas sesiones (inverso de sesion.curso_id)
    sesion_ids = fields.One2many('academia.sesion', 'curso_id', string='Sesiones')
    # Many2many: muchos cursos <-> muchos alumnos
    alumno_ids = fields.Many2many('res.partner', string='Alumnos')

    # Campos calculados (medidas para la vista graph y el smart button)
    total_alumnos = fields.Integer(
        string='Total de alumnos', compute='_compute_totales', store=True)
    sesion_count = fields.Integer(
        string='Número de sesiones', compute='_compute_totales', store=True)

    @api.depends('alumno_ids', 'sesion_ids')
    def _compute_totales(self):
        for curso in self:
            curso.total_alumnos = len(curso.alumno_ids)
            curso.sesion_count = len(curso.sesion_ids)

    # ------------------------------------------------------------------
    # Restricciones
    # ------------------------------------------------------------------
    # Restricción SQL: se valida en la base de datos
    # (En Odoo 19 se escribe con models.Constraint)
    _sql_constraints = [
        ('name_unique', 'unique(name)',
         'Ya existe un curso con ese nombre.'),
    ]

    # Restricción en Python: se valida al crear o modificar
    @api.constrains('horas')
    def _check_horas(self):
        for curso in self:
            if curso.horas <= 0:
                raise ValidationError(_('Horas debe ser mayor a 0.'))

    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_fechas(self):
        for curso in self:
            if curso.fecha_fin and curso.fecha_inicio and curso.fecha_fin < curso.fecha_inicio:
                raise ValidationError(_('La fecha de fin no puede ser anterior a la de inicio.'))

    # ------------------------------------------------------------------
    # Botones (type="object") -> métodos del modelo
    # ------------------------------------------------------------------
    def action_confirmar(self):
        # write(): modificar registros
        self.write({'estado': 'confirmado'})

    def action_terminar(self):
        self.write({'estado': 'terminado'})

    def action_borrador(self):
        self.write({'estado': 'borrador'})

    def action_crear_sesion(self):
        """create(): crea una sesión nueva para cada curso seleccionado."""
        Sesion = self.env['academia.sesion']
        for curso in self:
            numero = curso.sesion_count + 1
            Sesion.create({
                'name': _('Sesión %s', numero),
                'curso_id': curso.id,
                'duracion': 1.0,
            })

    def action_eliminar_sesiones(self):
        """unlink(): elimina las sesiones del curso."""
        for curso in self:
            if curso.estado == 'terminado':
                raise UserError(_('No se pueden eliminar sesiones de un curso terminado.'))
        self.sesion_ids.unlink()

    def action_ver_sesiones(self):
        """Botón que devuelve una acción de ventana (smart button)."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Sesiones'),
            'res_model': 'academia.sesion',
            'view_mode': 'tree,form',
            'domain': [('curso_id', '=', self.id)],
            'context': {'default_curso_id': self.id},
        }

    # ------------------------------------------------------------------
    # Más ejemplos de ORM: búsqueda
    # ------------------------------------------------------------------
    @api.model
    def cursos_largos(self, minimo_horas=10):
        """search(): busca con un dominio. Devuelve un recordset."""
        return self.search([('horas', '>', minimo_horas)], order='horas desc')

    @api.model
    def resumen_por_estado(self):
        """search_count(): cuenta registros sin cargarlos."""
        return {
            estado: self.search_count([('estado', '=', estado)])
            for estado, _etiqueta in self._fields['estado'].selection
        }
