from coursedef import Course
import pickle

# debug tool for printing the catalog

rfile = 'catalog.pickle'

with open(rfile, 'rb') as f:
    # load pickled catalog dictionary
    cc = pickle.load(f)
    for tt, cs in cc.items():
        print(f'{tt}, {cs.title}, {cs.description[:10]}, {cs.prereqs}, {cs.coreqs}')
