'''
Server-side script to update the sales and purchase list price 
of an item based on the purchase price and, in the case of
sales price, the margin uplift. At the same time, we take care
to insert new price_list items if they don't currently exist.
'''
import frappe
from frappe import _
from datetime import date
from kanban_mods.utils.misc_functions import dump

@frappe.whitelist() 
def update_prices(doctype, item_code, new_price): 
    try:
        if item_code == "Shipping":
            # shipping is always variable for every order so we dont want 
            # to update the cost because we don't want it to pop up on
            # future quotations. 
            #
            return "Success"
        else:
            item = frappe.get_doc("Item", item_code) # the actual item itself
            new_price = float(new_price)
            update_buying_price(doctype, item_code, new_price, item) 
            update_selling_price(doctype, item_code, new_price, item)
            return "Success"
    except Exception as ex:
        return ex
        

##### The  next two functions are the primary actions #######

def update_buying_price(doctype, item_code, price, item):

    buying_record = frappe.get_all(doctype, filters={'item_code': item_code, 'buying': True}) 
    if buying_record:
        frappe.db.set_value(doctype, buying_record[0].name, 'price_list_rate', price) 
    else: 
        create_item_price(doctype, item_code, 'Buying', price, item) 
    

def update_selling_price(doctype, item_code, price, item): 

    selling_price = get_selling_price(price, item)     
    selling_record = frappe.get_all(doctype, filters={'item_code': item_code, 'selling': True}) 
    if selling_record: 
        frappe.db.set_value(doctype, selling_record[0].name, 'price_list_rate', selling_price) 
    else: 
        create_item_price(doctype, item_code, 'Selling', selling_price, item) 
            
##### And here are the secondary, supportingfunctions #######

def create_item_price(doctype, item_code, price_list, price, item):
    # Populate and save a new item_price record. The type of 
    # record is determined by the price list in use
    selling = (price_list == "Selling")  
    buying  = not selling

    new_item_price = frappe.get_doc({'doctype':       doctype, 
                                    'item_code':      item_code,
                                    'item_name':      item.item_name, 
                                    'uom':            item.stock_uom,
                                    'brand':          item.brand,
                                    'currency':       'EUR',
                                    'selling':         selling,
                                    'buying':          buying,
                                    'price_list':      price_list, 
                                    'price_list_rate': price,
                                    'valid_from': date.today()
                                    }).insert()
    

def get_selling_price(price, item):
    # go fetch the correct rule ... you need the Buying rule data
    rule = frappe.get_doc("Pricing Rule", "Buying", {"item_group": item.item_group})

    margin = rule.margin_rate_or_amount
    margin_type = rule.margin_type
    # uplift the buying price to the sales "list price" and apply it
    # We always work with fixed percentages, but I added the redundant
    # case in case we ever meed it
    if margin_type == "Percentage":
        new_s_p = price * (1 + margin/100)
    else:
        new_s_p= price + margin
    print("New Selling Price = ",new_s_p)
    return new_s_p