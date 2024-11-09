# INSTRUCTIONS:
# Ensure the file paths below are accurate.
# Go to a cube in CubeKoga: Overview > Export > Copy to Clipboard.
# Paste into cube_list.txt.
# an implementation of Winchester drafting, where piles are face-up. Meant to be played on my computer and screenshared.

import random
MEMORY = r"C:\python\functions\drafts.txt"
CUBE_LIST_FILE = r"C:\python\Cube\cube_list.txt"

with open(CUBE_LIST_FILE, "r") as f:
    cube_list = f.read()

def remove_non_ascii(text):
    """Strips non-ASCII characters, like delta and prism star, from card names so that file.write doesn't error."""
    return ''.join([i for i in text if ord(i) < 128])


def draw_piles(cube):
    """NOTE: Mutates the list CUBE"""
    piles = [[], [], [], []]
    for i in range(16):
        if len(cube) > 0:
            card = random.choice(cube)
            piles[i % 4].append(card)
            cube.remove(card)

    return piles


def ask_for_confirmed_input(message, processing_function):
    confirmed = False
    while not confirmed:
        try:
            inp = input(message)
            result = processing_function(inp)
            confirmed = (input("Please confirm with Y: ") == "Y")
        except:
            print("Error. Please try again.")

    return result

# process cube card list

lst = cube_list.split("\n")

def find_nth(haystack: str, needle: str, n: int) -> int:
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

final_list = []
for s in lst:
    index = find_nth(s, "\t", 3)
    final_list.append(s[:index].replace("\t", " "))

# Actual code below

cube = list(final_list)
my_cards = []
opp_cards = []

unchosen = list(cube)

first_player = input("Which player is going first? A or G? ")
if first_player == "A":  # swap this for Grant's version of the code
    my_turn = True
    print("Aaron will pick first.")
else:
    my_turn = False
    print("Grant will pick first.")

piles = draw_piles(unchosen)

while len(unchosen) > 0 or len(piles) > 0:
    # set up the piles if there are none existing
    if len(piles) == 0:
        piles = draw_piles(unchosen)
    # one player chooses a pile
    if my_turn:
        for i in range(len(piles)):
            print(f"Pile {i + 1}: {', '.join(piles[i])}")
        chosen_pile = ask_for_confirmed_input("Which pile will Aaron take? ", lambda x: piles[int(x) - 1])
        my_cards = my_cards + chosen_pile
    else:
        for i in range(len(piles)):
            print(f"Pile {i + 1}: {', '.join(piles[i])}")
        chosen_pile = ask_for_confirmed_input("Which pile is Grant taking? ", lambda x: piles[int(x) - 1])
        opp_cards = opp_cards + chosen_pile

    piles.remove(chosen_pile)
    for pile in piles:
        if len(unchosen) > 0:  # otherwise don't add to the piles
            card = random.choice(unchosen)
            pile.append(card)
            unchosen.remove(card)

    if my_turn:
        print(f"You now have: {my_cards} \nGrant now has: {opp_cards}")
        with open(MEMORY, 'w') as file:
            file.write(remove_non_ascii("My cards: \n{0}".format('\n'.join(my_cards))))
    if len(piles) > 0:
        my_turn = not my_turn
    print(f"There are {len(unchosen)} cards left in the deck. There are {len(piles)} piles left.")

# when all cards are drafted
with open(MEMORY, 'w') as file:
    file.write(remove_non_ascii("Aaron's cards: \n{0}\n\nGrant's cards: \n{1}".format('\n'.join(my_cards), '\n'.join(opp_cards))))