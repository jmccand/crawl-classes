from coursedef import Course
import pickle

rfile = 'catalog.pickle'

with open(rfile, 'rb') as f:
    cc = pickle.load(f)
    for tt, cs in cc.items():
        print(f'{tt}, {cs.title}, {cs.description[:10]}, {cs.prereqs}, {cs.coreqs}')
