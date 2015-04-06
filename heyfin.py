# -*- coding: utf-8 -*-
import time
import praw
import sqlite3
import random
import os


user_agent = "user comment karma checking script ,v0.1 by /u/hurbraa"
r = praw.Reddit(user_agent=user_agent) 
r.login(os.environ['REDDIT_USER'], os.environ['REDDIT_PASS'])


dongers = { "a" :"ᕕ༼ ͠ຈ Ĺ̯ ͠ຈ ༽┌∩┐", "b" :"╭∩╮(ಠ۝ಠ)╭∩╮",  "c" :"凸( •̀_•́ )凸",  "d" :"┌∩┐(ಠ͜ʖಠ)┌∩┐",  "f" :" ੧༼ ◕ ∧ ◕ ༽┌∩┐",  "g" :"┌∩┐╭˵ಥ o ಥ˵╮┌∩┐",  "h" :"┌∩┐(◕◡◉)┌∩┐",  "i" :"╭∩╮( ͡° ل͟ ͡° )╭∩╮",  "j" :"╭∩╮ʕ ◉ ﹏ ◉ ʔ╭∩╮",  "k" :"ᕕ▒ ຈ ︿ ຈ ▒┌∩┐",  "l" :"٩║ ✿ ᴼ ل ᴼ ✿ ║┌∩┐",  "m" :"┌∩┐༼ ºل͟º ༽┌∩┐",  "n": "୧༼◔益◔╭∩╮༽",  "o" :"凸༼ຈل͜ຈ༽凸" }
messages = [ ", you have got %i karma. Calm down a bit, I need to catch up. Btw, i'm a bot, I bet you didn' know it." , ", fuck off with your shitty-ass %i karma whoring" , ", GYUIAUYASAS I CAN'T BELIEVE YOU ARE GETTING SO MUCH KARMA(%i) AGAIN FUCK OFFFFFFFFF SRSLY" , ", cancel 10k karma contest, u got %i karma points. " , ", I noticed you are getting some (%i) imaginary internet points in a comment for some reason. I recommend deleting the comment AND your account before something dangerous happens. Who knows what those points mean, maybe they like put you on a NSA watchlist or something."]



print("Opening database...")
sql = sqlite3.connect("sql.db")
cur = sql.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS oldposts(ID TEXT)")
sql.commit()

WAIT = 60

def pmBot():
    try:
        user_name = "Finlanderr"
        user = r.get_redditor(user_name)
        gen = user.get_comments()
        print ("Starting to analyze the comments")
        for comment in gen:
            karma = comment.ups - comment.downs
            cur.execute("SELECT * FROM oldposts WHERE ID=?", [comment.id])
            if not cur.fetchone():
                if karma > 10:
                    print("Sending Message")
                    dvalues = list(dongers.values())
                    msgself = "ALERT! FINLANDER HAS RECEIVED %i KARMA AND STILL COUNTING.\n LINK TO COMMENT: %s" % (karma , comment.permalink)
                    msgfin = "Hey Fin " + random.choice(dvalues) + random.choice(messages) % (karma)
                    #r.send_message('hurbraa', 'FINLANDER KARMA ALERT', msgself)
                    #r.send_message('finlanderr', 'HEY FIN', msgfin)
                    print(msgself, "\n")
                    print(msgfin , "\n")
                    cur.execute("INSERT INTO oldposts VALUES(?)", [comment.id])
                    sql.commit()
                    print("SQL.COMMIT DONE")
                else:
                    print("Comment doesn't have enough karma... getting a new comment")
            else:
                print("Comment ID matches a comment ID in the SQL database. Searching for a new comment...")
                continue
    except praw.errors.RateLimitExceeded as error:
        print("Sleeping %d seconds" % error.sleep_time)
        time.sleep(error.sleep_time)
    except praw.errors.APIException as error:
        print("Reddit Exception: Sleeping for 5 minutes")
        time.sleep(300)
    except Exception as e:
        print ("[ERROR]:", e)
        print ("Blindly handling error")


while True:
    pmBot()
    print("Waiting " + str(WAIT) + " seconds")
    time.sleep(WAIT)



