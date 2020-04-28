import keras
from keras.preprocessing.sequence import pad_sequences
import pickle
import re
import nltk
import itertools
import matplotlib.pyplot as plt
from nltk.stem.wordnet import WordNetLemmatizer 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from autocorrect import spell
nltk.download('stopwords')
stop_words = set(stopwords.words('english')) 
nltk.download('words')
words = set(nltk.corpus.words.words())
nltk.download('punkt')
nltk.download('wordnet')
g = open('tokenizer.pickle', 'rb')
pro = pickle.load(g)


def load_slang():
    slangdict = dict()
    with open('slang.txt','rt') as f:
        for line in f:
            spl = line.split('\t')
            slangdict[spl[0]] = spl[1][:-1]
    return slangdict

slang_words = load_slang()


def remove_elongated(text):
    pattern = re.compile(r"(.)\1{2,}")
    return pattern.sub(r"\1\1", text)


def data_cleaning(tweet, slang_words):
    
    lem = WordNetLemmatizer()
    
    tweet = re.sub("@[\w\d]+", "", tweet)
    tweet = re.sub("http:[\w\:\/\.]+","", tweet)   
    tweet = re.sub('[^[A-Za-z]\s]','', tweet)     
    tweet=  re.sub('[^a-zA-Z]',' ', tweet)
    tweet = re.sub('[^\w\s]','', tweet)            
    tweet = tweet.lower()
    
    tweet = ''.join(''.join(s)[:2] for _, s in itertools.groupby(tweet))
    
    tokens = nltk.tokenize.word_tokenize(tweet)
    
    tokens = [token if token not in slang_words else slang_words[token] for token in tokens]
    
    tokens = [token for token in tokens if not token in stop_words]
    
    tokens = [lem.lemmatize(token) for token in tokens]
    tokens = [remove_elongated(token) for token in tokens]
    
    tokens = [spell(token) for token in tokens]
    
    tokens = [token if len(token)>1 else token.replace(token,"") for token in tokens ]
    
    return tokens


model = keras.models.load_model("model.hdf5")

def pred(text):
    feature_array = data_cleaning(text, slang_words)
    feature_array=[feature_array]
    new1=pro.texts_to_sequences(feature_array)
    new2=pad_sequences(new1, maxlen = 50)
    prediction = model.predict(new2)
    pred = [x for x in prediction[0]]
    pred1 = [(x/(max(pred)))*100 for x in pred]
    return pred1
