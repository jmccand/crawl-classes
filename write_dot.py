import pickle
from coursedef import Course

# write the dot file from the catalog
# note: only writes courses with prerequisites
rfile = 'catalog.pickle'
wdot = 'catdot.dot'

# shrink defines whether or not to graph courses with no prereqs
shrink = True
intree = set()

# write the node for this course
def wnode(f, t):
    # level-dependent shaping (courses with different #s
    # of prereqs get differently shaped outlines
    if False:
        if t[5] == '1':
            f.write(f'\n"{t}" [shape=oval]')
        elif t[5] == '2':
            f.write(f'\n"{t}" [shape=doublecircle]')
        elif t[5] == '3':
            f.write(f'\n"{t}" [shape=triangle]')
        elif t[5] == '4':
            f.write(f'\n"{t}" [shape=box]')
        else:
            raise ValueError('GRADUATE COURSE')
    else:
        # plain text (no shaped outlines)
        f.write(f'\n"{t}" [shape=plain fontsize="8"]')

# write the edge for from (prereq) to to (course)
def wedge(f, fm, to):
    f.write(f'\n"{fm}" -> "{to}" [color="black:invis:black" weight="2"]')

with open(rfile, 'rb') as f:
    cc = pickle.load(f)
    with open(wdot, 'w') as d:
        # write graph type, RPI central node
        d.write('digraph D {\nlayout=twopi; graph [ranksep="30 2" overlap_scale=-5];\nratio=auto;\nfontsize="5"\n"RPI" [shape=circle root=true fontsize="240" fontcolor="red"]')
        # find the courses with prerequisites
        for tt, cs in cc.items():
            if tt[5] in ('1', '2', '3', '4'):
                if len(cs.prereqs) > 0:
                    for p in cs.prereqs:
                        # add course to tree set
                        intree.add(p)

        # write nodes
        for tt, cs in cc.items():
            if tt[5] in ('1', '2', '3', '4'):
                if not shrink or len(cs.prereqs) > 0 or tt in intree:
                    wnode(d, tt[:4]+tt[5:])
        # write edges
        d.write('\n')
        for tt, cs in cc.items():
            if tt[5] in ('1', '2', '3', '4'):
                if len(cs.prereqs) > 0:
                    for p in cs.prereqs:
                        wedge(d, p[:4]+p[5:], tt[:4]+tt[5:])
                else:
                    if not shrink or tt in intree:
                        # connect no prereqs courses to central node
                        wedge(d, 'RPI', tt[:4]+tt[5:])
        d.write('\n}')
