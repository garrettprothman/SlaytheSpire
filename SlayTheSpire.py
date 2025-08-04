import random
class Card:
    def __init__(self, name, energy_cost, damage=0, block=0):
        #Creates the cards
        self.name = name
        self.energy_cost = energy_cost
        self.damage = damage
        self.block = block

    def __str__(self):
        #Prints the stats of cards while omitting values of 0
        lines = [self.name, f"Cost: {self.energy_cost}"]
        if self.damage != 0:
            lines.append(f"Damage: {self.damage}")
        if self.block != 0:
            lines.append(f"Block: {self.block}")
        return '\n'.join(lines)
    
    def display(self):
        #When displaying cards, a newline is built in to improve readability
        print(self)
        print()

#Now, we create the cards
strike = Card("Strike", energy_cost=1, damage=6)
defend = Card("Defend", energy_cost=1, block=5)

#Create player's deck
player_deck = [strike, strike, strike, strike, strike, defend, defend, defend, defend]

#Function to display deck
def show_deck(deck):
    print("Your Deck:")
    for i, card in enumerate(deck, start=1):
        print(f"{i}. {card}")
        print()


#Making the player
class Player:
    def __init__(self, max_health=80, max_energy=3):
        self.max_health = max_health



#Manipulating deck

hand = []
discard_pile = []
draw_pile = []
cards_to_draw = 5

#We shuffle the deck
random.shuffle(player_deck)

#Drawing Cards
def draw_cards(draw_pile, hand, num):
    for i in range(num):
        if not draw_pile:
            draw_pile.extend(discard_pile)
            discard_pile.clear()
            random.shuffle(draw_pile)
            if not draw_pile:
                print("No cards left to draw!")
                break
        hand.append(draw_pile.pop())

draw_cards(player_deck, hand, cards_to_draw)

#Discarding cards
def discard_card(card, hand, discard_pile):
    if card in hand:
        discard_pile.append(card)
        hand.remove(card)
    else:
        print("Card not in hand!")

#Discarding hand
def discard_hand(hand, discard_pile):
    while hand:
        discard_card(hand[0], hand, discard_pile)



#Playing Cards
player_energy = 3
enemy_health = 50
player_block = 0

def play_card(card, hand, discard_pile, player_stats, enemy_stats):
    global player_energy

    if card.energy_cost > player_energy:
        print("Not enough energy!")

    player_energy -= card.energy_cost
    print(f"Playing {card.name}! Energy left: {player_energy}")

    if card.damage > 0:
        enemy_stats['health'] -= card.damage
        print(f"Dealt {card.damage} damage to enemy! Enemy health: {enemy_stats['health']}")
    
    if card.block > 0:
        player_stats['block'] += card.block
        print(f"Gained {card.block} block! Player block: {player_stats['block']}")
    if card in hand:
        hand.remove(card)
        discard_pile.append(card)
    else:
        print("Card not found in hand!")



"""print(f"Drawing {cards_to_draw} cards:")
for card in hand:
    print(card)
    print()"""