import random
import json

def get_random_list_value(target_list:list):
    return target_list[random.randint(0, len(target_list)-1)]

def check_word_exists(word:str, text:str):
    if word in text.split(" "):
        return True
    return False

def check_if_date_exists(date) -> bool:
    with open("dates.json", "r") as file:
        date_json : list = json.load(file)
  
    if date not in date_json:
        date_json.append(date)
        with open("dates.json", "w") as file:
            json.dump(date_json, file, indent=4)
        return False
    return True

if __name__ == "__main__":
    print(get_random_list_value(["oi", "tudo", "bem"]))