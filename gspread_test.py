import gspread

gc = gspread.service_account(filename='/home/CameronFord/mysite/learninggsheets-275116-85fd11269f0b.json')

sh = gc.create("Example spreadsheet")

worksheet = sh.get_worksheet(0)

worksheet.update('B1', 'Bingo!')
val = worksheet.acell('B1').value
print(val)
sh.share('cameron12.ford@gmail.com', perm_type='user', role='owner', notify=True)
