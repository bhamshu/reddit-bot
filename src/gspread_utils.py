import gspread

def init_sheet(sheet_name):
    gc = gspread.service_account()
    sh = gc.open(sheet_name)
    return sh

def init_reviews_worksheet(sh, index):
    worksheet = sh.get_worksheet(index)
    worksheet.update('A1:F1', [['Title', 'URL', 'Author', 'Content', 'Reply', 'User Summary']])
    return worksheet

def init_keywords_worksheet(sh, index):
    worksheet = sh.get_worksheet(index)
    return worksheet

def append_to_sheet(worksheet, row_data):
    worksheet.append_row(row_data)


def fetch_column_from_sheet(sheet, column_title):
    """Fetch a column's values based on the column title (assumes first row contains titles)."""
    # Find the column number for the given title
    titles = sheet.row_values(1)
    col_index = titles.index(column_title) + 1  # Adding 1 because gspread columns are 1-indexed
    return sheet.col_values(col_index)[1:]  # Skip the title row

gsheet = init_sheet("Reddit-Bot")