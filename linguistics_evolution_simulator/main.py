import random
import json
import time

from pathlib import Path
DATA_DIR = Path(__file__).parent / "data"

word_shift_modifier = 0 # number of words that are shifted per iteration
vowels = str()
consonants = str()
modified_words = list()

#loading some needed files
with open(DATA_DIR / "civilisation.json") as file:
    data = json.load(file) #loading all potential environment data
with open(DATA_DIR / "words.json") as file:
    word_pool = json.load(file)
with open(DATA_DIR / "events.json") as file:
    all_events = json.load(file)

with open(DATA_DIR / "intro.txt", "r") as file:
    intro_lines = file.readlines()
with open(DATA_DIR / "outro.txt", "r") as file:
    outro_lines = file.readlines()

#can we do it with a grammar function?


class Civilisation():
    def __init__(self):
        self.population = random.randint(100, 1000) # Sets beginning population of the civilisation
        self.geography, self.mobility_level = set_geography() # Sets geographical features of the generated civilisation
        self.resources = get_resources(self.geography) # Gets civilisation resources 
        self.words = generate_words(self.resources) # Generates word-like words + hardwired to initialise 20 words

        self.events = None # variable for events - list of event dicts

        self.write_to_json()

    def write_to_json(self):
        civilisation_data = {
            "population": self.population,
            "geography": self.geography,
            "mobility_level": self.mobility_level,
            "resources": self.resources,
        }

        with open(DATA_DIR / "civilisation_init.json", "w") as file:
            json.dump(civilisation_data, file, indent=4)

    def display_init(self):
        print("\n--- CIVILISATION ---")
        print(f"Population: {self.population}")
        print(f"Geography: {self.geography}")
        print(f"Mobility: {self.mobility_level}/10")
        print(f"Resources: {', '.join(self.resources)}")

    def display(self, year):
        print("\n--- DASHBOARD ---")
        print(f"Population: {self.population}")

        if year < 1000:
            era = "Antiquity"
        elif 1000 < year < 2000:
            era = "Medieval"
        else: 
            era = "Modern"
        print(f"Era: {era}")

        print("\nWORDS")
        for i, word in enumerate(self.words):
            if i == 0:
                print("--> General words")
            elif i == 11:
                print("\n--> Resource Words")
            elif i == 16:
                print("\n--> Era-Specific words")
            print(f"{word}: {self.words[word]}")

        print("\nCHANGES")
        print(f"{word_shift_modifier} words were modified in this iteration.")
        for i, word in enumerate(modified_words):
            print(f"{i + 1}. {word["original"]} --> {word["changed"]}")

        for i, event in enumerate(self.events):
            print(f"\n{i + 1}.", event["event"])
            print(f"Population change: {round(event["population_shift_modifier"] * 100)}%")

    def iterate_event(self):
        a = 0
        self.events = []

        for event in all_events["events"]:
            if self.population > 3000:
                self.events.append(all_events["events"][8])
                continue
            a = random.randint(0, 1)
            if a == 1 and len(self.events) < 3:
                self.events.append(event)
                
    def iterate_population(self):
        self.population += round(0.2 * self.population)
        for event in self.events:
            self.population += round(event["population_shift_modifier"] * self.population)

    def iterate_words(self, year):
        global word_shift_modifier
        word_shift_modifier = 0

        for event in self.events:
            word_shift_modifier += event["word_shift_modifier"]

        word_shift_modifier = max(0, min(word_shift_modifier, 10))  # Maximum 10 words changed per iteration


        new_era_words = None

        if year == 1000 or year == 2000:
            if year == 1000:
                new_era_words = word_pool["medieval"]
            else:
                new_era_words = word_pool["modern"]

            old_words = list(self.words.keys())[-5:]

            for word in old_words:
                self.words.pop(word)

            for word in new_era_words[:5]:
                global vowels
                global consonants
                self.words[word] = make_word(vowels, consonants)

            self.events.append({
                "event": "New era, new words - Change of era! Last 5 era-specific words have changed.",
                "population_shift_modifier": 0,
                "word_shift_modifier": 0
            })


        count = 0
        global modified_words
        modified_words = []

        words_to_change = random.sample(
            list(self.words.keys()),
            min(word_shift_modifier, len(self.words))
        )

        for word in words_to_change:
            change = {
                "original": self.words[word],
                "changed": None
            }

            self.words[word] = mutate_word(self.words[word])

            change["changed"] = self.words[word]
            modified_words.append(change)

            count += 1
#----------------------------------------------------------------------------------------
        

def set_geography():
    geography = random.choice(data["geographies"])

    if geography == "Forest":
        mobility_level = random.randint(3, 6)
    elif geography == "Plains":
        mobility_level = random.randint(6, 9)
    elif geography == "Desert/Steppe":
        mobility_level = random.randint(7, 10)
    elif geography == "Mountains/Valley":
        mobility_level = random.randint(0, 3)
    elif geography == "Wetlands (Ocean, River)":
        mobility_level = random.randint(4, 7)
    return geography, mobility_level

def get_resources(geography):
    resource_count = 5

    specific_resources = data["resources"]["specific"][geography]
    general_resources = data["resources"]["general"]

    resources = random.sample(specific_resources, 2)

    remaining = resource_count - 2

    resources += random.sample(general_resources, remaining)

    return resources

def generate_words(resources):
    words = dict()
    for word in word_pool["general"]:
        words[word] = None
    for resource in resources:
        words[resource] = None
    for word in word_pool["antiquity"]:
        words[word] = None

    all_vowels = "aeiou"
    all_consonants = "bcdfghjklmnpqrstvwxyz"

    global vowels
    global consonants
    vowels = random.sample(all_vowels, 3)
    consonants = random.sample(all_consonants, 10)

    for word in words:
        words[word] = make_word(vowels, consonants)

    return words

def make_word(vowels, consonants):
    word = ""
    for _ in range(random.randint(2, 3)):
        word += random.choice(consonants)
        word += random.choice(vowels) 

    return word

def mutate_word(word):
    vowels = "aeiou"
    consonants = "bcdfghjklmnpqrstvwxyz"

    index = random.randint(0, len(word) - 1)
    old_letter = word[index]

    if old_letter in vowels:
        possible_letters = vowels
    else:
        possible_letters = consonants

    new_letter = random.choice(possible_letters)

    while new_letter == old_letter:
        new_letter = random.choice(possible_letters)

    return word[:index] + new_letter + word[index + 1:]



def main():
    civilisation = Civilisation()

    running = True
    year = 0
    while running:
        if year == 0:
            #for line in intro_lines:
                #print(line, end="")
                #time.sleep(3)
            print("\n")
            print(f"\nYEAR {year}")
            civilisation.display_init()
            time.sleep(5)
            year += 100

        print(f"\nYEAR {year}")         
        civilisation.iterate_event() # Randomly gets events that are happening this iteration cycle
        civilisation.iterate_population() # Changes civilisation population (mechanic related to some events)
        civilisation.iterate_words(year) # Changes the words in the dashboard
        civilisation.display(year) # Displays a dashboard
        time.sleep(10) # 10 seconds for you to review the word changes in the dashboard

        if year == 3000:
            print("\n")
            for line in outro_lines:
                print(line, end="")
                time.sleep(3)
            break 

        year += 100

if __name__ == "__main__":
    main()