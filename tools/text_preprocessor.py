import re

from nltk.corpus import stopwords

regex = r"[а-яА-Я()]+"

pattern = re.compile(regex)

stopwords = set(stopwords.words('russian'))


def _lemmatize(doc: str) -> list[str] | None:
    doc = re.sub(pattern, ' ', doc)
    tokens = []
    for token in doc.split():
        if token and token not in stopwords:
            token = token.strip()
            tokens.append(token)
    if len(tokens) > 0:
        return tokens
    return None


def comment_tokens(comment: str) -> list:
    links_clear = _clear_link_tokens(comment)
    left_substring = comment
    tokens = []
    if links_clear:
        for link in links_clear:
            index = left_substring.find(link)
            tokens.append((left_substring[:index], 0))
            tokens.append((link, 1))
            left_substring = left_substring[index + len(link):]
        return tokens
    return [(comment, 0)]


def _clear_link_tokens(text: str) -> list | None:
    http_string = 'http'
    comment = _insert_substring_before_all(text, http_string, ' ')
    links = _lemmatize(comment)
    if links:
        return [link for link in links if http_string in link]
    return None


def _insert_substring_before(text: str, search_substring: str, insert_substring: str) -> str:
    index = text.find(search_substring)
    if index != -1:
        text = text[:index] + insert_substring + text[index:]
    return text


def _insert_substring_after(text: str, search_substring: str, insert_substring: str) -> str:
    index = text.find(search_substring) + len(search_substring)
    if index != -1:
        text = text[:index] + insert_substring + text[index:]
    return text


def _insert_substring_before_all(text: str, search_substring: str, insert_substring: str) -> str:
    return text.replace(search_substring, insert_substring + search_substring)
