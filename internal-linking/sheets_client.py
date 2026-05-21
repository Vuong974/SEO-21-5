import os
import gspread
from google.oauth2.service_account import Credentials

_SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def get_client() -> gspread.Client:
    creds_path = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "")
    if not creds_path:
        raise RuntimeError(
            "Set GOOGLE_SERVICE_ACCOUNT_JSON to the path of your service account key file.\n"
            "See internal-linking/README.md for setup instructions."
        )
    creds = Credentials.from_service_account_file(creds_path, scopes=_SCOPES)
    return gspread.authorize(creds)


def read_tab(sheet_id: str, tab_name: str) -> list:
    """Read a tab as list of dicts (first row = headers)."""
    ws = get_client().open_by_key(sheet_id).worksheet(tab_name)
    return ws.get_all_records()


def overwrite_tab(sheet_id: str, tab_name: str, headers: list, rows: list):
    """Overwrite an entire tab with new data (header + rows)."""
    ss = get_client().open_by_key(sheet_id)
    try:
        ws = ss.worksheet(tab_name)
        ws.clear()
    except gspread.WorksheetNotFound:
        ws = ss.add_worksheet(tab_name, rows=max(len(rows) + 20, 200), cols=len(headers))
    ws.append_row(headers)
    if rows:
        ws.append_rows(rows)


def upsert_internal_links(sheet_id: str, new_rows: list) -> int:
    """Append link opportunities that don't already exist (preserves Status edits)."""
    headers = [
        "Source URL", "Source Title", "Target URL", "Target Title",
        "Anchor Text", "Relevance Score", "Status",
    ]
    ss = get_client().open_by_key(sheet_id)
    try:
        ws = ss.worksheet("Internal Links")
        existing = ws.get_all_records()
    except gspread.WorksheetNotFound:
        ws = ss.add_worksheet("Internal Links", rows=1000, cols=len(headers))
        ws.append_row(headers)
        existing = []

    existing_keys = {(r.get("Source URL", ""), r.get("Target URL", "")) for r in existing}
    to_add = [
        [
            r["Source URL"], r["Source Title"], r["Target URL"], r["Target Title"],
            r["Anchor Text"], r["Relevance Score"], r["Status"],
        ]
        for r in new_rows
        if (r["Source URL"], r["Target URL"]) not in existing_keys
    ]
    if to_add:
        ws.append_rows(to_add)
    return len(to_add)


def update_statuses(sheet_id: str, tab_name: str, updates: dict):
    """Update Status column for specific (source_url, target_url) pairs."""
    ss = get_client().open_by_key(sheet_id)
    ws = ss.worksheet(tab_name)
    all_rows = ws.get_all_values()
    if not all_rows:
        return
    headers = all_rows[0]
    try:
        src_col = headers.index("Source URL")
        tgt_col = headers.index("Target URL")
        status_col = headers.index("Status")
    except ValueError:
        return
    for i, row in enumerate(all_rows[1:], start=2):
        key = (row[src_col] if len(row) > src_col else "", row[tgt_col] if len(row) > tgt_col else "")
        if key in updates:
            ws.update_cell(i, status_col + 1, updates[key])
