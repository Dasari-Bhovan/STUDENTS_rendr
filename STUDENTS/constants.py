import os

commands = ['/start','/register','/results','/studentsummary','/departmentsummary', '/help']

test_emails = ['20bq1a4213@vvit.net','20bq1a4216@vvit.net','20bq1a4222@vvit.net','20bq1a4264@vvit.net']

# Messages or Replies
start_msg = '''
Enter Roll number to view all semester results. Like this, For example 20BQ1A4762
Enter Roll number with semester to view particular semester results. Like this, For example 20BQ1A4762 2-2
'''

help_msg = '''
/start - Start the conversation
/register - To Authorize your Mail-Id
/results - To view Student Results
/studentsummary - To analyse Student Results
/departmentsummary - To analyse Department wise results Statistics
'''

report = '\n⚠️Something wrong? Please let us know'

wrong_msg = '''Please check your Roll Number❗️'''

auth_msg = '''🔺️You're not registered yet🔺️ \nTo register Use  /register'''

departments = {
    '01':'CIV',
    '02':'EEE',
    '03':'MEC',
    '04':'ECE',
    '05':'CSE',
    '12':'INF',
    '42':'CSM',
    '47':'CIC',
    '49':'CSO',
    '54':'AID',
    '61':'AIM'
}
dept_names = list(departments.keys())

dept_codes = list(departments.values())

dept_names_msg = '''Departments:\n{'CIV','EEE','MEC','ECE','CSE','IT','CSM','CIC','CSO','AID','AIM'}'''

dept_msg = '''Enter **BATCH<space>DEPARTMENT<space>SEM** to get semester and that semester's each subject analysis\ni.e *19 civ 2-1*\n
Enter **batch<space>department** to get department's Semester Analysis\ni.e *19 civ*'''

otp_dict = {}

years = [y[1:3] for y in os.listdir("Results_json")]

semesters = ['1-1','1-2','2-1','2-2','3-1','3-2','4-1','4-2']

messages = ['hi', 'hello', 'hey']