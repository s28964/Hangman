import random
from database import session
from models import Word
from sqlalchemy import func


lives = 7


def choose_word_with_same_length(length):
    possible_words = session.query(Word).filter(func.length(Word.value) == length).all()
    if not possible_words:
        raise ValueError("Lack of words in database of that length")
    return random.choice(possible_words).value.upper()

def get_word_of_equal_length():
    words = session.query(Word).all()
    if not words:
        raise ValueError("Lack of words in database")
    first_word = random.choice(words).value.upper()
    length = len(first_word)
    second_word = choose_word_with_same_length(length)
    return first_word, second_word

def get_two_words_from_category(category: str):
    words = session.query(Word).filter(Word.category == category.upper()).order_by(func.random()).limit(2).all()
    if len(words) < 2:
        raise ValueError("Lack of words in database of that category")
    return words[0].value.upper(), words[1].value.upper()



def get_two_random_words():
    words = session.query(Word).order_by(func.random()).limit(2).all()
    if len(words) < 2:
        raise ValueError("There must be at least 2 words in database")
    return words[0].value.upper(), words[1].value.upper()