import json


def load_counter():
    with open("assets/search_count.json", "r") as f:
        counter = json.load(f)
        return counter


def save_counter(counter):
    with open("assets/search_count.json", "w") as f:
        json.dump(counter, f)


def load_query():
    with open("assets/query.json", "r") as f:
        query = json.load(f)
        return query


def save_query(query):
    with open("assets/query.json", "w") as f:
        json.dump(query, f)


def load_items():
    with open("assets/items.json", "r") as f:
        items = json.load(f)
        return items

def save_items(items):
    with open("assets/items.json", "w") as f:
        json.dump(items, f)

