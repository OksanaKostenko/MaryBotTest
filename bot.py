import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
import random
import datetime

robo_name = "MaryBotTest"
user_name = "User"

with open('chatbot.txt','r',errors = 'ignore') as file:
    raw = file.read().lower()
    
nltk.download('punkt') # first-time use only
nltk.download('wordnet') # first-time use only

sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
word_tokens = nltk.word_tokenize(raw)# converts to list of words

lemmer = nltk.stem.WordNetLemmatizer()
#WordNet is a semantically-oriented dictionary of English included in NLTK.

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "hi there", "hello", "I am glad! You are talking to me", "Oh no, that's you..."]

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)
        
def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)

    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]

    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response
    
def write_to_log(*args):
    pass
#    with open("log.txt", 'a') as log:
#        log.write(" /// ".join(args)+ "\n")
        
def chat(user_response):
    write_to_log(str(datetime.datetime.now()), user_name, user_response)
    user_response=user_response.lower()
    bot_response = ""
    
    if (user_response=='/start'):
        bot_response = "My name is {}. I will answer your queries about Chatbots. If you want to exit, type Bye".format(robo_name)

    elif (user_response=='bye'):
        bot_response = random.choice(["Bye! take care..", "See you soon!","Bye-bye, darling!"])
        
    elif (user_response=='thanks' or user_response=='thank you'):
        bot_response = "You are welcome.."

    elif (greeting(user_response)!=None):
        bot_response = greeting(user_response)

    else:
        bot_response = response(user_response)
        sent_tokens.remove(user_response)

    write_to_log(str(datetime.datetime.now()), robo_name, bot_response)
    return bot_response
