"""Given a selection of 9 letters consisting of vowel and consonants, find the longest word using only these letters. 3 rounds per game."""

import itertools
import random
import time

word_dictionary_filename = "word_dictionary.txt"
letter_frequency_filename = "letter_frequency.txt"
word_dictionary = set()
vowels = []
consonants = []
min_vowel_count = 2
min_consonant_count = 3
max_letter_count = 9


def request_letters():
  """get selection of letters from the player. Player can only select a vowel or consonant, at random."""
  letters = []
  vowel_count = 0
  consonant_count = 0
  for _ in range(max_letter_count):
    print("Current Letters:   ", " ".join(letters))
    next_choice = " "
    if (vowel_count < min_vowel_count
        and len(letters) + min_vowel_count >= max_letter_count):
      print("Choosing a random Vowel...")
      next_choice = "V"
    elif (consonant_count < min_consonant_count
          and len(letters) + min_consonant_count >= max_letter_count):
      print("Choosing a random Consonant...")
      next_choice = "C"
    while not (next_choice == "V" or next_choice == "C"):
      next_choice = input("Choose a Vowel (V) or Consonant (C)? ")
      next_choice = next_choice.upper()
    if next_choice == "V":
      next_letter = random.choice(vowels)
      vowels.remove(next_letter)
      vowel_count += 1
    else:
      next_letter = random.choice(consonants)
      consonants.remove(next_letter)
      consonant_count += 1
    letters.append(next_letter)
  return letters


def prepare_dictionary():
  """prepares the global word_dictionary list"""
  global word_dictionary
  with open(word_dictionary_filename) as f:
    word_dictionary = set(f.read().upper().split("\n"))


def prepare_letter_choices():
  """create list of possible letter choices"""
  frequencies = {}
  global vowels, consonants
  with open(letter_frequency_filename) as f:
    data = f.read().split("\n")
  for line in data:
    letter, freq = line.split()
    frequencies[letter] = int(float(freq) / 20)
    if frequencies[letter] < 1:
      frequencies[letter] = 1
  while frequencies:
    letter = random.choice(list(frequencies.keys()))
    if letter in "AEIOU":
      vowels.append(letter)
    else:
      consonants.append(letter)
    frequencies[letter] -= 1
    if frequencies[letter] == 0:
      frequencies.pop(letter)


def find_words(letters):
  """find words given a list of letters"""
  global word_dictionary
  permutats = set()
  for i in range(2, 10):
    new_permutats = {"".join(p) for p in itertools.permutations(letters, i)}
    permutats = permutats.union(new_permutats)
  words = permutats.intersection(word_dictionary)
  return words


def find_longest_words(words):
  """find the longest words given a set of words"""
  words = list(words)
  words.sort(key=len)
  max_length = len(words[-1])
  longest_words = [w for w in words if len(w) == max_length]
  return longest_words


def main():
  """script entry point"""
  score = 0
  prepare_dictionary()
  prepare_letter_choices()
  print("COUNTDOWN - FIND THE LONGEST WORD")
  print("---------------------------------")
  print("Instructions:")
  print("Choose 9 random letters")
  print("You can only choose between a Vowel or a Consonant")
  print("Must choose at least 3 consonants and 2 vowels")
  print()
  print("When 9 letters are chosen, you will have 60 seconds to find")
  print("\tthe longest word possible using only those letters")
  print()
  print("The game has three rounds")
  print()
  print("There are a limited amount of letters available")
  print("Letters used in one round are not used in the following rounds")

  try:
    for round_number in range(1, 4):
      print()
      print("----------------------------------")
      print("*** ROUND", round_number, " ***")
      print()
      letters = request_letters()
      print("----------------------------------")
      print("Your letters are:\t\t", " ".join(letters))
      print("----------------------------------")
      words = find_words(letters)
      longest_words = find_longest_words(words)
      print("You have 60 SECONDS to find the longest word")
      time.sleep(0.25)
      print("Starting...")
      time.sleep(0.75)
      print("NOW!!")
      for _ in range(57):
        time.sleep(1)
      for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)

      print("TIME IS UP")
      print("----------------------------------")
      print("What was the longest word you could find?")
      player_word = input("Your word: ")
      player_word = player_word.upper()
      if player_word not in words:
        print("I do not recognise that word!")
        print("0 points")
      else:
        points = len(player_word)
        print(points, "points!")
        score += points
      print("The longest words are:  ", ", ".join(longest_words))
      print()
      if round_number < 3:
        print("Your score so far: ", score)
      else:
        print("Your Final Score:   ", score)
  except KeyboardInterrupt:
    print("\nQuitting Game...")


if __name__ == "__main__":
  main()
