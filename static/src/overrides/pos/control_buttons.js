/** @odoo-module */

import {patch} from "@web/core/utils/patch";
import {ControlButtons} from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import {makeAwaitable} from "@point_of_sale/app/store/make_awaitable_dialog";
import {SelectionPopup} from "@point_of_sale/app/utils/input_popups/selection_popup";
import {_t} from "@web/core/l10n/translation";

patch(ControlButtons.prototype, {
    async fetchWarehouses() {
        let warehouses = await this.env.services.orm.searchRead(
            "stock.picking.type",
            [["pos_operation", "=", true]],
            ["id", "name"],
        );
        warehouses.forEach(w => {
            w.label = w.name;
            w.item = w.id;
        })
        return warehouses;
    },

    async switch_warehouse(operation_type_id) {
        const result = await this.pos.data.call("pos.config", "switch_pos_picking_type", [
            [this.pos.config.id],
            operation_type_id
        ]);
        if(result) {
            this.pos.warehouse_name = result;
        }
    },

    async onClickWarehouse() {
        // const selectionList = this.getPricelistList();
        const warehouses = await this.fetchWarehouses()
        const payload = await makeAwaitable(this.dialog, SelectionPopup, {
            title: _t("Select the warehouse"),
            list: warehouses,
        });
        if (payload) {
            console.log("clicked", payload);
            await this.switch_warehouse(payload)
        }
    }
});
