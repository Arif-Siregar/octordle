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

"""
Given a word, break down the word into a count of the total number of each alphabets and their indices.
For example: word_dict("SERAI") -> {'S': [1, [0]], 'E': [1, [1]], 'R': [1, [2]], 'A': [1, [3]], 'I': [1, [4]]}
"""
def word_dict(word):
  temp = dict()
  for i in range(len(word)):
    if word[i] not in temp:
      temp[word[i]] = [1, [i]]
    else:
      temp[word[i]][0] += 1
      temp[word[i]][1].append(i)
  return temp

"""
Given an answer, word, and a guess, temp, provide the hint that will be produced.
For example: colours("SERAI", "EAGER") -> ['y', 'y', 'b', 'b', 'y']
"""
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

"""

"""
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

def best_entropy_trial(word_choices):
  information = defaultdict(int)

  for words in word_choices:
    for guess in words:
      pattern = defaultdict(int)
      for answer in words:
        pattern["".join(colours(answer, guess))] += 1
      for pat in pattern:
        information[guess] += (-1 * (pattern[pat]/len(words)) * math.log((pattern[pat]/len(words)), 2))

  return sorted(information, key=lambda x: information[x], reverse = True)[0]

def matches(word, pattern, temp):
  word_count = word_dict(word)
  temp_count = word_dict(temp)

  for char in word_count.keys():
    for index in word_count[char][1]:
      match pattern[index]:
        case 'b':
          word_count[char][0] -= 1
          if temp[index] == word[index]:
            return False
        case 'y':
          if temp[index] == word[index]:
            return False
        case 'g':
          if temp[index] != word[index]:
            return False

  for char in word_count.keys():
    if char in temp_count.keys():
      if len(word_count[char][1]) != word_count[char][0]:
        if word_count[char][0] != temp_count[char][0]:
          return False
      else:
        if word_count[char][0] > temp_count[char][0]:
          return False
    else:
      if word_count[char][0] != 0:
        return False

  return True

def guess_machine(state):
  immediate = None

  if state.attempt == 0:
    return "TARES"

  elif state.attempt == 1:
    pattern = classification(state.guess, state.choices)
    state.choices = []

    for hint in state.hint:
      if hint:
        pat = "".join(hint)
        state.choices.append(pattern[pat])

        if len(pattern[pat]) == 1:
          immediate = pattern[pat][0]
      else:
        state.choices.append([])

  else:
    temp_choices = []
    for i in range(len(state.choices)):
      if state.hint[i]:
        temp = []
        for word in state.choices[i]:
          if matches(state.guess, state.hint[i], word):
            temp.append(word)
        temp_choices.append(temp)

        if len(temp) == 1:
          immediate = temp[0]
      else:
        temp_choices.append([])
    state.choices = temp_choices

  if immediate:
    return immediate

  else:
    #all_choices = []
    #for choices in state.choices:
      #for word in choices:
        #if word not in all_choices:
          #all_choices.append(word)
    answer = best_entropy_trial(state.choices)
    return answer

def game():
  true_list = [GREEN for i in range(5)]
  answer = random.sample(WORDS, 8)
  answer_correct = [False for ans in answer]
  state = State()

  for i in range(13):
    guess = guess_machine(state)
    # print(f"Enter a guess: {guess}")

    # while guess not in WORDS:
      # print("Word does not exist, try again!")
      # guess = guess_machine(state)
      # print(f"Enter a guess: {guess}")

    # reply = ""
    state.guess = guess
    state.hint = []
    state.attempt += 1

    for j in range(len(answer)):
      if not answer_correct[j]:
        temp = colours(answer[j], guess)
        # for k in range(len(temp)):
          # reply += guess[k] + " " + temp[k] + " "
        # reply += "| "

        if temp == true_list:
          answer_correct[j] = True
          state.hint.append([])
        else:
          state.hint.append(temp)

      else:
        state.hint.append([])
        # reply += 20 * " " + "| "

    # print(reply)
    if sum(answer_correct) == 8:
      return 13 - state.attempt
      # print("You won!!!")
      break

  if sum(answer_correct) != 8:
    return (sum(answer_correct) - 8)
    # print(f"You lose!!! You only got {sum(answer_correct)}")
