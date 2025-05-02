/** @odoo-module */

import {patch} from "@web/core/utils/patch";
import {OrderSummary} from "@point_of_sale/app/screens/product_screen/order_summary/order_summary";
import {makeAwaitable} from "@point_of_sale/app/store/make_awaitable_dialog";
import {WarningDialog} from "@web/core/errors/error_dialogs";
import { _t } from "@web/core/l10n/translation";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { NumberPopup } from "@point_of_sale/app/utils/input_popups/number_popup";
import { parseFloat } from "@web/views/fields/parsers";

patch(OrderSummary.prototype, {
    async updateSelectedOrderline({ buffer, key }) {
        const order = this.pos.get_order();
        const selectedLine = order.get_selected_orderline();
        // Handling negation of value on first input
        if (buffer === "-0" && key == "-") {
            if (this.pos.numpadMode === "quantity" && !selectedLine.refunded_orderline_id) {
                buffer = selectedLine.get_quantity() * -1;
            } else if (this.pos.numpadMode === "discount") {
                buffer = selectedLine.get_discount() * -1;
            } else if (this.pos.numpadMode === "price") {
                buffer = selectedLine.get_unit_price() * -1;
            }
            this.numberBuffer.state.buffer = buffer.toString();
        }
        // This validation must not be affected by `disallowLineQuantityChange`
        if (selectedLine && selectedLine.isTipLine() && this.pos.numpadMode !== "price") {
            /**
             * You can actually type numbers from your keyboard, while a popup is shown, causing
             * the number buffer storage to be filled up with the data typed. So we force the
             * clean-up of that buffer whenever we detect this illegal action.
             */
            this.numberBuffer.reset();
            if (key === "Backspace") {
                this._setValue("remove");
            } else {
                this.dialog.add(AlertDialog, {
                    title: _t("Cannot modify a tip"),
                    body: _t("Customer tips, cannot be modified directly"),
                });
            }
            return;
        }
        if (
            selectedLine &&
            this.pos.numpadMode === "quantity" &&
            this.pos.disallowLineQuantityChange()
        ) {
            const orderlines = order.lines;
            const lastId = orderlines.length !== 0 && orderlines.at(orderlines.length - 1).uuid;
            const currentQuantity = this.pos.get_order().get_selected_orderline().get_quantity();

            if (selectedLine.noDecrease) {
                this.dialog.add(AlertDialog, {
                    title: _t("Invalid action"),
                    body: _t("You are not allowed to change this quantity"),
                });
                return;
            }
            const parsedInput = (buffer && parseFloat(buffer)) || 0;
            if (lastId != selectedLine.uuid) {
                this._showDecreaseQuantityPopup();
            } else if (currentQuantity < parsedInput) {
                this._setValue(buffer);
            } else if (parsedInput < currentQuantity) {
                this._showDecreaseQuantityPopup();
            }
            return;
        } else if (
            selectedLine &&
            this.pos.numpadMode === "discount" &&
            this.pos.restrictLineDiscountChange()
        ) {
            this.numberBuffer.reset();
            const inputNumber = await makeAwaitable(this.dialog, NumberPopup, {
                startingValue: selectedLine.get_discount() || 10,
                title: _t("Set the new discount"),
            });
            if (inputNumber) {
                await this.pos.setDiscountFromUI(selectedLine, inputNumber);
            }
            return;
        } else if (
            selectedLine &&
            this.pos.numpadMode === "price" &&
            this.pos.restrictLinePriceChange()
        ) {
            this.numberBuffer.reset();
            const inputNumber = await makeAwaitable(this.dialog, NumberPopup, {
                startingValue: selectedLine.get_unit_price(),
                title: _t("Set the new price"),
            });
            if (inputNumber) {
                await this.setLinePrice(selectedLine, inputNumber);
            }
            return;
        }
        const val = buffer === null ? "remove" : buffer;
        //check qty for numpad
        if (
            selectedLine &&
            (this.pos.numpadMode === "quantity" && val !== "" && val !== "remove") &&
            !(await this.pos.isQtyAvailable(selectedLine.get_product().id, selectedLine.getLocationId(), parseFloat(val)))
        ) {
            this.numberBuffer.reset();
            this.dialog.add(WarningDialog, {
                title: "Not enough quantity", message: "Product quantity not enough in this warehouse"
            })
            return;
        }
        this._setValue(val);
        if (val == "remove") {
            this.numberBuffer.reset();
            this.pos.numpadMode = "quantity";
        }
    }
})