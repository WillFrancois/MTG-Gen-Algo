import random

#Creating global variables for interaction with decks

deck_array = []
mana = [0,0]
card_types = [1,2,3,"L"]
turn_number = 3
starting_hand_amount = 7

#Declaring deck object

class Deck:
    def __init__(self, card_list: list, fitness):
        self.card_list = card_list
        self.fitness = fitness

best_decks = [Deck([random.choice(card_types) for i in range(60)], float('-inf')), Deck([random.choice(card_types) for i in range(60)], float('-inf')), Deck([random.choice(card_types) for i in range(60)], float('-inf')), Deck([random.choice(card_types) for i in range(60)], float('-inf')), Deck([random.choice(card_types) for i in range(60)], float('-inf'))]

#Creating 100 decks with random cards

for i in range(100):
    new_card_list = []
    new_card_list.append(random.choices(card_types, k=60))
    print(new_card_list)

    d = Deck(new_card_list[0], 0)
    deck_array.append(d)

#Finding the fitness of decks by adding lands and checking mana fits
def Simulate_Decks():
    
    global mana
    global deck_array
    global card_types
    global turn_number
    global starting_hand_amount

    for i in deck_array:
        #Running number of trials
        for j in range(200):
            #Shuffle the deck and create the hand
            random.shuffle(i.card_list)
            hand = []

            #Initial hand
            for k in range(starting_hand_amount):
                try:
                    hand.append(i.card_list[k])
                except IndexError:
                    print(k)
                    print(i.card_list)
                    print(starting_hand_amount)
                    print(hand)

            for k in range(turn_number):
                #Play land card at start of turn
                if "L" in hand:
                    hand.remove("L")
                    mana[1] += 1 #Total mana added by 1
                    mana[0] += 1 #Current mana added by 1
                #Play highest mana cards to fit mana pool
                else:
                    i.fitness -= k

                for m in range(mana[0], -1, -1):
                    if m == -1:
                        break
                    if m in hand:
                        hand.remove(m)
                        i.fitness += m
                        mana[0] -= m
                mana[0] = mana[1]
                hand.append(i.card_list[starting_hand_amount + k])
            mana = [0,0]

def Find_Best_Decks():
    
    global deck_array

    deck_array.sort(key=lambda deck: deck.fitness, reverse=True)
    del deck_array[4:99]
    if deck_array[0].fitness > best_decks[0].fitness:
        print("Changing Best Decks")
        for i in range(len(deck_array)):
            best_decks[i].fitness = deck_array[i].fitness
            best_decks[i].card_list = deck_array[i].card_list
    print(deck_array[0].fitness, best_decks[0].fitness)

def Evolve():
    
    global deck_array
    global best_decks

    for i in range(len(best_decks)):
        evolution_type = random.randint(0, 1)
        for j in range(19):

            #Mutation
            if evolution_type == 0:
                evolution_card_list = best_decks[i].card_list[:]
                x, y = random.randint(0, 59), random.randint(0, 59)
                evolution_card_list[min(x,y):max(x,y)] = random.choices(card_types, k=(max(x,y)-min(x,y)))
                deck_array.append(Deck(evolution_card_list, 0))
            
            #Mixing
            if evolution_type == 1:
                evolution_card_list = best_decks[i].card_list[:]
                x, y = random.randint(0, 59), random.randint(0, 59)
                random_mixer = random.choice(best_decks).card_list
                evolution_card_list[min(x,y):max(x,y)] = random_mixer[min(x,y):max(x,y)]
                deck_array.append(Deck(evolution_card_list, 0))
                
            #Mixing 2
            if evolution_type == 2:
                evolution_card_list = best_decks[i].card_list[:]
                for j in range(random.randint(0, 59)):
                    evolution_card_list[random.randint(0, 59)] = random.choice(card_types)
                deck_array.append(Deck(evolution_card_list, 0))

        for i in deck_array:
            i.fitness = 0

for i in range(1001):
    print("Generation", i)
    Simulate_Decks()
    Find_Best_Decks()
    if i < 1000:
        Evolve()
    for i in range(len(card_types)-1):
        print(str(i+1), best_decks[0].card_list.count(i+1))
    print("L", best_decks[0].card_list.count("L"))