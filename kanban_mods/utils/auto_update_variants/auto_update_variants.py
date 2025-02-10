import frappe
from frappe import _
from datetime import date
from kanban_mods.utils.misc_functions import dump
from erpnext.controllers.item_variant import get_variant

@frappe.whitelist() 
def update_variants():
    
    manufs = frappe.get_all("Manufacturer")
    filter = tuple(item.name for item in manufs)
    items = frappe.get_all("Item")

    ix = 0
    ix2 = 0
    for item in items:
        if not item.name.endswith(filter) and not item.name == "Shipping":
            process_item(item, filter)
            exit()
            ix += 1
            print(ix2," -- ",ix)
        if ix == 100:
            ix = 0
            ix2 += 100
            frappe.db.commit()
            exit()
    return "Its all ready for checking"
    
# create the variants of the template item
def process_item(item, filter):
    # first retrieve the item 
    template = frappe.get_doc("Item", item.name)
    # and check whether it is already a template (has_variants = true) 
    # if necessary make sure the item is defined as a template and saved
    if not template.has_variants:
        template.has_variants = 1
        template.save()
    # Now use filter to make sure the variants are all present by 
    # creating any missing ones, and saving them ...but ...
    # DON'T create duplicates of the ones which already exist so:
    # first see if there are already variants in existence
    for manufr in filter:
        seekname = item.name + " - " + manufr
        found = frappe.db.get_value("Item", seekname, "name")
        if not found:
            new_variant = get_variant(template.name, None, None, manufr, None)
            new_variant.save(
                ignore_permissions=True, # ignore write permissions during insert
            )

def add_manufacturer_suffix(manufacturer = None):
    if manufacturer: 
        items = frappe.get_all("Item", filters = {'has_variants': True})
        ix = 0
        ix2 = 0
        for item in items:
            process_item(item, [manufacturer])
            ix += 1
            print(ix2," -- ",ix)
            if ix == 100:
                frappe.db.commit()
                ix = 0
                ix2 += 100
                
        return "Its all ready for checking" 
    else:
        return "You need to provide a manufacturer ID like SKF oe GENERIC"
