import frappe 
def get_context(context):
    context.message = "Hello Customer!"
    context.show_sidebar = True