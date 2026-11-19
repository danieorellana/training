# -*- coding: utf-8 -*-
from odoo import http
from odoo.exceptions import AccessError, ValidationError
from odoo.http import request


class CursoController(http.Controller):
    """Ejemplos de controladores: respuestas JSON y HTML.

    Nota: en Odoo 19 type='json' pasa a llamarse type='jsonrpc'.
    """

    # ------------------------------------------------------------------
    # JSON: envío de datos
    # Probar desde la consola del navegador, con sesión iniciada:
    #   fetch('/api/cursos', {method: 'POST',
    #     headers: {'Content-Type': 'application/json'},
    #     body: JSON.stringify({jsonrpc: '2.0', params: {}})})
    #   .then(r => r.json()).then(console.log)
    # ------------------------------------------------------------------
    @http.route('/api/cursos', type='json', auth='user')
    def listar(self, estado=None):
        dominio = [('estado', '=', estado)] if estado else []
        # search_read(): busca y devuelve una lista de diccionarios
        return request.env['academia.curso'].search_read(
            dominio, ['name', 'horas', 'estado', 'instructor_id', 'total_alumnos'])

    # ------------------------------------------------------------------
    # JSON: recepción de datos
    #   body: {"jsonrpc": "2.0", "params": {"name": "QWeb", "horas": 3}}
    # ------------------------------------------------------------------
    @http.route('/api/cursos/crear', type='json', auth='user', methods=['POST'])
    def crear(self, name, horas=4.0, **kwargs):
        try:
            curso = request.env['academia.curso'].create({
                'name': name,
                'horas': float(horas),
            })
        except (ValidationError, AccessError) as error:
            return {'ok': False, 'error': str(error)}
        return {'ok': True, 'id': curso.id, 'name': curso.name}

    # ------------------------------------------------------------------
    # HTML: página pública que renderiza una plantilla QWeb
    #   Abrir en el navegador: http://localhost:8069/cursos
    # ------------------------------------------------------------------
    @http.route('/cursos', type='http', auth='public')
    def pagina(self, **kwargs):
        # sudo(): el usuario público no tiene permisos sobre el modelo.
        # Úsalo solo para datos que de verdad pueden ser públicos.
        cursos = request.env['academia.curso'].sudo().search(
            [('estado', '!=', 'borrador')])
        return request.render('academia.cursos_page', {'cursos': cursos})

    # ------------------------------------------------------------------
    # HTML: recepción de un parámetro desde la URL
    #   http://localhost:8069/cursos/1
    # ------------------------------------------------------------------
    @http.route('/cursos/<int:curso_id>', type='http', auth='public')
    def detalle(self, curso_id, **kwargs):
        curso = request.env['academia.curso'].sudo().browse(curso_id).exists()
        if not curso or curso.estado == 'borrador':
            return request.not_found()
        return request.render('academia.curso_detalle_page', {'curso': curso})
