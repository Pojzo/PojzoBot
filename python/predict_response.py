checkpoint_path = "training_checkpoints/cp.ckpt"
from main import create_model
import main
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
import pickle
from tensorflow import keras
import json
import numpy as np

data = None # There is probably a better way to do this
tokenizer = None #  --.--
LabelEncoder = None # --.--

try:
    model = keras.models.load_model("model")
except:
    print("Unable to load saved model")

with open("intents.json") as file:
    data = json.load(file)

with open('tokenizer.pickle', 'rb') as t:
    tokenizer = pickle.load(t)

with open('label_encoder.pickle', 'rb') as l:
    label_encoder = pickle.load(l)



max_len = main.max_len

def predict(text):
    sequences = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(sequences, truncating='post', maxlen=max_len)
    result = model.predict(padded)


    tag = label_encoder.inverse_transform([np.argmax(result)])

    for i in data['intents']:
        if i['tag'] == tag:
            return np.random.choice(i['responses'])

