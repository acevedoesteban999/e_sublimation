from odoo import fields,models,api

class ProductProduct(models.Model):
    _inherit = 'product.template'

    sublimation_ok = fields.Boolean(string='Sublimación')
    sublimation_ids = fields.One2many('sublimation.sublimation','product_tmpl_id','Sublimaciones')
    product_sublimation_count = fields.Integer(
        string='Sublimaciones (Total)',
        compute='_compute_total_attribute_line',
    )

    sublimation_id = fields.Many2one('sublimation.sublimation')
    product_tmpl_sublimation_id = fields.Many2one('product.template', 'Product Template Sublimation',compute="_compute_product_tmpl_sublimation_id")
    price_extra = fields.Monetary(related='sublimation_id.price_extra')
    
    def _compute_product_tmpl_sublimation_id(self):
        for rec in self:
            rec.product_tmpl_sublimation_id = rec.sublimation_id.product_tmpl_id
    



    @api.depends('product_sublimation_count')
    def _compute_total_attribute_line(self):
        self._create_variant_ids()
        for rec in self:
            rec.product_sublimation_count = len(rec.sublimation_ids)
    
    def action_open_product_product_sublimation(self):
        return {
            'name': f'{self.name} - Subl.',
            'type': 'ir.actions.act_window',
            'res_model': 'product.product',
            'view_mode': 'list,form',
            'target': 'current',
            'domain': [('id','in',self.env['product.product'].search([('sublimation_id','in',self.sublimation_ids.ids)]).ids)],
            'views': [
                (self.env.ref('e_sublimation.product_product_view_list_sublimation').id,'list'),
                (self.env.ref('product.product_normal_form_view').id,'form'),
            ],
        }
    
    def action_open_product_template(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'product.template',
            'view_mode': 'form',
            'target': 'current',
            'res_id': self.id,
            'view_id': self.env.ref('product.product_template_only_form_view').id,
        }

    def action_open_product_product_sublimation_kanban(self):
        return {
            'name': f'{self.name} - Subl.',
            'type': 'ir.actions.act_window',
            'res_model': 'product.product',
            'view_mode': 'kanban,list,form',
            'target': 'current',
            'domain': [('id','in',self.env['product.product'].search([('sublimation_id','in',self.sublimation_ids.ids)]).ids)],
            'views': [
                (self.env.ref('e_sublimation.product_product_view_kanban_sublimation').id,'kanban'),
                (self.env.ref('e_sublimation.product_product_view_list_sublimation').id,'list'),
                (self.env.ref('product.product_normal_form_view').id,'form'),
            ],
        }

    def unlink(self):
        self.sublimation_ids.unlink()
        return super().unlink()

