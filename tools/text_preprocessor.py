import re

from nltk.corpus import stopwords

from pymorphy2 import MorphAnalyzer


# morph = MorphAnalyzer()

regex = r"[!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"

# regex = r"[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"

pattern = re.compile(regex)

sub = {'.', ',', '!', '?', '``', '...'
    , '\'\'', '<', '>', '}', '{', '*'
    , ')', '(', '..', '\'re', 'op.utmn.ru'
    , ';', '—', '+', '=', '&', '|', '||'
    , ':', '’', '....', '-', '%', '_'
    , '[', ']', '', '–', '~', '^'
    , 'Рис', 'см', '»', '«', '++', 'ᡃ'
    , 'п', 'о', 'для', 'и', 'в', 'над'
    , '@', 'г', 'в', 'й', 'о', '№', 'м'
    , 'и', 'а', 'у', 'ю', 'с', 'н'}

stopwords = set(stopwords.words('russian'))

stopwords = stopwords.union(sub)


def lemmatize(doc):
    doc = re.sub(pattern, ' ', doc)
    tokens = []
    for token in doc.split():
        if token and token not in stopwords:
            token = token.strip()
            # token = morph.normal_forms(token)[0]
            tokens.append(token)
    if len(tokens) > 0:
        return tokens
    return None
