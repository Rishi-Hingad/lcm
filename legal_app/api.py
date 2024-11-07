import frappe
from frappe.utils import nowdate

@frappe.whitelist()
def get_hearing_events(start, end):
    events = []
    hearing_details = frappe.get_all(
        'Hearing Details',
        fields=['name', 'hearing_date', 'case_title', 'legal_team'],
        filters={
            'hearing_date': ['between', [start, end]]
        }
    )
    for hearing in hearing_details:
        # Define colors based on `legal_team`
        color = '#FF5733' if hearing['legal_team'] == 'IP' else (
            '#33C3FF' if hearing['legal_team'] == 'Legal' else '#28A745')
        # Append event details to events list
        events.append({
            'name': hearing['name'],
            'start': hearing['hearing_date'],
            'title': hearing['case_title'],
            'doctype': 'Hearing Details',
            'color': color
        })
    return events
