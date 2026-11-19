# Academia — módulo de ejemplo (Odoo 15 Community)

Módulo de práctica de la **Capacitación técnica básica en Odoo** de RG Ingenieros.
Cada tema de la presentación tiene su ejemplo en este módulo.

## Instalación

1. Copia la carpeta `academia` a tu ruta de addons (la que aparece en `addons_path`).
2. Reinicia el servidor de Odoo.
3. Activa el modo desarrollador, ve a **Aplicaciones › Actualizar lista de aplicaciones**.
4. Busca **Academia** e instálala.

Para ver los datos de ejemplo, la base de datos debe haberse creado con datos de demostración.

## Dónde está cada tema de la presentación

| Tema | Archivo |
|---|---|
| Estructura de un módulo | `__manifest__.py`, `__init__.py` |
| Modelo nuevo (`_name`) | `models/curso.py`, `models/sesion.py` |
| Extender un modelo (`_inherit`) | `models/res_partner.py`, `views/res_partner_views.xml` |
| Campos y sus tipos | `models/curso.py` (Char, Text, Float, Integer, Boolean, Date, Selection…) |
| Relaciones Many2one / One2many / Many2many | `models/curso.py`, `models/sesion.py` |
| Restricciones SQL y Python | `models/curso.py` (`_sql_constraints`, `@api.constrains`) |
| Métodos ORM: search, create, write, unlink | `models/curso.py` (métodos `action_*`, `cursos_largos`, `resumen_por_estado`) |
| Estructura XML de vistas | `views/curso_views.xml` |
| Vistas tree, form, kanban, search, calendar, graph | `views/curso_views.xml` |
| Botones y acciones | `views/curso_views.xml` (header y smart button), `views/menus.xml` |
| Grupos, acceso a modelos y reglas de registro | `security/academia_security.xml`, `security/ir.model.access.csv` |
| Controladores JSON y HTML | `controllers/main.py`, `views/templates.xml` |
| Reportes con QWeb | `report/curso_report.xml` |

## Probar los controladores

Con el servidor en `http://localhost:8069`:

- Página HTML pública: `http://localhost:8069/cursos` (muestra cursos confirmados o terminados).
- Detalle: `http://localhost:8069/cursos/<id>`.
- API JSON (con sesión iniciada), desde la consola del navegador:

```js
fetch('/api/cursos', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({jsonrpc: '2.0', params: {estado: 'confirmado'}})
}).then(r => r.json()).then(console.log);

fetch('/api/cursos/crear', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({jsonrpc: '2.0', params: {name: 'Controladores', horas: 2}})
}).then(r => r.json()).then(console.log);
```

## Probar el ORM desde el shell

```bash
./odoo-bin shell -d mi_base
```

```python
Curso = env['academia.curso']
Curso.search([('horas', '>', 10)])                 # buscar
curso = Curso.create({'name': 'Odoo básico 2'})    # crear
curso.write({'horas': 20})                         # modificar
curso.unlink()                                     # eliminar
env.cr.commit()                                    # guardar los cambios del shell
```

## Permisos

- **Academia / Usuario**: ve solo los cursos donde es responsable; no puede eliminar cursos.
- **Academia / Administrador**: ve y elimina todos los cursos. El usuario administrador recibe este grupo al instalar.

## Notas de sintaxis de Odoo 15

- Visibilidad condicional con `attrs="{'invisible': [...]}"`. El atributo `states="..."` solo funciona si el campo se llama `state`; aquí se llama `estado`, por eso se usa `attrs`.
  (Desde Odoo 17 se escribe `invisible="estado != 'borrador'"`.)
- La vista de lista usa `<tree>` (desde Odoo 18 es `<list>`).
- La plantilla kanban se llama `kanban-box`.
- En reportes, clases de Bootstrap 4 (`text-right`).
