import json
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
import numpy as np
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.models import Sequential

training_sentences = []
training_labels = []
labels = []
responses = []

with open("chat_intents.json") as file: # load training data 
    chat_intents = json.load(file)

with open("command_intents.json") as file: # load training data
    command_intents = json.load(file)

for intent in chat_intents['intents']:
    for pattern in intent['patterns']:
        training_sentences.append(pattern)
        training_labels.append(intent['type'])

    responses.append(intent['responses'])

for intent in command_intents['intents']:
    for pattern in intent['patterns']:
        training_sentences.append(pattern)
        training_labels.append(intent['type'])

    responses.append(intent['responses'])

num_classes = 2

label_encoder = LabelEncoder()
label_encoder.fit(training_labels)
training_labels = label_encoder.transform(training_labels)

vocab_size = 1000
embedding_dim = 16
max_len = 20
oov_token = "<OOV>"

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token)
tokenizer.fit_on_texts(training_sentences)

sequences = tokenizer.texts_to_sequences(training_sentences)

padded_sequences = pad_sequences(sequences, truncating="post", maxlen=max_len)

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
                  metrics=['accuracy'])

    return model

def train(model, epochs=500):
    history = model.fit(padded_sequences, np.array(training_labels), epochs=epochs)

    return history

#model = create_model()
model = tf.keras.models.load_model("determine_model")

#train(model)

def predict(text):
    predict_sequences = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(predict_sequences, truncating='post', maxlen=max_len)
    result = model.predict(padded)
    tag = label_encoder.inverse_transform([np.argmax(result)])

    return tag






