import frappe

def execute(filters=None):

    user_id = frappe.session.user
    user_doc = frappe.get_doc("User", user_id)
    legal_team_value = user_doc.legal_team if hasattr(user_doc, "legal_team") else None  

    if filters and legal_team_value:
        filters["legal_team"] = legal_team_value

    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data

def get_columns(filters):
    column_order = [
        "case_number", "case_status", "filing_date", "lawyer", "case_type",
        "opposite_party", "case_stage", "court_name", "meril_role", "meril_entity",
        "amount", "case_description", "city_name",
        "opposing_clients_name", "opposing_clients_email", "opposing_clients_mobile_number",
        "opposing_clients_location", "opposing_clients_nature", "opposing_clients_address",
        "case_witness_name", "case_witness_email", "case_witness_mobile_number",
        "case_witness_location", "case_witness_nature", "case_witness_address"
    ]
    columns = []

    for field in column_order:
        columns.append({
            "label": field.replace("_", " ").title(),
            "fieldname": field,
            "fieldtype": "Data",
            "width": 200
        })
    
    return columns

def get_data(filters):
    query = """
        SELECT
            cm.case_number,
            cm.case_status,
            cm.filing_date, 
            lm.name AS lawyer,
            cm.case_type,
            cm.opposite_party,
            cm.case_stage,
            cm.court_name,
            cm.meril_role,
            cm.meril_entity,
            cm.amount,
            cm.case_description,
            cm.city_name,
            STRING_AGG(DISTINCT oc.name1, ',\n') AS opposing_clients_name,
            STRING_AGG(DISTINCT oc.email, ',\n') AS opposing_clients_email,
            STRING_AGG(DISTINCT oc.mobile_number, ',\n') AS opposing_clients_mobile_number,
            STRING_AGG(DISTINCT oc.location, ',\n') AS opposing_clients_location,
            STRING_AGG(DISTINCT oc.nature, ',\n') AS opposing_clients_nature,
            STRING_AGG(DISTINCT oc.address, ',\n') AS opposing_clients_address,
            STRING_AGG(DISTINCT cw.name2, ',\n') AS case_witness_name,
            STRING_AGG(DISTINCT cw.email, ',\n') AS case_witness_email,
            STRING_AGG(DISTINCT cw.mobile_number, ',\n') AS case_witness_mobile_number,
            STRING_AGG(DISTINCT cw.location, ',\n') AS case_witness_location,
            STRING_AGG(DISTINCT cw.department, ',\n') AS case_witness_nature,
            STRING_AGG(DISTINCT cw.address, ',\n') AS case_witness_address
        FROM
            `tabCase Master` cm
        LEFT JOIN
            `tabLawyer Master` lm ON cm.lawyer_name = lm.name
        LEFT JOIN
            `tabOpposing Clients` oc ON oc.parent = cm.name
        LEFT JOIN
            `tabCase Witness` cw ON cw.parent = cm.name
        WHERE
            1 = 1
    """
    conditions = []
    if filters.get("case_number"):
        conditions.append("cm.case_number = %(case_number)s")
    if filters.get("case_status"):
        conditions.append("cm.case_status = %(case_status)s")
    if filters.get("lawyer_name"):
        conditions.append("cm.lawyer_name = %(lawyer_name)s")
    if filters.get("filing_year"):
        conditions.append("EXTRACT(YEAR FROM cm.filing_date) = %(filing_year)s")
    if filters.get("opposite_party"):
        conditions.append("cm.opposite_party LIKE %(opposite_party)s")
        filters["opposite_party"] = f"%{filters['opposite_party']}%"
    if filters.get("legal_team"):
        conditions.append("cm.legal_team = %(legal_team)s")
    
    if conditions:
        query += " AND " + " AND ".join(conditions)
    
    query += """
        GROUP BY
            cm.case_number, cm.case_status, cm.filing_date, lm.name,
            cm.case_type, cm.opposite_party, cm.case_stage, cm.court_name,
            cm.meril_role, cm.meril_entity, cm.amount, cm.case_description, cm.city_name
    """
    
    data = frappe.db.sql(query, filters, as_dict=True)
    return data
