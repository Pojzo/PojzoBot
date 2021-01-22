# using this https://towardsdatascience.com/how-to-build-your-own-chatbot-using-deep-learning-bb41f970e281

import json
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import model_from_json
import pickle


# assert(len(tf.config.list_physical_devices('GPU')))

with open('intents.json') as file:
    data = json.load(file)

training_sentences = []
training_labels = []
labels = []
responses = []

for intent in data['intents']:
    for pattern in intent['patterns']:
        training_sentences.append(pattern)
        training_labels.append(intent['tag'])

    responses.append(intent['responses'])

    if intent['tag'] not in labels:
        labels.append(intent['tag'])

num_classes = len(labels)

label_encoder = LabelEncoder()
label_encoder.fit(training_labels)
training_labels = label_encoder.transform(training_labels)

vocab_size = 1000
embedding_dim = 16
max_len = 20
oov_token = "<OOV>"

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token)
tokenizer.fit_on_texts(training_sentences)
word_index = tokenizer.word_index

sequences = tokenizer.texts_to_sequences(training_sentences)
padded_sequences = pad_sequences(sequences, truncating='post', maxlen=max_len)


def create_model():
    model = Sequential([
        Embedding(vocab_size, embedding_dim, input_length=max_len),
        GlobalAveragePooling1D(),
        Dense(16, activation='relu'),
        Dense(16, activation='relu'),
        Dense(num_classes, activation='softmax')
    ])
    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer=('adam'),
                  metrics=['accuracy']
                  )
    return model


def train_model(new=True, epochs=500): # THIS IS VERY SHITTY CODE, WILL REWRITE LATER
    if not new:
        with open("json_model.json", 'r') as json_file:
            loaded_json = json_file.read()
        model = model_from_json(loaded_json)
        model.load_weights("weights_model.h5")
        model.compile(loss='sparse_categorical_crossentropy',
                      optimizer=('adam'),
                      metrics=['accuracy']
                      )
        print("Loaded model")
    else:
        model = create_model()

    history = model.fit(padded_sequences, np.array(
        training_labels), epochs=epochs)
    model_json = model.to_json()
    with open("json_model.json", 'w') as json_file:
        json_file.write(model_json)

    model.save_weights("weights_model.h5")


with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

# to save the fitted label encoder
with open('label_encoder.pickle', 'wb') as ecn_file:
    pickle.dump(label_encoder, ecn_file, protocol=pickle.HIGHEST_PROTOCOL)
