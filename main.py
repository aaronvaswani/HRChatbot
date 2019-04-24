from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from flask import Flask, render_template, request, redirect, url_for, flash, Response
import logging
import time
import nltk

app = Flask(__name__)

#driver = webdriver.Chrome()

bot = ChatBot(
            'Bob',            
            # read_only=True,
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            database_uri=None,
            logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'I apologize, I do not understand. Can you rephrase?',
                'maximum_similarity_threshold': 0.9
            }
    ]
)

storeusers = "userhistory.csv"

def loadReward():
    trainer.train("./Reward/rewardBalance.yml")
    trainer.train("./Reward/rewardGeneral.yml")
    trainer.train("./Reward/rewardHealth.yml")
    trainer.train("./Reward/rewardInsurance.yml")
    trainer.train("./Reward/rewardPension.yml")

trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.english")
trainer.train("./Corpus/trivial.yml")
trainer.train("./Corpus/greetings.yml")
trainer.train("./Corpus/general.yml")
trainer.train("./Corpus/counterresponse.yml")

@app.route("/")
def home():
    return render_template("start.html",
    data = [{'function':'Reward'}, {'function':'Recruitment'}, {'function':'Compensation'}])

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        enteredname = request.form['username']
        enteredfunctionobj = request.form.get('jobFunction')        
        enteredfunction = str(enteredfunctionobj)
        if enteredname != "" and enteredfunction != "":
            userstore = open(storeusers, "a")
            userstore.write('\n' + enteredname + ',' + enteredfunction)
            userstore.close()
            if (enteredfunction == "Reward"):
               loadReward()
            #if entered function is x, load x, repeat for y,z etc
            return render_template("index.html")
        else:
            return Response('<p>Login failed</p>')

@app.route("/app", methods=['GET'])
def chatbot():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    if (userText == "break" or userText == "bye"):
        return str("bye!")        
    else:
        return str(bot.get_response(userText))

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

if __name__ == "__main__":
    app.run()

while True:
    try:
        user_input = input(': ')

        #Breaks out of while loop and quits the chat bot
        if (user_input == "break" or user_input == "bye"):
            print("bye!")
            break

        bot_response = bot.get_response(user_input)

        print(bot_response)

    except(KeyboardInterrupt, EOFError, SystemExit):
        break