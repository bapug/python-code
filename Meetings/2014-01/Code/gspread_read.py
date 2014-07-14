docData = {'Document' : name,'Sheets' : {} }
docSheets = docData['Sheets']

for sheet in wks.worksheets():
    all = sheet.get_all_values()

    filtered_data = [d for d in all[1:] if d[0] != '' and d[1] != '']
    docSheets[sheet.title] = {
        'rows' : sheet.row_count,'cols' : sheet.col_count,
        'headings' : all[0],'data' : fltdata }
