import pickle
from coursedef import Course

rfile = 'catalog.pickle'
with open(rfile, 'rb') as f:
    cc = pickle.load(f)
    print(cc)
