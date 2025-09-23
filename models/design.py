from odoo import fields, models , api

class SublimationDesign(models.Model):
    _name = 'sublimation.design'
    _description = 'Diseño de Sublimación'

    name = fields.Char(string='Nombre del diseño',required=True)
    image = fields.Binary(string='Imagen del diseño')
    product_tmpl_id = fields.Many2one('product.template', string='Producto base',required=True)
    attribute_line_ids = fields.One2many('sublimation.attribute', 'design_id', string='Atributos')
    total_attribute_line = fields.Integer(
        string='Total de Variantes',
        compute='_compute_total_attribute_line',
        store=True,
    )
    product_product_ids = fields.One2many(
        'product.product',
        'sublimation_design_id',
        string='Variantes generadas',
    )

    @api.depends('attribute_line_ids')
    def _compute_total_attribute_line(self):
        for rec in self:
            rec.total_attribute_line = len(rec.attribute_line_ids)


    def _get_or_create_variant(self, value_ids):
        """
        :param value_ids: lista de IDs de `product.attribute.value`
        :return: product.product record (creado o existente)
        """
        self.ensure_one()

        # 1. Buscamos si ya existe la variante con esos valores
        existing = self.product_tmpl_id.product_variant_ids.filtered(
            lambda p: set(p.product_template_attribute_value_ids.product_attribute_value_id.ids) == set(value_ids)
        )
        if existing:
            return existing[0]

        # 2. Nos aseguramos de que la plantilla tenga esas líneas de atributo
        for value in self.env['product.attribute.value'].browse(value_ids):
            line = self.product_tmpl_id.attribute_line_ids.filtered(
                lambda l: l.attribute_id == value.attribute_id
            )
            if not line:
                self.product_tmpl_id.attribute_line_ids = [
                    fields.Command.create({
                        'attribute_id': value.attribute_id.id,
                        'value_ids':      [(4, value.id)],
                    })
                ]
            else:
                if value.id not in line.value_ids.ids:
                    line.value_ids = [(4, value.id)]

        # 3. Creamos la variante
        return self.env['product.product'].create({
            'product_tmpl_id': self.product_tmpl_id.id,
            'product_template_attribute_value_ids': [
                fields.Command.create({'product_attribute_value_id': v}) for v in value_ids
            ],
            'sublimation_design_id': self.id,
        })