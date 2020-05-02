# pip install spacy
# pip install nltk
# nltk.download('punkt')
# nltk.download('stopwords')

import spacy
import nltk
from nltk.corpus import stopwords 
from spacy.lang.en.stop_words import STOP_WORDS

nlp = spacy.load('en_core_web_sm')

#Before reading the nlp() operation on text, add stop words from NLTK to spacy to get better set of stop words
STOP_WORDS.update(stopwords.words("english"))

text = "Responsibilities include working on research and development on core\nblockchain technologies, algorithms, data structures, NoSQL, cryptography,\nnetwork security, and scalable robust architectures.\n\n **Our criteria:**\n\n1\\. Strong engineering background, from a reputed university with\nbachelors/masters/doctorate degree in computer science or mathematics\n\n2\\. Maverick programmer, with a mindset to embrace open source technology\nstacks.\n\n3\\. A good team player\n\n4\\. Ability to thrive in a fast-changing environment with dynamic objectives\n\n5\\. Emotional intelligence and the consideration of your teammates\n\n6\\. Reflection and continuous self-improvement\n\n7\\. Adaptive, willing to learn, teach, lead, and follow\n\n8\\. Not afraid of long hours when necessary\n\n9\\. Able to handle stress well and maintain a positive attitude\n\n **Skills:**\n\n1\\. Fluent in functional programming language/s - Hakskell / Scala / Clojure /\nElixir / other..\n\n2\\. Adept on Linux and other open-source technologies/platforms\n\n3\\. Not the slightest averse to learning & mastering new programming\nlanguages/ concepts\n\n4\\. Interest in mathematics, code elegance & cryptographic primitives /\nlibraries\n\n5\\. Experience analyzing data structures and algorithms\n\n6\\. Experience with advanced concepts of functional programming\n\n7\\. Ability to analyze security on large scale systems, designing, working\nwith, and scaling distributed systems\n\n8\\. Knowledge of troubleshooting, concurrency, synchronization, common IPC/RPC\nmethods and patterns, messaging systems & patterns, solid OS/networking\nfundamentals\n\nJob Type: Full-time\n\nExperience:\n\n  * advanced concepts of functional programming: 1 year (Preferred)\n  * analyze security on large scale systems, designing, working: 1 year (Preferred)\n  * Linux and other open-source technologies/platforms: 1 year (Preferred)\n  * analyzing data structures and algorithms: 1 year (Preferred)\n  * Functional programming language/s - Hakskell / Scala / Cloju: 1 year (Preferred)\n\nEducation:\n\n  * Bachelor's (Preferred)\n\n"

# Pare text by spaCy
my_doc = nlp(text)

# Create list of word tokens
token_list = []
for token in my_doc:
    token_list.append(token.text)


# Create list of word tokens after removing stopwords
filtered_sentence =[] 

for word in token_list:
    lexeme = nlp.vocab[word]
    if lexeme.is_stop == False:
        filtered_sentence.append(word) 
print(token_list)
print(filtered_sentence)   