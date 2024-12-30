frappe.ready(function() {
	// bind events here
	frappe.web_form.after_load = function() {
		let me = frappe.web_form;
		console.log(me);
		// check if the web form is what you are looking for
		if (me.doc.doc_type !== "ClientRFQ") return;
		// check if child table fieldname exists in the doctype or not
		// if (!me.has_field('billing_address')) return;
		// let field = me.get_field('billing_address');
		// check if field is table
 		// let row = field.grid.add_new_row(null, null, true, null, true),
		// grid_rows = field.grid.grid_rows,
		// row_name = grid_rows[grid_rows.length - 1].doc.name;
		// frappe.model.set_value(field.grid.doctype, row_name, "produces_name", "Milk");
	}
})

