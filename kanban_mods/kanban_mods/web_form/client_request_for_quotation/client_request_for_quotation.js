frappe.ready(
	function() {		
		const form = frappe.web_form;
		
		// Function to update UOM when item_code is filled 
		function update_uom(row) { 
			frappe.call(
				{ 
				method: 'kanban_mods.kanban_mods.web_form.client_request_for_quotation.client_request_for_quotation.get_uom', args: {item_code: row.item_code}, 
					callback: function(retval) {
						r = retval.message;
						row.uom = r;
						form.refresh();
					}
				}
			)
		}
		// Attach event listener to item_code field in the child table 
		form.fields_dict.items.grid.wrapper.on('change focusout', 'input[data-fieldname="item_code"]',
			function(e) { 
				const target = $(e.target); 
				if (target.attr('data-fieldname') === 'item_code') { 
					const row = target.closest('.grid-row').data('doc'); 
					if (row.item_code) { 
						update_uom(row); 
					} 
				}
			}
		);

		frappe.call(
			{ 
			method: 'kanban_mods.kanban_mods.web_form.client_request_for_quotation.client_request_for_quotation.set_default_values', args: {}, 
				callback: function(retval) {
					r = retval.message;
					if (r.permitted) {
						Object.entries(r).forEach(([key,value]) => {
							if (!(key in ["permitted", "user"])) {
								form.set_value(key, value);
							}
						})
					} else {
						frappe.msgprint("User " + r.contact +" does not have sufficient permissions to create an RFQ","Unauthorised Access" );
						delay(10).then(() => {location.href = "/me";});
					}
				}
			}
		)
	
		form.on("schedule_date", function(){
			tDate = form.get_value("transaction_date");
			sDate = form.get_value("schedule_date")
			if (sDate && (isAtLeast14DaysLater(sDate, tDate ))) {
					frappe.msgprint("Sorry, but your 'required by' date must be at least 14 days in the future");
				delay(1).then(() => { form.set_value("schedule_date", null)});
			}
		});
	}
)

function isAtLeast14DaysLater(sched, trans) {
	console.log("we got here");
	baseDate = new Date(sched);
    twoWeeksLater = new Date(trans);
    twoWeeksLater.setDate( twoWeeksLater.getDate() + 13);
    return twoWeeksLater >= baseDate;
}

function delay(seconds) {
	return new Promise(resolve => setTimeout(resolve, seconds * 1000));
}
		
function update_uom(row) {
	if (row.item_code) { 
		// Set the UOM value (you can customize this logic)
		row.uom = 'Unit'; 
		form.refresh_field('items'); 
	} 
}
