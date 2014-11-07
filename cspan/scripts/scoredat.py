import processdata
import argparse
import os
#ARG PARSING (TODO: put this in an if __name__ == "__main__")
parser = argparse.ArgumentParser(description='Scoring for CSPAN data')
parser.add_argument('choice', metavar='cond', type=int, help='0:operation span (ospan), 1:reading span (rspan), 2:symmetry span (sspan)')
parser.add_argument('fname', metavar='fname', type=str, help='input file name')
parser.add_argument('out', nargs='?', metavar='out', type=str, help='output name')

args = parser.parse_args()
choice = args.choice        #task selection (from sysarg)

options = ['ospan', 'rspan', 'sspan']
fname = args.fname
path, end = os.path.split(args.fname)
#output file names
if not args.out:
    output = 'scored' + options[choice] + '.tsv'
    longoutput = 'scoredlong' + options[choice] + '.tsv'
else:
    output = args.out
    longoutput = '%s_long%s'%os.path.splitext(args.out)

d = {}
d['ospan'] = {'PROC_ACC':'OPERATION.ACC', 'PROC_STIM_RT':'showProblem.RT', 'PROC_MAX_RT': 'mathtime[Trial]', 'TBR_STIM': 'letterstimuli'}
d['rspan'] = {'PROC_ACC':'SENSEBOTH.ACC', 'PROC_STIM_RT':'showSentence.RT', 'PROC_MAX_RT': 'mathtime[Trial]', 'TBR_STIM': 'letterstimuli'}
d['sspan'] = {'PROC_ACC':'CheckResponse.ACC', 'PROC_STIM_RT':'ShowSymm.RT', 'PROC_MAX_RT': 'SymmetryTime', 'TBR_STIM': 'MatrixId'}
session = 1

x = processdata.getPartNums(fname)
print x
skipped = []
for ii, part in enumerate(x):
    print part
    scoreme = processdata.Score(fname, partNum = part, sessNum = session, **d[options[choice]])
    print len(scoreme.data)
    if len(scoreme.data) < 100:
        skipped.append(part)
        print 'SKIPPED ', part
        continue
    scoreme.globalScores(append = True, fname = output)
    scoreme.saveScore(longoutput, append = (ii != 0))

print "Skipped the following:\n\n", skipped
