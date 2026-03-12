import random

names = [
    "Arjun", "Ananya", "Meera", "Rahul", "Sneha", "Vikram", "Aditi", 
    "Kiran", "Neha", "Rohan", "Pooja", "Sanjay", "Nithin", "Akhil","juni","safna","Arya","vidhya","athul","vishnu","ronald",
    "sreenand","akshay","adarsh","nikitha","jasil","rashi","salma","sithara","sithu","manu","renju","akhil","viji","sudheer","sindhu",
    "devika","aksaya","sheena","biju","sabitha","kannan","mohan"
]

def get_random_patient():
    return {
        "name": random.choice(names),
        "age": random.randint(5, 80),
        "gender": random.choice(["Male", "Female"]),
        "contact": f"9{random.randint(100000000,999999999)}",
        "id": f"PID{random.randint(1000,9999)}"
    }