import random
# Card Class
class Card:
    def __init__(self, name, energy_cost, damage=0, block=0, effects=None):
        self.name = name
        self.energy_cost = energy_cost
        self.damage = damage
        self.block = block
        self.effects = effects if effects else {}  # e.g., {"Vulnerable": 2}

    def __str__(self):
        #Card Description
        lines = [self.name, f"Cost: {self.energy_cost}"]
        if self.damage:
            lines.append(f"Damage: {self.damage}")
        if self.block:
            lines.append(f"Block: {self.block}")
        for effect, duration in self.effects.items():
            lines.append(f"Applies {effect} ({duration} turn{'s' if duration > 1 else ''})")
        return '\n'.join(lines)

    def display(self):
        #When displaying, adds a newline to prevent cards clustering together
        print(self)
        print()


# Enemy Class
class Enemy:
    def __init__(self, name, base_health, moves, floor=1):
        self.name = name
        self.max_health = int(base_health + floor * 2)
        self.health = self.max_health
        self.block = 0
        self.debuffs = {"Weak": 0, "Vulnerable": 0}
        self.moves = moves
        self.intent = random.choice(self.moves)

    def take_damage(self, amount):
        if self.debuffs["Vulnerable"] > 0:
            amount = int(amount * 1.5)
            print(f"{self.name} is Vulnerable! Damage increased to {amount}.")
        damage = max(amount - self.block, 0)
        self.block = max(self.block - amount, 0)
        self.health -= damage
        print(f"{self.name} took {damage} damage! Remaining HP: {self.health}/{self.max_health}")

    def choose_intent(self):
        self.intent = random.choice(self.moves)

    def show_intent(self):
        print(f"{self.name} intends to {self.intent['type']} for {self.intent.get('amount', 0)}")

    def attack(self, player):
        if self.intent["type"] == "attack":
            actual_damage = self.intent["amount"]
            if self.debuffs["Weak"] > 0:
                actual_damage = int(actual_damage * 0.75)
                print(f"{self.name} is Weak! Damage reduced to {actual_damage}.")
            print(f"{self.name} attacks for {actual_damage} damage!")
            player.take_damage(actual_damage)
        elif self.intent["type"] == "block":
            self.block += self.intent["amount"]
            print(f"{self.name} gains {self.intent['amount']} block! Total block: {self.block}")

    def is_dead(self):
        return self.health <= 0

    def __str__(self):
        return f"{self.name} - HP: {self.health}/{self.max_health}"





# Enemy Generation
enemy_templates = {
    "Slime": {"base_health": 30,"moves": [{"type": "attack", "amount": 5},{"type": "attack", "amount": 8},{"type": "block", "amount": 5}]},
    "Jaw Worm": {"base_health": 40,"moves": [{"type": "attack", "amount": 6},{"type": "block", "amount": 6}]},
    "Cultist": {"base_health": 35,"moves": [{"type": "attack", "amount": 7},{"type": "attack", "amount": 10}]}
}

def generate_enemy(name, floor=1):
    template = enemy_templates.get(name)
    return Enemy(name, template["base_health"], template["moves"], floor)

def random_enemy(floor=1):
    name = random.choice(list(enemy_templates.keys()))
    return generate_enemy(name, floor)



# Player Class
class Player:
    def __init__(self, name="Ironclad", max_health=80, max_energy=3):
        self.name = name
        self.max_health = max_health
        self.current_health = max_health
        self.max_energy = max_energy
        self.energy = max_energy
        self.block = 0

        self.deck = []
        self.hand = []
        self.discard_pile = []
        self.draw_pile = []

        self.debuffs = {"Weak": 0, "Vulnerable": 0}

    def start_turn(self, cards_to_draw=5):
        print(f"\n--- {self.name}'s Turn ---")
        self.energy = self.max_energy
        self.block = 0
        for debuff in self.debuffs:
            if self.debuffs[debuff] > 0:
                self.debuffs[debuff] -= 1
                print(f"{self.name}'s {debuff} wears off, remaining: {self.debuffs[debuff]}")
        self.draw_cards(cards_to_draw)

    def draw_cards(self, num):
        for _ in range(num):
            if not self.draw_pile:
                self.shuffle_discard_into_draw()
            if not self.draw_pile:
                print("No cards left to draw!")
                break
            self.hand.append(self.draw_pile.pop())

    def shuffle_discard_into_draw(self):
        self.draw_pile = self.discard_pile[:]
        random.shuffle(self.draw_pile)
        self.discard_pile.clear()
        print("Shuffled discard pile into draw pile.")

    def play_card(self, card_index, enemy):
        if card_index < 0 or card_index >= len(self.hand):
            print("Invalid card index!")
            return

        #Handling insufficient energy
        card = self.hand[card_index]
        if card.energy_cost > self.energy:
            print(f"Not enough energy to play {card.name}.")
            return

        self.energy -= card.energy_cost
        print(f"\nPlaying {card.name}! Energy left: {self.energy}")

        if card.damage > 0:
            enemy.take_damage(card.damage)

        if card.block > 0:
            self.block += card.block
            print(f"Gained {card.block} block! Player block {self.block}")

        for effect, duration in card.effects.items():
            if effect in enemy.debuffs:
                enemy.debuffs[effect] += duration
                print(f"{enemy.name} is affected by {effect} for {duration} turn(s)!")

        self.hand.pop(card_index)
        self.discard_pile.append(card)

    def take_damage(self, amount):
        if self.debuffs["Vulnerable"] > 0:
            amount = int(amount * 1.5)
            print(f"{self.name} is Vulnerable! Damage increased to {amount}.")
        damage = max(amount - self.block, 0)
        self.block = max(self.block - amount, 0)
        self.current_health -= damage
        print(f"{self.name} took {damage} damage! HP: {self.current_health}/{self.max_health}")

    def is_dead(self):
        return self.current_health <= 0

# Game Setup
strike = Card("Strike", energy_cost=1, damage=6)
defend = Card("Defend", energy_cost=1, block=5)
bash = Card("Bash", energy_cost=2, damage=8, effects={"Vulnerable": 2})
cripple = Card("Crippling Blow", energy_cost=1, damage=4, effects={"Weak": 2})

player = Player()
player.deck = (
    [Card("Strike", 1, damage=6) for _ in range(5)] +
    [Card("Defend", 1, block=5) for _ in range(4)] +
    [bash, cripple]
)
player.draw_pile = player.deck[:]
random.shuffle(player.draw_pile)

# Battle Loop
floor = 1
enemy = random_enemy(floor)
print(f"\nEnemy appears: {enemy}")

while not player.is_dead() and not enemy.is_dead():
    enemy.show_intent()
    player.start_turn()

    print("\nYour Hand:")
    for i, card in enumerate(player.hand):
        print(f"{i+1}.")
        card.display()

    while True:
        if not player.hand:
            print("No cards left in hand!")
            break

        print(f"\nChoose a card to play (1 to {len(player.hand)} or 0 to end turn):")
        for i, card in enumerate(player.hand):
            print(f"{i+1}. {card.name} (Cost: {card.energy_cost})")

        try:
            choice = int(input(" ")) - 1
            if choice == -1:
                print("Ending turn.")
                break
            player.play_card(choice, enemy)
            if enemy.is_dead():
                print(f"{enemy.name} has been defeated!")
                break
            if player.energy == 0:
                print("No energy left.")
                break
        except (ValueError, IndexError):
            print("Invalid input. Please enter a number corresponding to a card.")

    if enemy.is_dead():
        break

    print(f"\n --- {enemy.name}'s Turn ---")
    enemy.attack(player)
    enemy.choose_intent()

    player.discard_pile.extend(player.hand)
    player.hand.clear()
    print("End of turn. Discarded hand.")

# End Result
if player.is_dead():
    print(f"\n{player.name} has been defeated. Game over.")
else:
    print(f"\nVictory! {enemy.name} was defeated.")