import random
import json
import time

word_shift_modifier = 0 # number of words that are shifted per iteration
vowels = ""
consonants = ""

#loading some needed files
with open("data/civilisation.json") as file:
    data = json.load(file) #loading all potential environment data
with open("data/words.json") as file:
    word_pool = json.load(file)
with open("data/events.json") as file:
    all_events = json.load(file)

with open("data/intro.txt", "r") as file:
    intro_lines = file.readlines()
with open("data/outro.txt", "r") as file:
    outro_lines = file.readlines()




class Civilisation():
    def __init__(self):
        self.population = random.randint(100, 1000) # Sets beginning population of the civilisation
        self.explicitness = random.randint(0, 10) # Sets initial "explicitness" of the population (mechanic)

        self.geography, self.mobility_level = set_geography() # Sets geographical features of the generated civilisation
        self.resources = get_resources(self.geography) # Gets civilisation resources 

        self.words = generate_words(self.resources) # Generates word-like words + hardwired to initialise 20 words
        #self.grammar = generate_grammar()
        #self.sentences = None

        self.events = None # variable for events - list of event dicts

        self.write_to_json()

    def write_to_json(self):
        civilisation_data = {
            "population": self.population,
            "geography": self.geography,
            "mobility_level": self.mobility_level,
            "resources": self.resources,
            "explicitness": self.explicitness
        }

        with open("data/civilisation_init.json", "w") as file:
            json.dump(civilisation_data, file, indent=4)

    def display_init(self):
        print("\n--- CIVILISATION ---")
        print(f"Population: {self.population}")
        print(f"Geography: {self.geography}")
        print(f"Mobility: {self.mobility_level}/10")
        print(f"Resources: {', '.join(self.resources)}")
        print(f"Cultural explicitness: {self.explicitness}/10")

    def display(self):
        print("\n--- DASHBOARD ---")
        print(f"Population: {self.population}")

        print("\nWORDS")
        for word in self.words:
            print(f"{word}: {self.words[word]}")

        print("\nGRAMMAR")
        print(f"Word order: we are checking") #for later: {self.words["word_order"]}
        print(f"Verb tenses: we are checking", end="")
        #for tense in self.words["verb_tenses"]:
            #print(tense, end=" ")

        print("\nEXAMPLES")
        #for sentence in self.sentences:
            #print(sentence)

        print("\nCHANGES")
        print(f"{word_shift_modifier} words were modified in this iteration.")
        for i, event in enumerate(self.events):
            print(f"\n{i + 1}.", event["event"])
            print(f"Population change: {round(event["population_shift_modifier"] * 100)}%")

    def iterate_event(self):
        a = 0
        self.events = []

        for event in all_events["events"]:
            if self.population > 1500:
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
        word_shift_modifier = max(0, min(word_shift_modifier, 10)) # Maximum 10 words changed per iteration

        new_era_words = None

        if year == 1000 or year == 2000:
            if year == 1000:
                new_era_words = word_pool["medieval"]
            else:
                new_era_words = word_pool["modern"]
            old_words = list(self.words.keys())[15:]

            for word in old_words:
                self.words.pop(word)

            for word in new_era_words[:5]:
                global vowels
                global consonants
                self.words[word] = make_word(vowels, consonants)

            self.events.append({"event": "New era, new words - Change of era! Last 5 era-specific words has changed.", 
                                "population_shift_modifier": 0})

        count = 0
        a = 0 
        for word in self.words:
            if count == word_shift_modifier:
                break
            a = random.randint(0, 1)
            if a == 1:
                self.words[word] = mutate_word(self.words[word])
                count += 1

    def iterate_grammar(self):
        ...
        #unfinished function, can potentially be used to add linguistic expressions/grammar evolution but this has to be seen

#----------------------------------------------------------------------------------------
        

def set_geography():
    geography = random.choice(data["geographies"])

    if geography == "forest":
        mobility_level = random.randint(3, 6)
    elif geography == "plains":
        mobility_level = random.randint(6, 9)
    elif geography == "desert/steppe":
        mobility_level = random.randint(7, 10)
    elif geography == "mountains/valley":
        mobility_level = random.randint(0, 3)
    elif geography == "wetlands (ocean, river)":
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

def generate_grammar():
    ...

def mutate_word(word):
    index = random.randint(0, len(word) - 1)

    letters = "aeioubcdfghjklmnpqrstvwxyz"

    old_letter = word[index]

    new_letter = random.choice(letters)

    while new_letter == old_letter:
        new_letter = random.choice(letters)

    return word[:index] + new_letter + word[index + 1:]



def main():
    civilisation = Civilisation()

    running = True
    year = 2900
    while running:
        print(f"\nYEAR {year}")
        if year == 0:
            for line in intro_lines:
                print(line, end="")
                time.sleep(3)
            civilisation.display_init()
            
        civilisation.iterate_event() # Randomly gets events that are happening this iteration cycle
        civilisation.iterate_population() # Changes civilisation population (mechanic related to some events)
        civilisation.iterate_words(year) # Changes the words in the dashboard
        civilisation.display() # Displays a dashboard
        time.sleep(10) # 10 seconds for you to review the word changes in the dashboard

        if year == 3000:
            for line in outro_lines:
                print(line, end="")
                time.sleep(3)
            break 

        year += 100

if __name__ == "__main__":
    main()