import frappe

def get_context(context):
    context.clientrfq_settings = frappe.get_doc('ClientRFQ', frappe.form_dict.name)
    return context