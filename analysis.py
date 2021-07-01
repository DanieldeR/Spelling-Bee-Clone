#%%
import pandas as pd
from random import sample, choice
import numpy as np 

# %%

def clean():
    word_list = pd.read_csv('resources/english3.txt', sep='\n', header=None)
    frequency = pd.read_csv('resources/unigram_freq.csv')

    word_list.columns = ['words']

    df = pd.merge(word_list, frequency, how='left', left_on='words', right_on='word')
    df = df.dropna()

    df = df.sort_values(by='count', ascending=0)

    cleaned = df['word']

    cleaned = cleaned[cleaned.map(lambda x: len(list(x)) >= 4)]
    cleaned = cleaned.reset_index(drop=True)

    return cleaned


# %%
def get_letters(v:int = 3):
    c = 7 - v
    consonants = list('bcdfghjklmnpqrstvwxyz')
    vowels = list('aeiou')

    return (list(sample(consonants, k=c)) + list(sample(vowels, k=v)))
# %%

def get_word_list(cleaned):
    found = False
    
    while not found:
        # Get all bunch of random letters
        raw_letters = get_letters()

        # Choose a random letter as the mandatory letter
        letter = choice(raw_letters)

        # Code the letters as a set so that they can be used easier
        letters = set(raw_letters)

        print(letters)

        # Subtract the words from the main list that do not contain the mandatory letter
        mandatory_cleaned = cleaned[cleaned.map(lambda x: letter in x)]

        # Make sure all of the letters can be matched
        words_to_spell = mandatory_cleaned[mandatory_cleaned.apply(lambda x: set(x).issubset(letters))]
        
        if len(words_to_spell[words_to_spell.map(lambda x: len(set(x).symmetric_difference(letters))==0)]) > 0:
            found = True

    return((letter, letters, words_to_spell))

#%%
def stats(letter, letters, words):
    difficulty = np.mean(list(words.index))

    return (difficulty, len(words))
# %%
if __name__ == '__main__':
    data = clean()

    letter, letters, words = get_word_list(data)

    print(letter, letters)
    print(stats(letter, letters, words))
# %%
