// Copyright (c) 2024, Virali Varnagar and contributors
// For license information, please see license.txt

frappe.query_reports["Case Detail Report"] = {
    "filters": [
        {
            "fieldname": "case_number",
            "label": __("Case Number"),
            "fieldtype": "Link",
            "options": "Case Master",
            "reqd": 0
        },
        {
            "fieldname": "case_status",
            "label": __("Case Status"),
            "fieldtype": "Select",
            "options": [
                { "label": "Open", "value": "Open" },
                { "label": "Closed", "value": "Closed" },
                { "label": "Re-Open", "value": "Re-Open" }
            ],
            "default": null,  // Set default value to null
            "reqd": 0
        },
        {
            "fieldname": "filing_year",
            "label": __("Year"),
            "fieldtype": "Int",
            "default": null,  // Set default value to null
            "reqd": 0
        }
    ]
};
