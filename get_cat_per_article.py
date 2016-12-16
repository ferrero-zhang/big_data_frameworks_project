import pandas as pd
import pickle

pages_index = pd.read_csv('seded_index.txt', 
                          sep='#', header=None)

links = pd.read_csv('links.csv', sep='#', header=None)

cats = links.set_index(0)
cats = cats[1].apply(hash)
cats = cats.reset_index().set_index(1)

with open('seen_categories/queue_seen_croyance_2.pkl', 'rb') as f:
    croyance = pickle.load(f)

with open('seen_categories/queue_seen_espace_2.pkl', 'rb') as f:
    espace = pickle.load(f)

with open('seen_categories/queue_seen_science_2.pkl', 'rb') as f:
    science = pickle.load(f)

def make_series(set_, name):
    s = pd.Series(list(set_)).apply(hash)
    s = s.reset_index().set_index(0)
    s.columns = [name]
    s[name] = 1
    return s

croyance = make_series(croyance, 'croyance')
science = make_series(science, 'science')
espace = make_series(espace, 'espace')

# join everything based on article id
res = cats.join(croyance).join(espace).join(science)
