import telebot
import os
import json
import math
import random
import smtplib
from constants import *
from validate_email_address import validate_email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
load_dotenv()

bot = telebot.TeleBot(os.getenv('API_KEY_BHO'))

# START COMMAND
@bot.message_handler(commands=['start'])
def start(message):
    try:
        read_id = None
        with open("student_chat_ids.json", 'r') as fstart:
            x = json.load(fstart)
            read_id = x
    except:
        bot.send_message(message.chat.id, "You haven't registered yet.\nTo register, use   /register   command")
    else:
        if(str(message.chat.id) not in read_id):
            bot.send_message(message.chat.id, "You haven't registered yet.\nTo register, use   /register   command")
        else:
            bot.send_message(message.chat.id, "You've already registered.\nUse   /results   to view your results")

# REGISTRATION
@bot.message_handler(commands=['register'])
def register(message):
    # OPENING CHAT_ID FILE
    try:
        read_id = None
        with open("student_chat_ids.json", 'r') as freg:
            if read_id == None:
                y = json.load(freg)
                read_id = y
    except:
        msg = bot.send_message(message.chat.id, "Enter Your Email to get registered")
        bot.register_next_step_handler(msg, getid)
    else:
        if(str(message.chat.id) not in read_id):
            msg = bot.send_message(message.chat.id, "Enter Your Email to get registered")
            bot.register_next_step_handler(msg, getid)
        else:
            bot.send_message(message.chat.id, "You've already registered.\nUse   /results   to view results")

# OTP GENERATION
def otpmail(mailid, name):
    stud_mailid = (mailid.text).lower()
    valid_email = validate_email(stud_mailid,verify=True)
    if valid_email or valid_email==None:
        my_email = os.getenv("my_email")
        password = os.getenv("password")
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "OTP for VVIT Results Bot"
        msg['From'] = my_email
        otp = []
        def otpgen():
            digits="0123456789"
            OTP=""
            for i in range(6) :
                OTP+= digits[math.floor(random.random() * 10)]
            return OTP
        otp = otpgen()
        otp_dict.update({mailid.chat.id:[otp,stud_mailid]})
    else:
        bot.send_message(mailid.chat.id, "Enter valid email address")
        return False
    x="""
    <html>
    <body>
    <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
    <div style="margin:50px auto;width:70%;padding:20px 0">
        <div style="border-bottom:1px solid #eee">
        <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">VVIT RESULTS BOT</a>
        </div>
        <p style="font-size:1.1em">Hi """ + name + """,</p>
        <p> Use the following OTP to complete your Registration</p>
        <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">"""+otp+"""</h2>
        <p style="font-size:0.9em;">Regards,<br />VVIT MANAGEMENT<if(otpgen() not in OTP):
        OTP.append(otp)/p>
        <hr style="border:none;border-top:1px solid #eee" />
        <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
        <p>VVIT</p>
        </div>
    </div>
    </div>
    </body>
    </html>
    """
    parthtml=MIMEText(x,'html')
    msg.attach(parthtml)
    connection=smtplib.SMTP("smtp.gmail.com", port=587)
    connection.ehlo()
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(my_email,stud_mailid,msg.as_string())
    connection.quit()
    return True

# GET CHAT ID
def getid(message):
    # print(message.text)
    stud_mail  = (message.text).lower()
    if ((('bq1a' in stud_mail or 'bq5a' in stud_mail)) and ('@vvit.net' in stud_mail)) or (stud_mail in test_emails):
        name = 'VVITIAN'
        if(message.chat.first_name and message.chat.last_name):
            name = message.chat.first_name+ " " + message.chat.last_name
        # OTP GENERATION FUNCTION CALL
        if(otpmail(message, name)):
            bot.send_message(message.chat.id, "OTP Sent to your mail Successfully!")
            bot.send_message(message.chat.id, "Please enter the OTP")
            bot.register_next_step_handler(message, otpverification)
        else:
            bot.register_next_step_handler(message, getid)
    else:
        bot.send_message(message.chat.id, "Invalid Email-id")
        bot.send_message(message.chat.id, "Enter your Email-id again")
        bot.register_next_step_handler(message, getid)

# OTP VERIFICATION
def otpverification(message):
    # print(otp_dict[message.chat.id])
    if(message.text == otp_dict[message.chat.id][0]):
        id = {}
        id[message.chat.id] = {
                "USERNAME":message.chat.username,
                "FIRSTNAME":message.chat.first_name,
                "LASTNAME":message.chat.last_name,
                "MAIL":otp_dict.pop(message.chat.id)[1]
                }
        try:
            read_id = None
            with open("student_chat_ids.json", 'r') as fotpver:
                if read_id == None:
                    z = json.load(fotpver)
                    read_id = z
        except:
            with open("student_chat_ids.json", 'w') as fwotpver:
                json.dump(id,fwotpver, indent=5)
            bot.send_message(message.chat.id, "You've successfully registered")
            bot.send_message(message.chat.id, "Use /results command to view results")
        else:
            if(str(message.chat.id) not in read_id):
                # print(id)
                read_id.update(id)
                # print(read_id)
                with open("student_chat_ids.json", 'w') as fwotpver:
                    json.dump(read_id,fwotpver, indent=5)
                bot.send_message(message.chat.id, "You've successfully registered")
                bot.send_message(message.chat.id, "Use /results command to view results")
            else:
                bot.send_message(message.chat.id, "You've already registered")
                bot.send_message(message.chat.id, "Use /help command or Tap on the MENU to view available commands")
    else:
        bot.send_message(message.chat.id, "OTP Mismatched!")
        bot.send_message(message.chat.id, "Enter your mail-id again")
        bot.register_next_step_handler(message, getid)

# USER AUTHORIZATION FUNCTION
def auth_user(message):
    # print("auth",message.text)
    try:
        read_id = None
        with open("student_chat_ids.json", 'r') as fotpauth:
                z = json.load(fotpauth)
                read_id = z
    except:
        bot.send_message(message.chat.id, auth_msg)
        return False
    else:
        if(str(message.chat.id) not in read_id):
            bot.send_message(message.chat.id, auth_msg)
            return False
        else:
            return True

# /RESULTS COMMAND
@bot.message_handler(commands=['results'], func=auth_user)
def results(message):
    try:
        read_id = None
        with open("student_chat_ids.json", 'r') as fresult:
                z = json.load(fresult)
                read_id = z
    except:
        bot.send_message(message.chat.id, auth_msg)
    else:
        if(str(message.chat.id) not in read_id):
            bot.send_message(message.chat.id, auth_msg)
        else:
            bot.send_message(message.chat.id, start_msg)
            bot.send_message(message.chat.id, "Enter Roll number:")
            bot.register_next_step_handler(message,validate_roll_num)

# ROLL NUMBER VALIDATION
def validate_roll_num(message):
    # print("validate roll",message.text)
    if(message.text not in commands):
        if(auth_user(message)):
            msg = message.text.split()
            if(msg[0][4:6].lower() == '5a'):
                year = str(int(msg[0][0:2]) - 1)
            else:
                year = msg[0][0:2]
            if(msg[0].lower() in messages):
                user = message.from_user.username
                if(user != None):
                    bot.send_message(message.chat.id, f"{msg[0].upper()} {user.upper()}, Please Enter Roll Number to check Results!")
                    return False
                else:
                    bot.send_message(message.chat.id, start_msg)
                    return False
            elif msg[0].lower() in commands:
                return False
            elif(len(msg[0]) == 10 and (msg[0][2:4].lower() == 'bq') and (year in years)):
                bot.register_next_step_handler(message,msg_result)
                return True
            # print("Wrong Roll Number")
            bot.reply_to(message, wrong_msg)
            return False
        else:
            return False
    return False

# RESULTS MESSAGE GENERATION COMMAND
@bot.message_handler(func=validate_roll_num)
def msg_result(message):
    # print(message.text)
    try:
        msg_list = message.text.split()
        msg_list[0] = msg_list[0].upper()
        dept_code = departments[msg_list[0][6:8]]
        if(msg_list[0][4:6].lower() == '5a'):
            year = str(int(msg_list[0][0:2]) - 1)
        else:
            year = msg_list[0][0:2]
        if(len(msg_list) == 2 and (dept_code in dept_codes)):
            try:
                with open(f'Results_json/R{year}/{dept_code}.json','r') as fres:
                    res_json = json.load(fres)
            except:
                bot.reply_to(message, wrong_msg)
            reply = ""
            if(msg_list[1] in semesters):
                if(res_json.get(msg_list[0]) != None):
                    if(res_json[msg_list[0]].get(msg_list[1]) != {}):
                        reply += f"Name : {res_json[msg_list[0]]['name']}\nRoll Number : {msg_list[0]}\n\n"
                        reply += f"➡️ {msg_list[1]} Semester End Exam Result ⬅️\n"
                        for subject in res_json[msg_list[0]][msg_list[1]]:
                            if(subject == 'username'):
                                continue
                            reply += f"{subject} : {res_json[msg_list[0]][msg_list[1]][subject]}\n"
                        bot.send_message(message.chat.id, reply + report)
                    else:
                        bot.reply_to(message, f"🔺️'{msg_list[1]}' Semester End exam results are not available🔺️\n" + report)
                else:
                    bot.reply_to(message, wrong_msg +"\n"+report)
            else:
                bot.reply_to(message, "🔺️Please check the semester entered🔺️\n" + report)
        elif(len(msg_list) == 1 and len(msg_list[0]) == 10 and (dept_code in dept_codes)):
            try:
                with open(f'Results_json/R{year}/{dept_code}.json','r') as fres:
                    res_json = json.load(fres)
            except:
                bot.reply_to(message, wrong_msg)
            else:
                reply = ""
                if(res_json.get(msg_list[0]) != None): # CHECKING RESULT OF ROLL NUMBER
                    for sem in res_json[msg_list[0]]:
                        if(res_json[msg_list[0]][sem]): # CHECKING RESULT OF A SEMESTER OF THAT ROLL NUMBER
                            if(sem == 'name'):
                                reply += f"Name : {res_json[msg_list[0]]['name']}\nRoll Number : {msg_list[0]}\n" # ADDING NAME, ROLL NUMBER TO MESSAGE
                            else:
                                # ADDING RESULTS
                                reply += f"➡️ {sem} Semester End Exam Result ⬅️\n\n"
                                for subject in res_json[msg_list[0]][sem]:
                                    if(subject == 'username'):
                                        continue
                                    reply += f"{subject} : {res_json[msg_list[0]][sem][subject]}\n"
                        else:
                            continue
                        reply += '\n'
                    bot.send_message(message.chat.id, reply + report)
                else:
                    bot.reply_to(message, " No results found \n" +report)
        else:
            bot.reply_to(message, wrong_msg + "\n" +report)
    except:
        bot.reply_to(message, " No results found \n" +report)

bot.polling()