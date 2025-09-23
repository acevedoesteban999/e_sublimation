# models/sublimation_sublimation.py
from odoo import api, fields, models


class SublimationSublimation(models.Model):
    _name = 'sublimation.sublimation'
    _description = 'Sublimación'

    name = fields.Char(required=True)
    image = fields.Binary(attachment=True)
    product_tmpl_id = fields.Many2one(
        'product.template',
        required=True,
        ondelete='cascade',
        string='Plantilla base',
    )
    product_product_id = fields.Many2one(
        'product.product',
        ondelete='cascade',
        string='Variante creada',
    )
    price_extra = fields.Monetary(default=0.0)
    currency_id = fields.Many2one(
        related='product_tmpl_id.currency_id',
        depends=['product_tmpl_id'],
    )
    file = fields.Binary()

    @api.model
    def create(self, vals):
        rec = super().create(vals)
        if rec.product_tmpl_id.product_variant_count > 1:
            variant = self.env['product.product'].create({
                'product_tmpl_id': rec.product_tmpl_id.id,
                'default_code': f'SUB-{rec.id}',
                'lst_price': rec.product_tmpl_id.list_price + rec.price_extra,
                'active': True,
            })
        else: 
            variant = rec.product_product_id.product_variant_id
            variant.update({
                'product_tmpl_id': rec.product_tmpl_id.id,
                'default_code': f'SUB-{rec.id}',
                'lst_price': rec.product_tmpl_id.list_price + rec.price_extra,
                'active': True,
            })

        rec.product_product_id = variant
        return rec

    def write(self, vals):
        res = super().write(vals)
        if 'price_extra' in vals:
            for rec in self:
                rec.product_product_id.lst_price = (
                    rec.product_tmpl_id.list_price + rec.price_extra
                )
        return res

    def unlink(self):
        if self.product_product_id:
            self.product_product_id.unlink()
        return super().unlink()

    def action_open_product_product(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'product.product',
            'res_id': self.product_product_id.id,
            'view_mode': 'form',
            'target': 'current',
        }