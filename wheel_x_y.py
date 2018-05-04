import xlrd

a = xlrd.open_workbook(r'/Users/wlt/Desktop/total.xlsx')
sheet1 = a.sheet_by_index(0)
sheet1 = a.sheet_by_name('Sheet1')
x = sheet1.col_values(0)
y = sheet1.col_values(1)

l = zip(x, y)
