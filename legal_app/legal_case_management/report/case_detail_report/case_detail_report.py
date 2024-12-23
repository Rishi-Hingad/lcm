# Copyright (c) 2024, Virali Varnagar and contributors
# For license information, please see license.txt
import frappe

def execute(filters=None):
    columns = get_columns(filters)  # Pass filters to get columns dynamically
    data = get_data(filters)
    return columns, data

def get_columns(filters):
    # Fetch all fields from the Case Master table dynamically
    fields = frappe.get_all('Case Master', fields=["*"], limit=1)  # Just get 1 row to fetch all columns
    columns = []

    # Add columns dynamically from the Case Master schema
    if fields:
        # Define the desired column order
        column_order = [
            "case_number", "case_status", "filing_date", "lawyer", "case_type", 
            "opposing_party", "case_stage", "court_name", "meril_role"
        ]
        
        for field in column_order:  # Use the desired order of fields
            if field in fields[0]:
                column = {
                    "label": field.replace("_", " ").title(),
                    "fieldname": field,
                    "fieldtype": "Data",  # Default type is Data, can be customized per fieldtype
                    "width": 150
                }
                # Check if the field is a "Link" field and set options accordingly
                field_info = frappe.get_meta('Case Master').get_field(field)
                if field_info and field_info.fieldtype == 'Link':
                    column["fieldtype"] = "Link"
                    column["options"] = field_info.options  # Set the linked Doctype as options
                columns.append(column)
    
    return columns


def get_data(filters):
    # Base query to fetch all cases from the Case Master where legal_team == 'Legal'
    query = """
    SELECT
        cm.case_number, cm.case_status, cm.filing_date, 
        lm.name AS lawyer, cm.case_type, cm.opposite_party, cm.case_stage, cm.court_name, cm.meril_role
    FROM
        "tabCase Master" cm
    LEFT JOIN
        "tabLawyer Master" lm ON cm.lawyer_name = lm.name
    LEFT JOIN
        "tabCase Types Master" ct ON cm.case_type = ct.name
    LEFT JOIN
		"tabCase Stages Master" cs ON cm.case_stage = cs.name
    LEFT JOIN
		"tabMeril Role Master" mr ON cm.meril_role = mr.name
    WHERE
        cm.legal_team = 'Legal'
""" 
    # Apply filters if they are provided
    conditions = []
    if filters.get("case_number"):
        conditions.append("cm.case_number = %(case_number)s")
    if filters.get("case_status"):
        conditions.append("cm.case_status = %(case_status)s")
    if filters.get("filing_year"):
        conditions.append("EXTRACT(YEAR FROM cm.filing_date) = %(filing_year)s")
    
    # Append conditions to the base query if there are any
    if conditions:
        query += " AND " + " AND ".join(conditions)
    
    # Execute the query with the filters
    data = frappe.db.sql(query, filters, as_dict=True)
    return data
