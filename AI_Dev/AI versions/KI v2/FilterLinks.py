import xlrd
def get_links(sheet_index, loc, filtered_subtopic):
    
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(sheet_index) 
    sheet.cell_value(0, 0) 
    FilteredLinks = []
    OtherLinks = []
    for i in range(1, sheet.nrows): 
        if not sheet.cell_value(i, 0) == '':
            
            if sheet.cell_value(i, 3) == filtered_subtopic:
                FilteredLinks.append(sheet.cell_value(i, 0))
            else:
                OtherLinks.append(sheet.cell_value(i, 0))

    return FilteredLinks, OtherLinks

