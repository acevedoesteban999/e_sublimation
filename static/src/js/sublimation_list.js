/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListController } from "@web/views/list/list_controller";
import { useService } from "@web/core/utils/hooks";

export class SublimationListController extends ListController {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.action = useService("action");
    }

    openRecord(record){
        return this.action.doAction(this.orm.call(
            "product.template",
            "action_open_product_product_sublimation_kanban",
            [record.resId],
        ));
    }
}

registry.category("views").add("sublimation_list", {
    ...listView,
    Controller: SublimationListController,
});