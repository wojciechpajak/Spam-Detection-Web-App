from pathlib import Path
from joblib import load
import re
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
from pathlib import Path
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
import shap


class Classification:
    def __init__(self, input, model_name):
        # Pre-processing
        self.stopword = stopwords.words('english')
        self.email_stopword = self.load_email_stopword()
        self.wnl = WordNetLemmatizer()

        # Klasyfikator/model
        self.SRC_DIR=Path('./data/models/')
        self.input = input
        self.X_batch = self.preprocess(input)
        self.model_name = model_name
        self.vectorizer = self.load_vectorizer()
        self.model = self.load_model()
        self.X = self.vectorize()

        # XAI
        self.masker = shap.maskers.Text(tokenizer=r"\W+")
        self.explainer = shap.Explainer(self.f, self.masker)
        self.shap_values = self.explain_model()


    def load_email_stopword(self):
        email_stopword = self.stopword.copy()
        email_stopword.remove("re")
        return email_stopword
    
    def get_pos(self, tag):
        if tag.startswith('J'):
            return wordnet.ADJ
        elif tag.startswith('V'):
            return wordnet.VERB
        elif tag.startswith('N'):
            return wordnet.NOUN
        elif tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN
        
    def preprocess(self, input):
        # Pre-processing tekstu tak samo jak pre-processing zbioru danych treningowych modelu - jednolitość ocenianych danych
        # Zmiana tekstu na tokeny, rozdzielanie liczb od znaków
        X_batch = []
        text = input[0]
        text = re.sub(r'(\d+)', r' \1 ', text)
        tokens = word_tokenize(text)
        new_tokens = []
        num_tag = 'NUMBER'

        # Zmiana numerów na NUMBER, zmiana tekstu na małe litery, usunięcie stopwords (bez 're')
        for token in tokens:
            if token.isdigit():
                new_tokens.append('NUMBER')
            elif token.lower() not in self.email_stopword and token is not num_tag:
                token = token.lower()
                new_tokens.append(token)

        # Lemantyzacja
        pos_tags = nltk.pos_tag(new_tokens)
        lemma_tokens = []
        for token, pos_tag in pos_tags:
            pos_tag = self.get_pos(pos_tag)
            lemma_token = self.wnl.lemmatize(token, pos=pos_tag)
            lemma_tokens.append(lemma_token)
        
        # Detokenizacja fn. join
        text = ' '.join(lemma_tokens)
        X_batch.append(text)
        print(text)
        return X_batch
    

    def load_vectorizer(self):
        vectorizer = load(f'{self.SRC_DIR}/TFIDF_Vectorizer_MaxFeatures1000.joblib')
        print(f'Załadowano TF-IDF vectorizer.')
        return vectorizer
    
    def load_model(self):
        model = load(f'{self.SRC_DIR}/{self.model_name}.joblib')
        print(f'Załadowano model {self.model_name}.')
        return model


    def vectorize(self):
        X = self.vectorizer.transform(self.X_batch)
        return X

    ####################################
    def get_preds(self):
        preds = self.model.predict(self.X)
        return preds
    
    def get_preds_proba(self):
        preds_proba = self.model.predict_proba(self.X)
        return preds_proba
    
    def get_class_prediction(self):
        prediction = self.get_preds()[0]
        return prediction
    
    def get_ham_prediction(self):
        prediction = self.get_preds_proba()[0][0]
        prediction = round(prediction*100, 2)
        print(prediction)
        return prediction
    
    def get_spam_prediction(self):
        prediction = self.get_preds_proba()[0][1]
        prediction = round(prediction*100, 2)
        print(prediction)
        return prediction


    def f(self, inputs):
        X = self.vectorizer.transform(inputs).toarray()
        preds = self.model.predict(X)
        return preds
    
    def explain_model(self):
        shap_values = self.explainer(self.X_batch)
        return shap_values

    def text_plot(self):
        shap_plot = shap.plots.text(self.shap_values, display=False)
        return shap_plot
    