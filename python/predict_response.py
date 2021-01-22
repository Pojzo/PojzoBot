
import time
start_time = time.time();
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import sys
import numpy as np
import json
from tensorflow.keras.models import model_from_json
import pickle
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import argparse


# VERY SHITTY CODE, WILL REWRITE LATER

checkpoint_path = "training_checkpoints/cp.ckpt"
os.chdir(r"C:\Users\pojzi\OneDrive\Plocha\Programovanie\javascript\DiscordBot.v2\python")


parser = argparse.ArgumentParser(description='Test.')
parser.add_argument('text', type=str), 
args = parser.parse_args()

try:
    with open("json_model.json", 'r') as json_file:
        loaded_json = json_file.read()
    model = model_from_json(loaded_json)
    model.load_weights("weights_model.h5")
    model.compile(loss='sparse_categorical_crossentropy',
                    optimizer=('adam'),
                    metrics=['accuracy']
                    )
except:
    print("Unable to load saved model")

with open("intents.json") as file:
    data = json.load(file)

with open('tokenizer.pickle', 'rb') as t:
    tokenizer = pickle.load(t)

with open('label_encoder.pickle', 'rb') as l:
    label_encoder = pickle.load(l)

max_len = 20
text = args.text

sequences = tokenizer.texts_to_sequences([text])
padded = pad_sequences(sequences, truncating='post', maxlen=max_len)
result = model.predict(padded)


tag = label_encoder.inverse_transform([np.argmax(result)])

for i in data['intents']:
    if i['tag'] == tag:
        sys.stdout.write(np.random.choice(i['responses']))
        sys.stdout.flush()

