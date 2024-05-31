import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime


def make_new_comment(name, email, comment):
    now = datetime.now()
    date = now.strftime("%m/%d/%Y")
    time = now.strftime("%H:%M:%S")

    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/CameronFord/mysite/learninggsheets-275116-85fd11269f0b.json', scope)
    gc = gspread.authorize(credentials)
    comment_spreadsheet = gc.open('Juggle Hacker comments')
    comment_worksheet=comment_spreadsheet.get_worksheet(0)
    comment_worksheet.append_row([date,time,name,email,comment])
    comment_spreadsheet.share('juggle.hacker@gmail.com', perm_type='user', role='writer',email_message='You have a new comment from {}!'.format(name))

if __name__ == "__main__":
    now = datetime.now()
    date = now.strftime("%m/%d/%Y")
    time = now.strftime("%H:%M:%S")
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/CameronFord/mysite/learninggsheets-275116-85fd11269f0b.json', scope)
    gc = gspread.authorize(credentials)
    comment_spreadsheet = gc.open('Juggle Hacker comments')
    comment_worksheet=comment_spreadsheet.get_worksheet(0)
    print(comment_worksheet.get_all_values())