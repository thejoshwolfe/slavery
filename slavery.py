#!/usr/bin/env python

import random

KING = 3
NOBLE = 2
PEASANT = 1
SPY = 0

class Player:
  def __init__(self, name):
    self.name = name
    self.hide_hand = False
    self.hide_deck = False
    self.big_points = 0
    self.new_game()
  def new_game(self):
    self.deck = [PEASANT]*5 + [NOBLE]*3 + [KING] + [SPY]
    random.shuffle(self.deck)
    self.hand = []
    for _ in range(5):
      self.draw()
    self.score = 0
    self.active_card = None
    self.master = None
    self.slaves = []
  def draw(self):
    if len(self.deck) == 0:
      return
    self.hand.append(extract(self.deck, 0))
    self.hand.sort()
  def play(self, index):
    self.active_card = extract(self.hand, index)
  def capture(self, other_player):
    self.score += 1
    other_player.active_card = None
  def bow_out(self):
    self.capture(self)
  def enslave(self, other_player):
    other_player.master = self
    self.slaves.append(other_player)
    # steal slaves
    for slave in other_player.slaves[:]:
      slave.freedom()
      self.enslave(slave)
  def freedom(self):
    self.master.slaves.remove(self)
    self.master = None
  def __repr__(self):
    result = self.name + " [" + repr(self.big_points) + "," + repr(self.score) + "]"
    result += ": (" + repr(self.active_card) + ")"
    result += " " + " ".join(self.reveal_hand(x) for x in self.hand)
    result += " [" + " ".join(self.reveal_deck(x) for x in self.deck) + "]"
    if self.master != None:
      result += " :("
    if len(self.slaves) > 0:
      result += " :> " + ", ".join(slave.name for slave in self.slaves)
    return result
  def reveal_hand(self, card):
    if self.hide_hand: return "?"
    return repr(card)
  def reveal_deck(self, card):
    if self.hide_deck: return "?"
    return repr(card)

def extract(arr, index):
  item = arr[index]
  del arr[index]
  return item

def what():
  for player in players:
    print(player)

def compare(card, other_card):
  if card == other_card:
    return 0
  reverser = 1
  if card > other_card:
    card, other_card = other_card, card
    reverser = -1
  if (card, other_card) == (SPY, PEASANT):
    return 0
  if (card, other_card) == (SPY, KING):
    return reverser
  if card < other_card:
    return -reverser
  return reverser

def resolve():
  for slave in players:
    if slave.master == None: continue
    if compare(slave.active_card, slave.master.active_card) > 0:
      # break free
      slave.freedom()
    else:
      # sorry sucka
      slave.master.capture(slave)

  spies = players_with(0)
  if len(spies) == 1:
    [spy] = spies
    # kill kings
    kings = players_with(3)
    if len(kings) > 0:
      # success
      for king in kings:
        spy.capture(king)
      spy.bow_out()
    # otherwise, they're just peasants

  kings = players_with(3)
  if len(kings) >= 2:
    # cancel kings
    for king in kings:
      king.bow_out()
  elif len(kings) == 1:
    [king] = kings
    for noble in players_with(2):
      king.capture(noble)
    for peasant in players_with(0, 1):
      king.capture(peasant)
      king.enslave(peasant)
    king.bow_out()

  nobles = players_with(2)
  if len(nobles) >= 2:
    # cancel nobles
    for noble in nobles:
      noble.bow_out()
  elif len(nobles) == 1:
    [noble] = nobles
    for peasant in players_with(0, 1):
      noble.capture(peasant)
    noble.bow_out()

  for peasant in players_with(0, 1):
    peasant.bow_out()

  # all should be done
  if len(players_with(0, 1, 2, 3)) != 0:
    raise everything

def players_with(*cards):
  return [player for player in players if player.active_card in cards]

def play_random(player):
    player.play(random.randint(0, len(player.hand) - 1))

def all_random():
  for player in players:
    play_random(player)
  resolve()
  all_draw()
def all_draw():
  for player in players:
    player.draw()

def score_big():
  for me in players:
    for you in players:
      if me == you: continue
      if me.score >= you.score:
        me.big_points += 1
      if you.master == me:
        me.big_points += 1

try:    player_count = input("players?\n[4] >>> ")
except: player_count = 4
players = [Player(chr(ord("A") + i)) for i in range(player_count)]

def simulation():
  for _ in range(10):
    all_random()
  what()

def interactive():
  for player in players:
    player.hide_deck = True
    player.hide_hand = True
  players[0].hide_hand = False
  for _ in range(5):
    for _ in range(10):
      what()
      for player in players:
        if player != players[0]:
          play_random(player)
      choices = sorted(set(players[0].hand))
      while True:
        choice = raw_input("[" + ",".join(repr(x) for x in choices) + "] >>> ")
        try:
          choice_value = int(choice)
          index = players[0].hand.index(choice_value)
          players[0].play(index)
        except ValueError:
          print("wat")
        else:
          break
      what()
      raw_input("[] >>> ")
      resolve()
      all_draw()
    what()
    raw_input("[] >>> ")
    score_big()
    for player in players:
      player.new_game()
  what()
interactive()
