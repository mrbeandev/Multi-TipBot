import datetime
import requests
import string
import telebot
import mysql.connector
from mysql.connector import Error
import requests
from bs4 import BeautifulSoup
import json
import os
import time
from random import *
from telebot import types
from flask import Flask, request
from decimal import *
from config import *

#=================================================================      dont change anything from here          ==================================================================##
bot = telebot.TeleBot(token=token) 
server = Flask(__name__)
Wapi_url = "https://mrcyjanek.net/wapi/api.php"

def get_recent_txid(currency, address):
    pp = requests.get("https://sochain.com/api/v2/get_tx_received/" + str(currency) + "/"+ str(address))
    pps = json.loads(pp.text)
    dat = pps['data']
    coun = len(dat['txs'])
    print(coun)
    coo = coun - 1
    txx = dat['txs']
    if txx == []:
        txid = "no transactions!!"
    else:
        txid = txx[int(coo)]['txid']
    return txid

def get_txid_confirm(currency, address):
    pp = requests.get("https://sochain.com/api/v2/get_tx_received/" + str(currency) + "/"+ str(address))
    pps = json.loads(pp.text)
    dat = pps['data']
    coun = len(dat['txs'])
    #print(coun)
    coo = coun - 1
    con = dat['txs']
    if con == []:
      conf = 1000
    else:
      conf = con[int(coo)]['confirmations']
    return conf

def get_recent_amount(currency, address):
    pp = requests.get("https://sochain.com/api/v2/get_tx_received/" + str(currency) + "/"+ str(address))
    pps = json.loads(pp.text)
    dat = pps['data']
    coun = len(dat['txs'])
    #print(coun)
    coo = coun - 1
    amu = dat['txs']
    if amu == []:
      amount = 0
    else:
      amount = amu[int(coo)]['value']
    return amount

def check_address(currency, address):
    cc = requests.get("https://sochain.com/api/v2/get_address_balance/" + str(currency) + "/"+ str(address))
    jsn = json.loads(cc.text)
    add = jsn["status"]
    return add

def generate_address(currency):
    cc = requests.post(str(Wapi_url), data= json.dumps({'apikey' : api_key, 'username' : str(wapi_username) , 'currency' : str(currency.upper()), 'action' : 'getnewaddress'}))
    jj = json.loads(cc.text)
    return jj['address']

def make_Withdraw(currency, amount, address):
    cc = requests.post(str(Wapi_url), data= json.dumps({'apikey' : api_key, 'username' : str(wapi_username), 'currency' : str(currency.upper()), 'action' : 'sendtoaddress', 'data':{ "address" :str(address) , "amount" : str(amount)}}))
    jj = json.loads(cc.text)
    return jj['txid']

def user_btc_add(userid):
    mydb = mysql.connector.connect(
      host=db_host,
      user=db_user,
      password=db_pass,
      database=db_database
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT btc_address FROM users WHERE userid = "+ str(userid) +"")
    myresult = mycursor.fetchall()
    btc = myresult[0][0]
    return btc

def user_ltc_add(userid):
    mydb = mysql.connector.connect(
      host=db_host,
      user=db_user,
      password=db_pass,
      database=db_database
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT ltc_address FROM users WHERE userid = "+ str(userid) +"")
    myresult = mycursor.fetchall()
    ltc = myresult[0][0]
    return ltc

def user_doge_add(userid):
    mydb = mysql.connector.connect(
      host=db_host,
      user=db_user,
      password=db_pass,
      database=db_database
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT doge_address FROM users WHERE userid = "+ str(userid) +"")
    myresult = mycursor.fetchall()
    doge = myresult[0][0]
    return doge

def user_btc_bal(userid):
    mydb = mysql.connector.connect(
      host=db_host,
      user=db_user,
      password=db_pass,
      database=db_database
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT btc_balance FROM users WHERE userid = "+ str(userid) +"")
    myresult = mycursor.fetchall()
    btc = myresult[0][0]
    return btc

def user_doge_bal(userid):
    mydb = mysql.connector.connect(
      host=db_host,
      user=db_user,
      password=db_pass,
      database=db_database
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT doge_balance FROM users WHERE userid = "+ str(userid) +"")
    myresult = mycursor.fetchall()
    doge = myresult[0][0]
    return doge

def user_ltc_bal(userid):
    mydb = mysql.connector.connect(
      host=db_host,
      user=db_user,
      password=db_pass,
      database=db_database
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT ltc_balance FROM users WHERE userid = "+ str(userid) +"")
    myresult = mycursor.fetchall()
    ltc = myresult[0][0]
    return ltc

def user_check(userid):
    mydb = mysql.connector.connect(
                    host=db_host,
                    user=db_user,
                    password=db_pass,
                    database=db_database
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM users WHERE userid = "+ str(userid) +"")
    mycursor.fetchall()
    row = mycursor.rowcount
    print(row)
    return row

def user_add_bal(userid, amount, currency):
    mydb = mysql.connector.connect(
      host=db_host,
      user=db_user,
      password=db_pass,
      database=db_database
    )
    if currency == "DOGE" or currency == "doge":
        cur = "doge_balance"
    elif currency == "BTC" or currency == "btc":
        cur = "btc_balance"
    elif currency == "LTC" or currency == "ltc":
        cur = "ltc_balance"

    mycursor = mydb.cursor()
    mycursor.execute("UPDATE users SET "+ str(cur) +" = " + str(cur) + " + %s WHERE userid = %s", (str(amount), str(userid)))
    mydb.commit()
    return

def user_remove_bal(userid, amount, currency):
    mydb = mysql.connector.connect(
      host=db_host,
      user=db_user,
      password=db_pass,
      database=db_database
    )
    if currency == "DOGE" or currency == "doge":
        cur = "doge_balance"
    elif currency == "BTC" or currency == "btc":
        cur = "btc_balance"
    elif currency == "LTC" or currency == "ltc":
        cur = "ltc_balance"

    mycursor = mydb.cursor()
    mycursor.execute("UPDATE users SET "+ str(cur) +" = " + str(cur) + " - %s WHERE userid = %s", (str(amount), str(userid)))
    mydb.commit()
    return

def get_active():
    mydb = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pass,
        database=db_database
    )
    mycursor = mydb.cursor()
    ti = time.time() - float(active_users_store_time)
    mycursor.execute("SELECT userid FROM users WHERE last_message >= " + str(ti) + "")
    myres = mycursor.fetchall()
    count = mycursor.rowcount
    return count

def new_user_register(userid):
    btc = generate_address('btc')
    doge = generate_address('doge')
    ltc = generate_address('ltc')
    mydb = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=db_pass,
                database=db_database
    )
    mycursor = mydb.cursor()
    sql = "INSERT INTO users (userid, btc_address, ltc_address, doge_address) VALUES (%s, %s, %s, %s)"
    val = (str(userid), str(btc), str(ltc), str(doge))
    mycursor.execute(sql, val)
    mydb.commit()
    return 


def menu():
    markup = types.ReplyKeyboardMarkup(row_width=3,resize_keyboard=True)
    btn1 = types.KeyboardButton(button1)
    btn2 = types.KeyboardButton(button2)
    btn3 = types.KeyboardButton(button3)
    btn4 = types.KeyboardButton(button4)
    markup.add(btn1)
    markup.add(btn2, btn3)
    markup.add(btn4)
    return markup

def withdraw_menu():
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    btn1 = types.KeyboardButton("BTC")
    btn2 = types.KeyboardButton("DOGE")
    btn3 = types.KeyboardButton("LTC")
    btn4 = types.KeyboardButton("🚫 Cancel")
    markup.add(btn1, btn2, btn3)
    markup.add(btn4)
    return markup

def cancel_menu():
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    btn4 = types.KeyboardButton("🚫 Cancel")
    markup.add(btn4)
    return markup
#=================================================================             defs             ==================================================================##


# balance ================================================================================#
def bal(message):
    try:
        bot.send_message(message.chat.id, "💰 <b>Your Wallet Balance :</b>\n💳 <b>BTC :</b> <code>"+ str("{0:.7f}".format(user_btc_bal(message.chat.id))) + " BTC</code>\n💶 <b>LTC :</b> <code>"+ str("{0:.7f}".format(user_ltc_bal(message.chat.id))) +" LTC</code>\n💷 <b>DOGE :</b> <code>" + str("{0:.7f}".format(user_doge_bal(message.chat.id))) +" DOGE </code>", parse_mode="html", reply_markup=menu())
        lll = [20,40,28,24,35,13,24,16,30]
        x_time = choice(lll)
        time.sleep(x_time)
        check_txid(message)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Error : "+ str(e))
# balance ================================================================================#


# Check ================================================================================#
def check_txid(message):
    try:
        mydb = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pass,
        database=db_database
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT btc_txid,ltc_txid,doge_txid FROM users WHERE userid = "+ str(message.chat.id) +"")
        bbbb = mycursor.fetchall()
        #================#
        old_btc = bbbb[0][0]
        old_ltc = bbbb[0][1]
        old_doge = bbbb[0][2]
        #================================================================================#
        new_btc = get_recent_txid('btc', str(user_btc_add(message.chat.id)))
        btc_conf = get_txid_confirm('btc', str(user_btc_add(message.chat.id)))
        btc_amount = get_recent_amount('btc', str(user_btc_add(message.chat.id)))
        #================================================================================#
        new_ltc = get_recent_txid('ltc', str(user_ltc_add(message.chat.id)))
        ltc_conf = get_txid_confirm('ltc', str(user_ltc_add(message.chat.id)))
        ltc_amount = get_recent_amount('ltc', str(user_ltc_add(message.chat.id)))
        #================================================================================#
        new_doge = get_recent_txid('doge', str(user_doge_add(message.chat.id)))
        doge_conf = get_txid_confirm('doge', str(user_doge_add(message.chat.id)))
        doge_amount = get_recent_amount('doge', str(user_doge_add(message.chat.id)))
        #================================================================================#
        if old_doge != new_doge or old_doge == "not_set":
            if doge_conf <= 10:
                mydb = mysql.connector.connect(
                        host=db_host,
                        user=db_user,
                        password=db_pass,
                        database=db_database
                )
                mycursor = mydb.cursor()
                mycursor.execute("UPDATE users SET doge_txid = %s, doge_balance = doge_balance + %s WHERE userid = %s", (str(new_doge), str(doge_amount), str(message.chat.id),))
                mydb.commit()
                bot.send_message(message.chat.id, "🎉 <b>New Deposit of " + str("{0:.8f}".format(float(doge_amount))) + " DOGE Received</b>", parse_mode="html", reply_markup=menu())
            else:
                print("too many confirms DOGE")
                pass
        else:
            pass
        #================================================================================#
        if old_btc != new_btc or old_btc == "not_set":
            if btc_conf <= 10:
                mydb = mysql.connector.connect(
                        host=db_host,
                        user=db_user,
                        password=db_pass,
                        database=db_database
                )
                mycursor = mydb.cursor()
                mycursor.execute("UPDATE users SET btc_txid = %s, btc_balance = btc_balance + %s WHERE userid = %s", (str(new_btc), str(btc_amount), str(message.chat.id),))
                mydb.commit()
                bot.send_message(message.chat.id, "🎉 <b>New Deposit of " + str("{0:.8f}".format(float(doge_amount))) + " BTC Received</b>", parse_mode="html", reply_markup=menu())
            else:
                print("too many confirms BTC")
                pass
        else:
            pass
        #================================================================================#
        if old_ltc != new_ltc or old_ltc == "not_set":
            if ltc_conf <= 10:
                mydb = mysql.connector.connect(
                        host=db_host,
                        user=db_user,
                        password=db_pass,
                        database=db_database
                )
                mycursor = mydb.cursor()
                mycursor.execute("UPDATE users SET ltc_txid = %s, ltc_balance = ltc_balance + %s WHERE userid = %s", (str(new_ltc), str(ltc_amount), str(message.chat.id),))
                mydb.commit()
                bot.send_message(message.chat.id, "🎉 <b>New Deposit of " + str("{0:.8f}".format(float(doge_amount))) + " LTC Received</b>", parse_mode="html", reply_markup=menu())
            else:
                print("too many confirms LTC")
                pass
        else:
            pass
    except Exception as e:
        bot.send_message(message.chat.id, "ErRoR : "+ str(e))
# check ================================================================================#


# deposit ================================================================================#
def deposit(message):
    try:
        btc = user_btc_add(message.chat.id)
        ltc = user_ltc_add(message.chat.id)
        doge = user_doge_add(message.chat.id)
        bot.send_message(message.chat.id, "🧩 <b>Your Permanent Deposit Wallets : </b>\n\n<b>BTC : </b>[ <code>" + str(btc) + "</code> ]\n<b>LTC : </b>[ <code>" + str(ltc) + "</code> ]\n<b>DOGE : </b>[ <code>" + str(doge) + "</code> ]\n\n<i>You Depsit Will get Reflected Automatically Wait for 5 - 15 min</i>", parse_mode="html", reply_markup=menu())
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Error : "+ str(e))
# deposit ================================================================================#

# cancel 
def cancel(message):
    try:
        bot.send_message(message.chat.id, "<b> Welcome To Tipper Bot </b>", parse_mode="html", reply_markup=menu())
    except Exception as e:
        bot.send_message(message.chat.id, "- /start : error : " + str(e))
# cancel


# withdraw ================================================================================#
def withdraw(message):
    try:
        bot.send_message(message.chat.id, "<b>Select The Currency You Want To Withdraw : </b>", parse_mode="html", reply_markup=withdraw_menu())
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Error : "+ str(e))

# ltc ----------------------------------------------------------------------------------------------------------------------------------------
def withdraw_ltc(message):
    try:
        if message.text == "🚫 Cancel":
            cancel(message)
        else:
            global with_currency
            with_currency = "LTC"
            bot.send_message(message.chat.id, "<b>Send Your LITECOIN wallet addresss : </b>", parse_mode="html", reply_markup=cancel_menu())
            bot.register_next_step_handler(message, withdraw_ltc_address)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "error : "+ str(e))

def withdraw_ltc_address(message):
    try:
        if message.text == "🚫 Cancel":
            cancel(message)
        else:
            if check_address('ltc', str(message.text)) == "success":
                global with_address
                with_address = message.text
                bot.send_message(message.chat.id, "<b>Send the amount of LTC You want to withdraw : </b>", parse_mode="html")
                bot.register_next_step_handler(message, withdraw_ltc_amount)
            else:
                bot.send_message(message.chat.id, "Invalid Address!!")
                withdraw_ltc(message)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "error : "+ str(e))

def withdraw_ltc_amount(message):
    try:
        if message.text == "🚫 Cancel":
            cancel(message)
        else:
            if float(message.text) <= user_ltc_bal(message.chat.id) and float(message.text) > float(ltc_min_withdraw):
                global with_amount
                with_amount = message.text
                markup2 = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
                btn1 = types.KeyboardButton("🛒 Confirm 🎫")
                btn2 = types.KeyboardButton("🚫 Cancel")
                markup2.add(btn1)
                markup2.add(btn2)
                bot.send_message(message.chat.id, "✅ <b>Confirmation : </b>\n\n<b>Amount : </b>" +str(with_amount)+ " LTC\n<b>Address : </b>"+ str(with_address) + "\n\n♻ <b>Do you want to confirm This withdraw : </b>" , parse_mode="html", reply_markup=markup2)
                bot.register_next_step_handler(message, withdraw_final)
            else:
                bot.send_message(message.chat.id, "Invalid Amount Check Your Balance and Minimum Withdraw is " + str('%.8f'%(ltc_min_withdraw)) + " LTC")
                cancel(message)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "error : "+ str(e))
# ltc ----------------------------------------------------------------------------------------------------------------------------------------


# doge ---------------------------------------------------------------------------------------------------------------------------------------
def withdraw_doge(message):
    try:
        if message.text == "🚫 Cancel":
            cancel(message)
        else:
            global with_currency
            with_currency = "DOGE"
            bot.send_message(message.chat.id, "<b>Send Your DOGE wallet addresss : </b>", parse_mode="html", reply_markup=cancel_menu())
            bot.register_next_step_handler(message, withdraw_doge_address)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "error : "+ str(e))

def withdraw_doge_address(message):
    try:
        if message.text == "🚫 Cancel":
            cancel(message)
        else:
            if check_address('doge', str(message.text)) == "success":
                global with_address
                with_address = message.text
                bot.send_message(message.chat.id, "<b>Send the amount of DOGE You want to withdraw : </b>", parse_mode="html")
                bot.register_next_step_handler(message, withdraw_doge_amount)
            else:
                bot.send_message(message.chat.id, "Invalid Address!!")
                withdraw_doge(message)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "error : "+ str(e))

def withdraw_doge_amount(message):
    try:
        if message.text == "🚫 Cancel":
            cancel(message)
        else:
            if float(message.text) <= user_doge_bal(message.chat.id) and float(message.text) > float(doge_min_withdraw):
                global with_amount
                with_amount = message.text
                markup2 = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
                btn1 = types.KeyboardButton("🛒 Confirm 🎫")
                btn2 = types.KeyboardButton("🚫 Cancel")
                markup2.add(btn1)
                markup2.add(btn2)
                bot.send_message(message.chat.id, "✅ <b>Confirmation : </b>\n\n<b>Amount : </b>" +str(with_amount)+ " DOGE\n<b>Address : </b>"+ str(with_address) + "\n\n♻ <b>Do you want to confirm This withdraw : </b>" , parse_mode="html", reply_markup=markup2)
                bot.register_next_step_handler(message, withdraw_final)
            else:
                bot.send_message(message.chat.id, "Invalid Amount Check Your Balance and Minimum Withdraw is "+ str('%.8f'%(doge_min_withdraw)) +" DOGE")
                cancel(message)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "error : "+ str(e))
# doge -------------------------------------------------------------------------------------------------------------------------------------------

# btc --------------------------------------------------------------------------------------------------------------------------------------
def withdraw_btc(message):
    try:
        if message.text == "🚫 Cancel":
            cancel(message)
        else:
            global with_currency
            with_currency = "BTC"
            bot.send_message(message.chat.id, "<b>Send Your BITCOIN wallet addresss : </b>", parse_mode="html", reply_markup=cancel_menu())
            bot.register_next_step_handler(message, withdraw_btc_address)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "error : "+ str(e))

def withdraw_btc_address(message):
    try:
        if message.text == "🚫 Cancel":
            cancel(message)
        else:
            if check_address('btc', str(message.text)) == "success":
                global with_address
                with_address = message.text
                bot.send_message(message.chat.id, "<b>Send the amount of BTC You want to withdraw : </b>", parse_mode="html")
                bot.register_next_step_handler(message, withdraw_btc_amount)
            else:
                bot.send_message(message.chat.id, "Invalid Address!!")
                withdraw_btc(message)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "error : "+ str(e))

def withdraw_btc_amount(message):
    try:
        if message.text == "🚫 Cancel":
            cancel(message)
        else:
            if float(message.text) <= user_btc_bal(message.chat.id) and float(message.text) > float(btc_min_withdraw):
                global with_amount
                with_amount = message.text
                markup2 = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
                btn1 = types.KeyboardButton("🛒 Confirm 🎫")
                btn2 = types.KeyboardButton("🚫 Cancel")
                markup2.add(btn1)
                markup2.add(btn2)
                bot.send_message(message.chat.id, "✅ <b>Confirmation : </b>\n\n<b>Amount : </b>" +str(with_amount)+ " BTC\n<b>Address : </b>"+ str(with_address) + "\n\n♻ <b>Do you want to confirm This withdraw :</b> " , parse_mode="html", reply_markup=markup2)
                bot.register_next_step_handler(message, withdraw_final)
            else:
                bot.send_message(message.chat.id, "Invalid Amount Check Your Balance and Minimum Withdraw is " + str('%.8f'%(btc_min_withdraw))+ " BTC")
                cancel(message)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "error : "+ str(e))
# btc --------------------------------------------------------------------------------------------------------------------------------------

def withdraw_final(message):
    if message.text == "🚫 Cancel":
        cancel(message)
    else:
        try:
            amu = with_amount
            addre = with_address
            currr = with_currency
            txid = make_Withdraw(str(currr), str(amu), str(addre))
            bot.send_message(message.chat.id, "Making Withdraw now\n\n" + str(amu) +"\n"+str(addre)+"\n"+str(currr) + "\n" + str(txid), parse_mode="html", reply_markup=menu())
        except Exception as e:
            bot.send_message(adminid, "Please check Your Wapi Details and also top up some balance \n\nA user just tried to withdraw\n\nError : "+ str(e))
            bot.send_message(message.chat.id, "Withdraw Failed Contact admin : "+'<a href="' + 'tg://user?id=' + str(adminid) + '"><strong>Admin Link 😎</strong></a>'+"")
# withdraw ================================================================================#

# info ===============================================================================#
def info(message):
    try:
        bot.send_message(message.chat.id, bot_info, parse_mode="html", reply_markup=menu())
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Error : "+ str(e))
# info ===============================================================================#


# cmd bal =========================================================================#
@bot.message_handler(commands=['bal', 'balance', 'acc', 'account'])
def cmd_bal(message):
    try:
        if user_check(message.from_user.id) > 0:
            btc = user_btc_bal(message.from_user.id)
            ltc = user_ltc_bal(message.from_user.id)
            doge = user_doge_bal(message.from_user.id)
            bot.reply_to(message, "💳 <b>BTC :</b> <code>"+ str('%.8f'%(float(btc))) + " BTC</code>\n💶 <b>LTC :</b> <code>"+ str("%.8f"%(float(ltc))) +" LTC</code>\n💷 <b>DOGE :</b> <code>" + str("%.8f"%(float(doge))) +" DOGE </code>", parse_mode="html")
        else:
            bot.reply_to(message, "<b>User Not Registered !!</b>\n<i>start this bot to get registered</i> - @"+ str(bot.get_me().username) +"", parse_mode="html")
    except:
        bot.reply_to(message, "💳 <b>BTC :</b> <code>"+ str(user_btc_bal(message.from_user.id)) + " BTC</code>\n💶 <b>LTC :</b> <code>"+ str(user_ltc_bal(message.from_user.id)) +" LTC</code>\n💷 <b>DOGE :</b> <code>" + str(user_doge_bal(message.from_user.id)) +" DOGE </code>", parse_mode="html")
# cmd bal =========================================================================#

# instant bet =================================================================================#
@bot.message_handler(commands=['bet', 'gamble'])
def inst_bets(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        chatids = (message.from_user.id)
    elif message.chat.type == "private":
        chatids = (message.chat.id)
    #try:
    msg = message.text.split(" ",3)
    amount = msg[1]
    percent = msg[2]
    op = msg[3]
    if float(amount) <= float(user_doge_bal(chatids)):
        if float(amount) > 0.9:
            ran_per = randint(1, 100)
            if op == "hi":
                if int(ran_per) > int(percent):
                    perrr = (int(percent)/100)
                    #print(float(perrr))
                    amu = int(amount) + 0.0000
                    #print(amu)
                    bos = float(amu) * float(perrr)
                    #user_bal_add(chatids, float(bos))
                    user_add_bal(chatids, float(bos), "doge")
                    bot.reply_to(message, "😎 "+'<a href="' + 'tg://user?id=' + str(message.from_user.id) + '"><strong>' + str(message.from_user.first_name) +'</strong></a>'+"\n⏹<b> Target :</b> Above "+ str(percent) + "\n🧻 <b>Roll :</b> "+ str(ran_per) +"%\n💸 <b>Bet :</b> "+ str(amount)+" DOGE\n📈 <b>Won :</b> +"+ str(bos), parse_mode="html")
                else:
                    user_remove_bal(chatids, amount, "doge")
                    bot.reply_to(message, "😎 "+'<a href="' + 'tg://user?id=' + str(message.from_user.id) + '"><strong>' + str(message.from_user.first_name) +'</strong></a>'+"\n⏹ <b>Target :</b> Above "+ str(percent) + "\n🧻 <b>Roll :</b> "+ str(ran_per) +"%\n💸 <b>Bet :</b> "+ str(amount)+" DOGE\n📉 <b>Lost :</b> -"+ str(amount), parse_mode="html")
            if op == "lo":
                if int(ran_per) < int(percent):
                    percen = 100 - int(percent)
                    perrr = (int(percen)/100)
                    amu = int(amount) + 0.0000
                    bos = float(amu) * float(perrr)
                    user_add_bal(chatids, float(bos), "doge")
                    bot.reply_to(message, "😎 <b>User : </b>"+ str(message.from_user.first_name)+"\n⏹ <b>Target :</b> Under "+ str(percent) + "\n🧻 <b>Roll :</b> "+ str(ran_per) +"%\n💸 <b>Bet :</b> "+ str(amount)+"\n📈 <b>Won :</b> +"+ str(bos), parse_mode="html")
                else:
                    user_remove_bal(chatids, amount, "doge")
                    bot.reply_to(message, "😎 <b>User : </b>"+ str(message.from_user.first_name)+"\n⏹ <b>Target :</b> Under "+ str(percent) + "\n🧻 <b>Roll :</b> "+ str(ran_per) +"%\n💸 <b>Bet :</b> "+ str(amount)+"\n📉 <b>Lost :</b> -"+ str(amount), parse_mode="html")
        else:
            bot.send_message(chatids, "Minimum Bet Amount is 1 DOGE")
    else:
        bot.send_message(chatids, "You dont have sufficient balance!")
    #except:
     #   bot.reply_to(message, "Use the correct Format!\n<code>/bet amount percentage hi/lo</code>\n<b>Example : </b><code>/bet 20 90 hi</code>", parse_mode="html")
# instant bet =================================================================================#


# tip ================================================================================#
@bot.message_handler(commands=['tip', 'send', 'transfer'])
def tipping(message):
    if message.chat.type != "private":
        try:
            mesg = message.text
            msg = mesg.split(" ")
            amount = msg[1]
            cur = msg[2]
            if cur == "doge" or cur == "BTC" or cur == "btc" or cur == "DOGE" or cur == "LTC" or cur == "ltc":
                if user_check(message.from_user.id) > 0:
                    if user_check(message.reply_to_message.from_user.id) > 0:
                        if cur.isupper():
                            currency = cur
                        else:
                            currency = cur.upper()
                        if currency == "BTC":
                            user_balance = user_btc_bal(message.from_user.id)
                            minimum = 0.000000001
                        elif currency == "LTC":
                            user_balance = user_ltc_bal(message.from_user.id)
                            minimum = 0.000000001
                        elif currency == "DOGE":
                            user_balance = user_doge_bal(message.from_user.id)
                            minimum = 0.001
                        if float(amount) <= float(user_balance):
                            if float(amount) > float(minimum):
                                try:
                                    bot.send_message(message.reply_to_message.from_user.id, "<b>You Just received "+ str(amount) +" "+ str(currency) +" from</b> "+'<a href="' + 'tg://user?id=' + str(message.from_user.id) + '"><strong>' + str(message.from_user.id) +'</strong></a>'+" <b>In chat Group </b>"+ '<a href="' + 'https://t.me/'+ str(message.chat.username) +'"><strong>'+ str(message.chat.title) +'</strong></a>'+ " ", parse_mode="html")
                                    #bot.send_message(message.chat.id, message.from_user.id)
                                    user_add_bal(message.reply_to_message.from_user.id, amount, currency)
                                    user_remove_bal(message.from_user.id, amount, currency)
                                    #bot.send_message(message.chat.id, str(message.reply_to_message.from_user.id) + "\nmsg: "+ str(message.reply_to_message.message_id))
                                    frommm = ""+'<a href="' + 'tg://user?id=' + str(message.from_user.id) + '"><strong>' + str(message.from_user.first_name) +'</strong></a>'+""
                                    tooop = ""+'<a href="' + 'tg://user?id=' + str(message.reply_to_message.from_user.id) + '"><strong>' + str(message.reply_to_message.from_user.first_name) +'</strong></a>'+""
                                    bot.reply_to(message.reply_to_message, "🎫 "+ str(frommm) +"<b> tip </b>"+ str(tooop) +" <b>" + str(amount) + " "+ str(currency) + "</b>", parse_mode="html")
                                except Exception as e:
                                    bot.reply_to(message, "<b>User Not Registered !!</b>\n<i>start this bot to get Receive The tip</i> - @"+ str(bot.get_me().username) +"", parse_mode="html")
                            else:
                                bot.send_message(message.chat.id, "Your Tip is smaller than minimum!!")
                        else:
                            bot.send_message(message.chat.id, "<b>You Dont Have Enough </b><code>Balance!</code>", parse_mode="html")
                    else:
                        bot.reply_to(message, "<b>User Not Registered !!</b>\n<i>start this bot to get Receive The tip</i> - @"+ str(bot.get_me().username) +"", parse_mode="html")
                else:
                    bot.reply_to(message, "<b>User Not Registered !!</b>\n<i>start this bot to get registered</i> - @"+ str(bot.get_me().username) +"", parse_mode="html")
            else:
                bot.reply_to(message, "Invalid Currency")
        except Exception as e:
            print(e)
            bot.reply_to(message, "‼<b> Use the Correct Format : </b>\n<code>/tip amount currency</code>\n<i>/tip 10 DOGE</i>\nor\n<i>/tip 10 doge</i>", parse_mode="html")
    else:
        bot.send_message(message.chat.id, "Only Allowed IN groups/supergroups")
# tip ================================================================================#


# rain ================================================================================#
@bot.message_handler(commands=['rain', 'shit', 'flush', 'spread', 'incinerate'])
def rain(message):
    try:
        if message.chat.type != "private":
            msg = message.text.split(" ", 2)
            ammmm  = msg[1]
            currency = msg[2]
            if currency == "btc" or currency == "BTC" or currency == "ltc" or currency == "LTC" or currency == "doge" or currency == "DOGE":
                if ammmm == "all" or ammmm == "full":
                    if currency == "doge" or currency == "DOGE":
                        amount = user_doge_bal(message.from_user.id)
                    elif currency == "btc" or currency == "BTC":
                        amount = user_btc_bal(message.from_user.id)
                    elif currency == "ltc" or currency == "LTC":
                        amount = user_ltc_bal(message.from_user.id)
                else:
                    amount = ammmm
                if currency == "doge" or currency == "DOGE":
                    if float(amount) <= float(user_doge_bal(message.from_user.id)):
                        if float(amount) > 0.01:
                            mydb = mysql.connector.connect(
                                host=db_host,
                                user=db_user,
                                password=db_pass,
                                database=db_database
                            )
                            mycursor = mydb.cursor()
                            ti = time.time() - float(active_users_store_time)
                            mycursor.execute("SELECT userid FROM users WHERE last_message >= " + str(ti) + "")
                            myres = mycursor.fetchall()
                            msgg = " "
                            if mycursor.rowcount != 0 and mycursor.rowcount >= 2:
                                rain_amount = float(amount) / float(mycursor.rowcount - 1)
                                user_remove_bal(message.from_user.id, amount, 'doge')
                                for x in myres:
                                    active = x[0]
                                    if active == message.from_user.id:
                                        msgg += ""
                                    else:
                                        msgg += "| "+'<a href="' + 'tg://user?id=' + str(active) + '"><strong>' + str(active) +'</strong></a>'+" | "
                                        user_add_bal(active, rain_amount, 'doge')
                                bot.send_message(message.chat.id, "🎭 Total Users  = " + str(mycursor.rowcount - 1) + "\n⛈ Total Rain Amount : " + str(amount) + " DOGE\n💦 Per User  = " + str("{0:.10f}".format(float(rain_amount))) + " DOGE\n\n💢💢💢💢💢💢💢💢💢\n" + str(msgg), parse_mode="html")
                            else:
                                bot.reply_to(message, "⚡<b> No Active Users</b>", parse_mode="html")
                        else:
                            bot.reply_to(message, "☔ <b>Minimum Rain Allowed = 0.01 DOGE</b>", parse_mode="html")
                    else:
                        bot.reply_to(message, "☂ <b>You Dont have Sufficient Balance !</b>", parse_mode="html")
                elif currency == "btc" or currency == "BTC":
                    if float(amount) <= float(user_btc_bal(message.from_user.id)):
                        if float(amount) > 0.000000082:
                            mydb = mysql.connector.connect(
                                host=db_host,
                                user=db_user,
                                password=db_pass,
                                database=db_database
                            )
                            mycursor = mydb.cursor()
                            ti = time.time() - float(active_users_store_time)
                            mycursor.execute("SELECT userid FROM users WHERE last_message >= " + str(ti) + "")
                            myres = mycursor.fetchall()
                            msgg = " "
                            if mycursor.rowcount != 0 and mycursor.rowcount >= 2:
                                rain_amount = float(amount) / float(mycursor.rowcount - 1)
                                user_remove_bal(message.from_user.id, amount, 'btc')
                                for x in myres:
                                    active = x[0]
                                    if active == message.from_user.id:
                                        msgg += ""
                                    else:
                                        msgg += "| "+'<a href="' + 'tg://user?id=' + str(active) + '"><strong>' + str(active) +'</strong></a>'+" | "
                                        user_add_bal(active, rain_amount, 'btc')
                                bot.send_message(message.chat.id, "🎭 Total Users  = " + str(mycursor.rowcount - 1) + "\n⛈ Total Rain Amount : " + str(amount) + " BTC\n💦 Per User  = " + str("{0:.10f}".format(float(rain_amount))) + " BTC\n\n💢💢💢💢💢💢💢💢💢\n" + str(msgg), parse_mode="html")
                            else:
                                bot.reply_to(message, "⚡<b> No Active Users</b>", parse_mode="html")
                        else:
                            bot.reply_to(message, "☔ <b>Minimum Rain Allowed = 0.000000082 BTC</b>", parse_mode="html")
                    else:
                        bot.reply_to(message, "☂ <b>You Dont have Sufficient Balance !</b>", parse_mode="html")
                elif currency == "ltc" or currency == "LTC":
                    if float(amount) <= float(user_ltc_bal(message.from_user.id)):
                        if float(amount) > 0.0000082:
                            mydb = mysql.connector.connect(
                                host=db_host,
                                user=db_user,
                                password=db_pass,
                                database=db_database
                            )
                            mycursor = mydb.cursor()
                            ti = time.time() - float(active_users_store_time)
                            mycursor.execute("SELECT userid FROM users WHERE last_message >= " + str(ti) + "")
                            myres = mycursor.fetchall()
                            msgg = " "
                            if mycursor.rowcount != 0 and mycursor.rowcount >= 2:
                                rain_amount = float(amount) / float(mycursor.rowcount - 1)
                                user_remove_bal(message.from_user.id, amount, 'ltc')
                                for x in myres:
                                    active = x[0]
                                    if active == message.from_user.id:
                                        msgg += ""
                                    else:
                                        msgg += "| "+'<a href="' + 'tg://user?id=' + str(active) + '"><strong>' + str(active) +'</strong></a>'+" | "
                                        user_add_bal(active, rain_amount, 'ltc')
                                bot.send_message(message.chat.id, "🎭 Total Users  = " + str(mycursor.rowcount - 1) + "\n⛈ Total Rain Amount : " + str(amount) + " LTC\n💦 Per User  = " + str("{0:.10f}".format(float(rain_amount))) + " LTC\n\n💢💢💢💢💢💢💢💢💢\n" + str(msgg), parse_mode="html")
                            else:
                                bot.reply_to(message, "⚡<b> No Active Users</b>", parse_mode="html")
                        else:
                            bot.reply_to(message, "☔ <b>Minimum Rain Allowed = 0.0000082 LTC</b>", parse_mode="html")
                    else:
                        bot.reply_to(message, "☂ <b>You Dont have Sufficient Balance !</b>", parse_mode="html")
            else:
                bot.reply_to(message, "Invalid Currency")
        else:
            bot.reply_to(message, "Only Allowed IN groups/supergroups")
    except:
        bot.send_message(message.chat.id, "Use the Correct Format!!\n<code>/rain 10 DOGE</code>", parse_mode="html")
# rain ================================================================================#


# active ================================================================================#
@bot.message_handler(commands=['active'])
def active_users(message):
    try:
        acti = get_active()
        bot.reply_to(message, "⚡ <b>"+ str(acti) +" Users Are Active</b>", parse_mode="html")
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Error : "+ str(e))
# active ================================================================================#


# start ================================================================================#
@bot.message_handler(commands=['start'])
def start_message(message):
    if message.chat.type != "group" and message.chat.type != "supergroup":
        try:
            row = user_check(message.chat.id)
            if row == 0:
                print("new")
                btc = generate_address('btc')
                doge = generate_address('doge')
                ltc = generate_address('ltc')
                mydb = mysql.connector.connect(
                            host=db_host,
                            user=db_user,
                            password=db_pass,
                            database=db_database
                )
                mycursor = mydb.cursor()
                sql = "INSERT INTO users (userid, btc_address, ltc_address, doge_address) VALUES (%s, %s, %s, %s)"
                val = (str(message.chat.id), str(btc), str(ltc), str(doge))
                mycursor.execute(sql, val)
                mydb.commit()
                bot.send_message(message.chat.id, bot_name, parse_mode="html", reply_markup=menu())
            else:
                bot.send_message(message.chat.id, bot_name, parse_mode="html", reply_markup=menu())
        except Exception as e:
            print(e)
            bot.send_message(message.chat.id, "ERror : "+ str(e))
# start ================================================================================#


# ----- ================================================================================#
@bot.message_handler(content_types=['text'])
def buttons_setup(message):
    if message.chat.type != "private":
        if user_check(message.from_user.id) > 0:
            mydb = mysql.connector.connect(
                    host=db_host,
                    user=db_user,
                    password=db_pass,
                    database=db_database
            )
            mycursor = mydb.cursor()
            mycursor.execute("UPDATE users SET last_message = %s WHERE userid = %s", (str(round(time.time(), 2)), str(message.from_user.id)))
            mydb.commit()
            #set_user_msg_time(message.chat.id, round(time.time(), 3))
            #bot.send_message(message.chat.id, "Storing id to active users")
        else:
            print("new one in rain")
            btc = generate_address('btc')
            doge = generate_address('doge')
            ltc = generate_address('ltc')
            mydb = mysql.connector.connect(
                        host=db_host,
                        user=db_user,
                        password=db_pass,
                        database=db_database
            )
            mycursor = mydb.cursor()
            sql = "INSERT INTO users (userid, btc_address, ltc_address, doge_address) VALUES (%s, %s, %s, %s)"
            val = (str(message.from_user.id), str(btc), str(ltc), str(doge))
            mycursor.execute(sql, val)
            mydb.commit()
            mycursor.execute("UPDATE users SET last_message = %s WHERE userid = %s", (str(round(time.time(), 2)), str(message.from_user.id)))
            mydb.commit()
            print("registered !!")
    elif message.text == button1 and message.chat.type != "group" and message.chat.type != "supergroup":
        bal(message)
    elif message.text == button2 and message.chat.type != "group" and message.chat.type != "supergroup":
        deposit(message)
    elif message.text == button3 and message.chat.type != "group" and message.chat.type != "supergroup":
        withdraw(message)
    elif message.text == button4 and message.chat.type != "group" and message.chat.type != "supergroup":
        info(message)
    elif message.text == "BTC" and message.chat.type != "group" and message.chat.type != "supergroup":
        withdraw_btc(message)
    elif message.text == "DOGE" and message.chat.type != "group" and message.chat.type != "supergroup":
        withdraw_doge(message)
    elif message.text == "LTC" and message.chat.type != "group" and message.chat.type != "supergroup":
        withdraw_ltc(message)
    elif message.text == "🚫 Cancel" and message.chat.type != "group" and message.chat.type != "supergroup":
        cancel(message)
# ------ ================================================================================#

bot.polling()