from queue import PriorityQueue
import numpy as np
import pickle
import sys
import pandas as pd

top_cat = sys.argv[1]

print("FOR TOP CATEGORY={}".format(top_cat))

class Queue(list):
    
    def __init__(self, first):
        self.queue = PriorityQueue()
        self.queue.put((0, first))
        self.seen = set([first])
        self.n_searched = 0
        self.res = []
    
    def next(self):
        self.n_searched += 1
        if self.queue.empty():
            print("emptyqueu1")
            raise ValueError
        return self.queue.get()
    
    def add_list(self, priority_number, l):
        for e in l:
            if (e not in self.seen and isinstance(e, str)):
                self.seen.add(e)
                self.queue.put((priority_number + 1, e))

def save_values(queue, top_cat):
    """
    Save the results
    """
    with open('queue_seen_{}.pkl'.format(top_cat), 'wb+') as f:
        pickle.dump(queue.seen, f)
    with open('queue_queue_{}.pkl'.format(top_cat), 'wb+') as f:
        pickle.dump(queue.queue.queue, f)
    with open('queue_res_{}.pkl'.format(top_cat), 'wb+') as f:
        pickle.dump(queue.res, f)
    print("OK for pickles, n_searched={}".format(queue.n_searched))


pages_index = pd.read_csv('../wiki_data/seded_index.txt', 
                          sep='#', header=None)

categories = pages_index[pages_index[2].astype(str).apply(lambda x: x.startswith('Catégorie:'))]

# in order to quickly get corresponding, we index
cat_index = categories.set_index(1, drop=True)

# remove "Catégorie:" from the name
# and replace spaces with _ as it is in wikipedia
cat_index[2] = cat_index[2].apply(lambda x: x[10:])
cat_index[2] = cat_index[2].apply(lambda x: x.replace(" ", "_"))
cat_indices = cat_index.index

# the real pages (non category)
non_cat = pages_index[~pages_index[2].apply(lambda x: ":" in x if isinstance(x, str) else True)]
non_cat_index = non_cat.set_index(1, drop=True)
non_cat_indices = non_cat_index.index

links = pd.read_csv('../wiki_data/links.csv', sep='#', header=None)

links_index = links.set_index(0, drop=True)[1]
# hashed strings allows for much faster comparison
hashed_links_index = links_index.apply(hash)

queue = Queue(top_cat)

k = 0
try:
    while True:
        priority, cat = queue.next()
        sub = links_index[hashed_links_index == hash(cat)]
        indices = cat_indices.intersection(sub.index)
        page_indices = non_cat_indices.intersection(sub.index)
        for ix, row in non_cat_index.loc[page_indices].iterrows():
            queue.res.append((ix, row[0], row[2], top_cat, priority))
        queue.add_list(priority, cat_index.loc[indices][2].values)
        if not k % 100:
            print("looking for={} queue_size={} n_searched={} priority={}".format(
                    cat, len(queue.seen), queue.n_searched, priority))
        k+=1
except KeyboardInterrupt:
    save_values(queue, top_cat)
except ValueError:
    print("############ Empty queue")
    save_values(queue, top_cat)
