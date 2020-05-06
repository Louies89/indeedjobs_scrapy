import spacy
from spacy.pipeline import Sentencizer
from spacy.lang.en.stop_words import STOP_WORDS
from nltk.corpus import stopwords
from spacy.lemmatizer import Lemmatizer
from lemminflect import getLemma
from spacy.lookups import Lookups
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
import numpy
import json


nlp = spacy.load('en_core_web_sm')

STOP_WORDS.update(stopwords.words("english"))
for word in STOP_WORDS:
    lexeme = nlp.vocab[word]
    lexeme.is_stop = True



text = "Responsibilities include working on research and development on core\nblockchain technologies, algorithms, data structures, NoSQL, cryptography,\nnetwork security, and scalable robust architectures.\n\n **Our criteria:**\n\n1\\. Strong engineering background, from a reputed university with\nbachelors/masters/doctorate degree in computer science or mathematics\n\n2\\. Maverick programmer, with a mindset to embrace open source technology\nstacks.\n\n3\\. A good team player\n\n4\\. Ability to thrive in a fast-changing environment with dynamic objectives\n\n5\\. Emotional intelligence and the consideration of your teammates\n\n6\\. Reflection and continuous self-improvement\n\n7\\. Adaptive, willing to learn, teach, lead, and follow\n\n8\\. Not afraid of long hours when necessary\n\n9\\. Able to handle stress well and maintain a positive attitude\n\n **Skills:**\n\n1\\. Fluent in functional programming language/s - Hakskell / Scala / Clojure /\nElixir / other..\n\n2\\. Adept on Linux and other open-source technologies/platforms\n\n3\\. Not the slightest averse to learning & mastering new programming\nlanguages/ concepts\n\n4\\. Interest in mathematics, code elegance & cryptographic primitives /\nlibraries\n\n5\\. Experience analyzing data structures and algorithms\n\n6\\. Experience with advanced concepts of functional programming\n\n7\\. Ability to analyze security on large scale systems, designing, working\nwith, and scaling distributed systems\n\n8\\. Knowledge of troubleshooting, concurrency, synchronization, common IPC/RPC\nmethods and patterns, messaging systems & patterns, solid OS/networking\nfundamentals\n\nJob Type: Full-time\n\nExperience:\n\n  * advanced concepts of functional programming: 1 year (Preferred)\n  * analyze security on large scale systems, designing, working: 1 year (Preferred)\n  * Linux and other open-source technologies/platforms: 1 year (Preferred)\n  * analyzing data structures and algorithms: 1 year (Preferred)\n  * Functional programming language/s - Hakskell / Scala / Cloju: 1 year (Preferred)\n\nEducation:\n\n  * Bachelor's (Preferred)\n\n"

def cleanTheText(text):
    import re
    text = text.replace('**','')
    text = text.replace('\\',' ')
    text = text.replace('/',' ')
    text = re.sub(r'http\S+', '',text)
    text = re.sub('\s+',' ',text)
    text = re.sub(r"[,.;@#?!&$\(\)<>\[\]]+\ *", " ", text)
    return text


def sentencize(text):
    if not nlp.has_pipe("sentencizer"):
        sentencizer = Sentencizer(punct_chars=[".", "?", "!", "。", "\n\n", "\n"])
        nlp.add_pipe(sentencizer,name="sentencizer")
    doc = nlp(cleanTheText(text))   
    return [str(sentence).lower() for sentence in doc.sents]

# Create token list after removing stop words
def tokenize(sentence):
    # Pare text by spaCy
    lookups = Lookups()
    lookups.add_table("lemma_rules", {"noun": [["ies","y"],["ses","s"],["xes","x"],["zes","z"],["ches","ch"],["shes","sh"],["s","s"],["men","man"]]})
    token_list = []
    for token in nlp(sentence):
        if (token.is_stop == False and 
            not (token.is_punct or           #Remove punctuations like ?:!.,; etc..
            token.is_space or                #Remove spaces
            token.like_num or                #Remove numbers
            token.is_stop) and               #Remove stop words
            len(token.text)>2):              #Remove shorter words
            # token_list.append(lemmatizer(token.text,'NOUN')[0])
            lemma = getLemma(token.text,upos='NOUN')
            if lemma == token.text:
                token_list.append(getLemma(token.text,upos='VERB')[0])
            else:
                token_list.append(getLemma(token.text,upos='NOUN')[0])
    return token_list



tfDict = {}
def computeTF(text):
    global tfDict
    for sentence in sentencize(text):
        token_list = tokenize(sentence)
        for word in token_list:
            if word in tfDict:
                tfDict[word] += 1
            else:
                tfDict[word] = 1



with open('output.json', 'r') as f:
    jobs = json.load(f)

    for job in jobs:
        computeTF(job['job_description'])

    # print(tfDict)

    dictOut = {}
    for key, value in tfDict.items():
        if value in dictOut:
            if not key in dictOut[value]:
                dictOut[value].append(key)
        else:
            dictOut[value] = [key]

    print(dict(sorted(dictOut.items())))



# with open('output.json', 'r') as f:
#     jobs = json.load(f)

#     jobDescriptions = []
#     for job in jobs:
#         jobDescriptions.append(job['job_description']) 

#     bow_vector = CountVectorizer(tokenizer = tokenize, ngram_range=(1,1))
#     X = bow_vector.fit_transform(jobDescriptions)
#     feature_names = bow_vector.get_feature_names()

#     dictOut = {}
#     for col in X.nonzero()[1]:
#         dictOut[feature_names[col]] = X[0, col]

#     print(dictOut)

        



# token_list = tokenize(text)
# print(token_list, len(token_list))

# bow_vector = CountVectorizer(tokenizer = tokenize, ngram_range=(1,1))
# X = bow_vector.fit_transform(sentencize(text))
# print(bow_vector.get_feature_names(),len(bow_vector.get_feature_names()))
# print(X.toarray())



# numpy.savetxt(r'.\nlp\bow_vector.txt', X.toarray(), delimiter=', ')

# tfidf_vector = TfidfVectorizer(tokenizer = tokenize,ngram_range=(1,1))
# Y = tfidf_vector.fit_transform(sentencize(text))
# # print(tfidf_vector.get_feature_names(),len(tfidf_vector.get_feature_names()))
# # print(Y,Y.shape)
# feature_names = tfidf_vector.get_feature_names()
# for col in Y.nonzero()[1]:
#     print (feature_names[col], ' - ', Y[0, col])
