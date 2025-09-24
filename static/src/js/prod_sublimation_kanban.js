/** @odoo-module **/

import { registry } from "@web/core/registry";
import { kanbanView } from "@web/views/kanban/kanban_view";
import { KanbanController } from "@web/views/kanban/kanban_controller";
import { useService } from "@web/core/utils/hooks";

export class ProdSublimationKanbanController extends KanbanController {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.action = useService("action");
    }

    async  createRecord({ group } = {}) {
        const action = await this.orm.call(
            "product.template",
            "action_open_sublimation_wizard",
            [this.props.context.default_product_tmpl_sublimation_id],
        );
    
        await this.action.doAction(action, {
            onClose: (infos) => {
                if (infos?.new_product_id) {
                    const dom = [...this.model.config.domain];
                    const idx = dom.findIndex(t => t[0] === 'id' && t[1] === 'in');
                    if (idx >= 0) {
                        const ids = new Set(dom[idx][2]);
                        ids.add(infos.new_product_id);
                        dom[idx] = ['id', 'in', [...ids]];
                    } else {
                        dom.push(['id', 'in', [infos.new_product_id]]);
                    }
                    this.model.config.domain = dom;
                    this.model.load().then(() => this.render(true));
                }
            },
        });              
    }

}

registry.category("views").add("prod_sublimation_kanban", {
    ...kanbanView,
    Controller: ProdSublimationKanbanController,
});

