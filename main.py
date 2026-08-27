import random
import json
import time

#loading some needed files
with open("data/civilisation.json") as file:
    data = json.load(file)
with open("data/intro.txt", "r") as file:
    intro_lines = file.readlines()


class Civilisation():
    def __init__(self):
        self.population = random.randint(100, 1000)
        self.explicitness = random.randint(0, 10)

        self.geography, self.mobility_level = set_geography()
        self.resources = get_resources(self.geography)

        self.write_to_json()

    def write_to_json(self):
        civilisation_data = {
            "population": self.population,
            "geography": self.geography,
            "mobility_level": self.mobility_level,
            "resources": self.resources,
            "explicitness": self.explicitness
        }

        with open("data/init_civ.json", "w") as file:
            json.dump(civilisation_data, file, indent=4)

    def display(self):
        print("\n--- CIVILISATION ---")
        print(f"Population: {self.population}")
        print(f"Geography: {self.geography}")
        print(f"Mobility: {self.mobility_level}/10")
        print(f"Resources: {', '.join(self.resources)}")
        print(f"Cultural explicitness: {self.explicitness}/10")



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
    resource_count = random.randint(3, 5)

    specific_resources = data["resources"]["specific"][geography]
    general_resources = data["resources"]["general"]

    resources = random.sample(specific_resources, 2)

    remaining = resource_count - 2

    resources += random.sample(general_resources, remaining)

    return resources



def main():
    civilisation = Civilisation()

    running = True
    year = 0
    while running:
        if year == 0:
            for line in intro_lines:
                print(line, end="")
                time.sleep(3)

        print(f"\nYEAR {year}")
        print(civilisation.display())
        time.sleep(5)
        break

#Let's figure out the flow of this project

#first: we need to initialize a civilisation
#we will write to a new csv file
#Criteria: pop, geography, resources, occupations

#second: we will generate a basic vocabulary
#I think the way we can do this is just to make a very simple representative 10-word list
#I think the way we generally do this is through some sort of dashboard
#maybe also a conversation at the time


#third: add evolution features
#THIS PART REQUIRES SOME BASIC RESEARCH
#Language should respond to the world, so it develops diff environment words


#Fourth: generate multiple civilisations
#This should be another mode or something we set in a menu

if __name__ == "__main__":
    main()