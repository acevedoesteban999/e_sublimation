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
        compute="_compute_product_product_id"
    )
    price_extra = fields.Monetary(default=0.0)
    currency_id = fields.Many2one(
        related='product_tmpl_id.currency_id',
        depends=['product_tmpl_id'],
    )
    file = fields.Binary()

    def _compute_product_product_id(self):
        for rec in self:
            try:
                rec.product_product_id = self.env['product.template'].filtered(lambda p: p.sublimation_id == rec.id)[0]
            except:
                rec.product_product_id = False

    def create(self, vals):
        rec = super().create(vals)
        
        self.env['product.product'].create({
            'name': rec.product_tmpl_id.name + " " + rec.name,
            'sublimation_id': rec.id,
            'default_code': f'SUB-{rec.id}',
            'lst_price': rec.product_tmpl_id.list_price + rec.price_extra,
        })
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