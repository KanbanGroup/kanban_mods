/********
This is just a place to hold some client Scripts which are actually
saved in the daabase .... I may need them her to copy and paste into
the production version once I am happy with them ...
********/

/////////////////////////////////////////////////////
//    Event Handler triggered by a submit event    //
/////////////////////////////////////////////////////
// It updates item default purchase prices based 
// on the data provided in the suppliers quotation.
// 
// When we scommit to the auotation, we update the
// buying and selling prices for the item.
//
// This does not affect the prices on existing 
// quotations ... only those which follow this 
// latest one. *I hope* ... :) :) :)
/////////////////////////////////////////////////////

frappe.ui.form.on('Supplier Quotation', "on_submit", function(cur_frm) {
    // for each item on table ...
if (cur_frm.doc.status == "Submitted") {
    $.each(cur_frm.doc.items || [], function(i, v) { 
        // let the user know you're doing something ...
        if (v.item_code != "Shipping"){
            frappe.show_alert({
                message:__("Updating the price for item "+ v.item_code + " to " + v.rate),
                indicator: 'green'
            }, 10);
            // then go off and do it ....
            frappe.call({
                // all the real work is done server-side by python
                method: "kanban_mods.utils.buy_sell_utils.auto_update_prices.update_prices",
                args: {
                    doctype: "Item Price",
                    item_code: v.item_code,
                    new_price: v.rate
                },
                callback: function(r) { 
                    if (r.message === "Success") { 
                        console.log("Price updated successfully for item " + v.item_code);
                    } else { 
                        console.error("Error updating price for item " + v.item_code + ": " + r.message);
                        console.print(r.message); 
                        frappe.msgprint({
                            title: __("System Error"),
                            indicator: "red",
                            message: __("Something went wrong updating the item prices.<br />"+
                                        "Please make a note of what you were doing and if possible<br />"+
                                        "open dev tools in your browser and check out the console dump<<br /><br />"+
                                        "Then call Kevin on +31 6 2158 4454 and tell him what is happening.")
                        })
                    } 
                }, 
                error: function(err) { 
                    console.error("Server error: ", err); 
                    frappe.show_alert({ message: __("Error updating price for item " + v.item_code), indicator: 'red' }, 10);
                }
            });
        }
    });
}
});




frappe.ui.form.on('Supplier Quotation', "on_submit", function(cur_frm) {
    // for each item on table ...
if (cur_frm.doc.status == "Submitted") {
    $.each(cur_frm.doc.items || [], function(i, v) { 
        // let the user know you're doing something ...
        if (v.item_code != "Shipping"){
            frappe.show_alert({
                message:__("Updating the price for item "+ v.item_code + " to " + v.rate),
                indicator: 'green'
            }, 10);
            // then go off and do it ....
            frappe.call({
                // all the real work is done server-side by python
                method: "kanban_mods.utils.buy_sell_utils.auto_update_prices.update_prices",
                args: {
                    doctype: "Item Price",
                    item_code: v.item_code,
                    new_price: v.rate
                },
                callback: function(r) {
                    console.log(r.message)
                }
            });
        }
    });
}
});
