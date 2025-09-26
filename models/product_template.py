from odoo import fields,models,api

class ProductProduct(models.Model):
    _inherit = 'product.template'

    sublimation_ok = fields.Boolean(string='Sublimation')
    product_sublimation_count = fields.Integer(
        string='Sublimations (Total)',
        compute='_compute_total_attribute_line',
    )

    product_tmpl_sublimation_id = fields.Many2one('product.template', 'Product Template Sublimation')
    product_prod_sublimation_ids = fields.One2many('product.product', 'product_tmpl_sublimation_id', string='Product Products Sublimation', readonly=True)
    


    @api.depends('product_sublimation_count')
    def _compute_total_attribute_line(self):
        self._create_variant_ids()
        for rec in self:
            rec.product_sublimation_count = len(rec.product_prod_sublimation_ids)
    
    def action_open_product_product_sublimation(self):
        return {
            'name': f'{self.name} - Subl.',
            'type': 'ir.actions.act_window',
            'res_model': 'product.product',
            'view_mode': 'list,form',
            'target': 'current',
            'domain': [('id','in',self.product_prod_sublimation_ids.ids)],
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
            'view_mode': 'kanban,list',
            'target': 'current',
            'domain': [('id','in',self.product_prod_sublimation_ids.ids)],
            'context': {'default_product_tmpl_sublimation_id': self.id},
            'views': [
                (self.env.ref('e_sublimation.product_product_view_kanban_sublimation').id,'kanban'),
                (self.env.ref('e_sublimation.product_product_view_list_sublimation').id,'list'),
                (self.env.ref('product.product_normal_form_view').id,'form'),  
            ],
        }

    @api.model
    def action_open_sublimation_wizard(self,id_model = False):
        model = self or self.env['product.template'].browse(id_model)
        return {
            'name': 'Create Sublimación',
            'type': 'ir.actions.act_window',
            'res_model': 'sublimation.wizard',
            'view_mode': 'form',
            'target': 'new',
            'views': [(self.env.ref('e_sublimation.sublimation_wizard_view_form').id,'form')],
            'context': {'default_product_tmpl_sublimation_id': model.id}
        }

    def unlink(self):
        if self.product_prod_sublimation_ids:
            self.product_prod_sublimation_ids.unlink()
        return super().unlink()

