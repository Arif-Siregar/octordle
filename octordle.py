import random
from collections import Counter, defaultdict
from itertools import product
import math
import pandas as pd

GREEN = "g"
YELLOW = "y"
BLACK = "b"

f = open("words.txt", "r")
WORDS = f.read().split()

class State:
  def __init__(self):
    self.guess = None
    self.hint = None
    self.attempt = 0
    self.choices = WORDS
    
##############################################################################################

def word_dict(word):
  temp = dict()
  for i in range(len(word)):
    if word[i] not in temp:
      temp[word[i]] = [1, [i]]
    else:
      temp[word[i]][0] += 1
      temp[word[i]][1].append(i)
  return temp

def colours(word, temp):
  word_count = word_dict(word)
  temp_count = word_dict(temp)
  temp = [-1, -1, -1, -1, -1]

  for char in temp_count.keys():
    if char not in word_count.keys():
      for index in temp_count[char][1]:
        temp[index] = BLACK
    else:
      remove = []
      for index in temp_count[char][1]:
        if index in word_count[char][1]:
          temp[index] = GREEN
          word_count[char][0] -= 1
          temp_count[char][0] -= 1
          remove.append(index)

      for item in remove:
        word_count[char][1].remove(item)
        temp_count[char][1].remove(item)

      for index in temp_count[char][1]:
        if word_count[char][0] > 0:
          temp[index] = YELLOW
          word_count[char][0] -= 1
        else:
          temp[index] = BLACK

  return temp

def classification(word, word_list):
  pattern = defaultdict(list)
  for answer in word_list:
    pattern["".join(colours(answer, word))].append(answer)
  return pattern

def best_entropy(words):
  information = defaultdict(int)

  for guess in words:
    pattern = defaultdict(int)
    for answer in words:
      pattern["".join(colours(answer, guess))] += 1
    for pat in pattern:
      information[guess] += (-1 * (pattern[pat]/len(words)) * math.log((pattern[pat]/len(words)), 2))

  return sorted(information, key=lambda x: information[x], reverse = True)[0]
