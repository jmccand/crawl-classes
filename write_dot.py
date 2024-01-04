import pickle
from coursedef import Course
import sys

# write the dot file from the catalog
# note: only writes courses with prerequisites
rfile = 'catalog.pickle'
if len(sys.argv) < 2:
    print('expected command line argument: <write file>')
    exit()
wdot = sys.argv[1]
filter_code = ''
if len(sys.argv) > 2:
    filter_code = sys.argv[2]

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

# add prerequisites recursively
def add_prereqs_rec(tt):
    # check if already covered
    if not tt in intree:
        intree.add(tt)
        for p in cc[tt].prereqs:
            # add prereq
            add_prereqs_rec(p)

with open(rfile, 'rb') as f:
    cc = pickle.load(f)
    with open(wdot, 'w') as d:
        # find the courses with prerequisites
        for tt, cs in cc.items():
            if tt[5] in ('1', '2', '3', '4') and (filter_code == '' or tt[:4] == filter_code):
                if len(cs.prereqs) > 0 or not shrink:
                    # add this course
                    add_prereqs_rec(tt)

        # write graph type, RPI central node
        # adjust settings based on graph size
        if len(intree) < 50:
            d.write('digraph D {\nlayout=twopi;\nratio=auto;\nfontsize="20"\n"RPI" [shape=circle root=true fontsize="20" fontcolor="red"]')
        else:
            d.write('digraph D {\nlayout=twopi; graph [ranksep="30 2" overlap_scale=-5];\nratio=auto;\nfontsize="5"\n"RPI" [shape=circle root=true fontsize="240" fontcolor="red"]')

        # write nodes
        for tt in intree:
            assert tt[5] in ('1', '2', '3', '4')
            wnode(d, tt[:4]+tt[5:])
            
        # write edges
        d.write('\n')
        for tt in intree:
            cs = cc[tt]
            assert tt[5] in ('1', '2', '3', '4')
            if len(cs.prereqs) > 0:
                for p in cs.prereqs:
                    wedge(d, p[:4]+p[5:], tt[:4]+tt[5:])
            else:
                # connect no prereqs courses to central node
                wedge(d, 'RPI', tt[:4]+tt[5:])
        d.write('\n}')
