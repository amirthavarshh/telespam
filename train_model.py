import pandas as pd
import nltk
import re
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

print("Loading dataset...")

nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    words = text.split()
    words = [w for w in words if w not in stop_words]
    return " ".join(words)


# LOAD DATA
df = pd.read_csv("spam.csv", encoding="latin-1")

print("\nColumns in dataset:", list(df.columns))

# Assume first column = label, last column = message
label_col = df.columns[0]
text_col = df.columns[-1]

print("Using label column:", label_col)
print("Using text column:", text_col)

df = df[[label_col, text_col]]
df.columns = ['label', 'text']

# convert labels to 0 and 1 automatically
df['label'] = df['label'].astype(str).str.lower()
df['label'] = df['label'].apply(lambda x: 1 if 'spam' in x else 0)

df['text'] = df['text'].apply(clean_text)

print("\nTraining model...")

X_train, X_test, y_train, y_test = train_test_split(
    df['text'], df['label'], test_size=0.2, random_state=42
)

model = Pipeline([
    ('vectorizer', TfidfVectorizer()),
    ('classifier', MultinomialNB())
])

model.fit(X_train, y_train)

pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, pred))

joblib.dump(model, "spam_model.pkl")

print("\nModel saved successfully as spam_model.pkl")
