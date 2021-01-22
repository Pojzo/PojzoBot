import json
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder

assert(len(tf.config.list_physical_devices('GPU')))

with open('intents.json') as file:
    data = json.load(file)

training_sentences = []
trainng_labels = []
labels = []
responses = []

print(data)
