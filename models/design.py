from odoo import fields, models , api

class SublimationDesign(models.Model):
    _name = 'sublimation.design'
    _description = 'Diseño de Sublimación'

    name = fields.Char(string='Nombre del diseño',required=True)
    image = fields.Binary(string='Imagen del diseño')
    product_tmpl_id = fields.Many2one('product.template', string='Producto base',required=True)
    product_product_id = fields.Many2one('product.product',string='Variante generada')
    
    price_extra = fields.Monetary(string="Extra Price",currency_field='currency_id',default=0.0)
    currency_id = fields.Many2one('res.currency',related='product_tmpl_id.currency_id')
    attch = fields.Binary("Adjunto")
    

    def action_open_product_product(self):       
        return {
            'type': 'ir.actions.act_window',
            'name': 'Producto Variante',
            'res_model': 'product.product',
            'res_id': self.product_product_id.id,
            'view_mode': 'form',
            'view_id': self.env.ref('product.product_variant_easy_edit_view').id,
            'target': 'current',
        }
    
    def create(self, vals_list):
        rec = super().create(vals_list)
        product_product = self.env['product.product'].create({
            'product_tmpl_id':rec.product_tmpl_id.id,
            'price_extra':rec.price_extra,
        })
        rec.product_product_id = product_product.id
        return rec

    def write(self, vals):
        if 'price_extra' in vals:
            self.product_product_id.price_extra = vals["price_extra"]
        return super().write(vals)

    def unlink(self):
        for rec in self:
            if rec.product_product_id:
                rec.product_product_id.unlink()
        super().unlink()