import frappe
from frappe.utils import cstr
from datetime import datetime

@frappe.whitelist()
def get_hearing_dates(start, end):
    hearing_dates = frappe.db.sql("""
        SELECT 
            hdt.name AS event_id,                  -- Unique identifier for the event
            hdt.hearing_date AS start_date,        -- Start and end date
            hdt.hearing_details_link AS title      -- Title to display
        FROM 
            `tabHearing Date` hdt
        WHERE 
            hdt.hearing_date BETWEEN %(start)s AND %(end)s
    """, {"start": start, "end": end}, as_dict=True)

    # Debug log to verify returned data
    frappe.log_error(hearing_dates, "Hearing Dates Retrieved")

    events = []
    for hearing in hearing_dates:
        events.append({
            "doctype": "Hearing Date",
            "name": hearing.get("event_id"),
            "title": hearing.get("title"),        # Title populated with hearing_details_link
            "start": hearing.get("start_date"),
            "end": hearing.get("start_date"),
        })

    return events
