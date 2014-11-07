'''
Class for scoring the AOSPAN using math accuracy, speed, and correct recall as scoring criteria.  Well,
I mean, that's what it started as.
        Author: Michael Chow
        Date:   28 Apr 2011

        initializes using a tab delimited data file name, with optional parameters for participant number, sess num.
        Requires the following columns from E-DataAid:
            AccErrorTotal                     total number of accuracy errors
            letterstimuli                     stimulus shown to participant
            MathErrorTotal                    total number of math errors
            mathtime[Trial]                   time allowed on arithematic component
            OPERATION.RT                      time spent on true / false screen
            OPERATION.ACC                     1 for operation answered correctly or time expires
            Procedure[Block]
            Running[SubTrial]                 task block (practice, TrialList, etc..)                         
            showProblem.RT                    time spent on arithematic component, 0 if time expires (speed error)
            Subject                          
            WordSelection                     responses selected by participant
            Session
            ExperimentName

        Fore RSPAN need:
            SENSEBOTH.RT
            SENSEBOTH.ACC
            showSentence.RT

                                              
            
'''
import os

#testStart = 63                              #test trials begin on this row (not used anymore)
def getPartNums(fname, header = 6):
    f = open(fname)
    data = f.readlines()
    data = [data[ii].strip('\n').split('\t') for ii in xrange(len(data))]
    # look for header row using the var header.  If can't find, search rows around it.
    try: data[header].index('Subject')            
    except ValueError:
        header += 3
        while header > -1:
            try:
                data[header].index('Subject')
                header = header
                break
            except ValueError:
                header += -1
    partNumCol = data[header].index('Subject')
    partNums = set()
    for row in data[header+1:]:
        partNums.add(row[partNumCol])
    return list(partNums)




class Score:    


    def __init__(self, fname, partNum = '', sessNum = '', header = 1, PROC_ACC = "OPERATION.ACC", PROC_STIM_RT = 'showProblem.RT', PROC_MAX_RT = 'mathtime[Trial]', TBR_STIM = 'letterstimuli'):
        self.header = header
        self.PROC_ACC = PROC_ACC
        self.PROC_MAX_RT = PROC_MAX_RT
        self.PROC_STIM_RT = PROC_STIM_RT
        self.TBR_STIM = TBR_STIM
        f = open(fname)
        data = f.readlines()
        self.data = [data[ii].strip('\n').split('\t') for ii in xrange(len(data))]
        # reads: data[rows][cols]
        
        try: data[header].index('Subject')            #checks if header works, tries to find right header
        except ValueError:
            header += 3
            while header > -1:
                try:
                    data[header].index('Subject')
                    self.header = header
                    break
                except ValueError:

                    header += -1
        self.partNum = partNum
        self.sessNum = sessNum
        if partNum:
            subjectCol = self.data[self.header].index('Subject')
            self.data = [self.data[header]] + [row for row in self.data if row[subjectCol] == partNum]

            


    def scoreRecall(self, omt_char = ''):
        stimList = self.getStimList()
        respList = self.getRespList()

        trialList = [[], [], [], [], []]                              #[trialNum, stimNum, stim, resp, corr]
        for trial in range(len(stimList)):
            diff = len(respList[trial]) - len(stimList[trial])       # < 0 if stimList is longer
            if diff < 0:
                respList[trial] = list(respList[trial])
                respList[trial].extend([omt_char]*abs(diff))         # fill in omt_char for non-responses
                respList[trial] = tuple(respList[trial])             # make respList at least as long
            if diff > 0:
                respList[trial] = respList[trial][:len(stimList[trial])]
            score = self.checkMatch(stimList[trial], respList[trial], retCols = True)
            trialList[0].extend([trial+1]*len(stimList[trial]))
            for ii in range(4):
                trialList[ii+1].extend(score[ii])
        return trialList

    def scoreMathWithRecall(self, serial = True):
        mathtimeCol = self.getStimList(colName = self.PROC_MAX_RT)
        opACCList = self.getStimList(colName = self.PROC_ACC)         #all are [(trial1-item1,..), (trial2-item1,..), (trial3,..)]
        probRTList = self.getStimList(colName = self.PROC_STIM_RT)
        stimList = self.getStimList()
        respList = self.getRespList()
        opACCCol = []
        probRTCol = []
        alltogether = []
        countforspan = []
        for trial in xrange(len(opACCList)):            #by trial
            recallAcc = self.checkMatch(stimList[trial], respList[trial], serial = serial)[3]
            for item in xrange(len(opACCList[trial])):  #by stim
                if (int(opACCList[trial][item]) != 0) and (int(probRTList[trial][item]) != 0):  #no acc or math errors
                    if recallAcc[item] == 1: alltogether.append(1)
                    else: alltogether.append(0)
                else:
                    alltogether.append(0)

            opACCCol.extend(opACCList[trial])                           #if you've chanced upon this, apologies for the patchy
            probRTCol.extend(probRTList[trial])                         #list extensions here!  Last minute move to make 
            countforspan.extend(alltogether)                            #everything columns
            alltogether = []
        return opACCCol, probRTCol, countforspan
            
            

    def saveScore(self, fname, append = True):
        #Write the data in this format:      trialNum    Stim    Resp    isCorrect      mathAcc     speedErrors     ttlCorrect
        
        trialList = self.scoreRecall()              #[trialNum, stimNum, stim, resp, corrRecall]
        mathList = self.scoreMathWithRecall()       #[accuracy, problemRT, correct_by_new_scoring_proc]
        mathTimeLim = self.getStimList(colName = self.PROC_MAX_RT)[0][0]
        f = open(fname, ['w','a'][append])
        if not append:
            f.write('partNum' + '\t' + 'sessNum' + '\t' +
                'trialNum' + '\t' + 'stimNum' + '\t' + 'stim' + '\t' + 'resp' + '\t' 'corrRecall' + '\t' +
                'mathAcc' + '\t' + 'probRT' + '\t' + 'MOSPAN_scoring' + '\t'
                'mathTimeLim' + '\n')

        for trial in range(len(trialList[0])):
            f.write(str(self.partNum) + '\t' + str(self.sessNum) + '\t')
            for var in trialList:
                f.write(str(var[trial]) + '\t')
            for var in mathList:
                f.write(str(var[trial]) + '\t')
            f.write(str(mathTimeLim) + '\n')

                    
    def globalScores(self, ret = False, append = False, fname = None):
        d = {}
        d['PartNum'] = self.partNum
        d['SessNum'] = self.sessNum
        d['TimeLim'] = self.getStimList(colName = self.PROC_MAX_RT)[0][0]
        expcol = self.data[self.header].index('ExperimentName')
        d['task'] = self.data[2][expcol]
        mathVars = self.scoreMathWithRecall()       #[opACC],[probRT],[countforspan]
        RT = [int(ii) for ii in mathVars[1]]
        ACC = [int(ii) for ii in mathVars[0]]
        tooSlow = 0
        errCount = 0
        accErr = 0
        for ii in range(len(mathVars[0])):
            if RT[ii] == 0 or ACC[ii] == 0: errCount += 1
            if RT[ii] == 0: tooSlow += 1
            if ACC[ii] == 0: accErr += 1
        d['err_Math'] = errCount
        try: d['meanMathRT1'] = sum(RT) / (len(RT) - tooSlow)                                #avg when RT < time limit
        except ZeroDivisionError: d['meanMathRT1'] = 'NA'                                   #Once I had a participant click haphazardly through the practice...
        d['meanMathRT2'] = ( sum(RT) + int(d['TimeLim'])*tooSlow ) / len(mathVars[1])   #overall avg
        d['err_Speed'] = tooSlow
        d['err_Acc'] = accErr

        recallVars = self.scoreRecall()      #[trialNum, stimNum, stim, resp, corr]
        trialNum = 1
        absCorr = True
        absSpan = 0
        for ii in range(len(recallVars[0])):
            if recallVars[4][ii] == 0: absCorr = False
            if ii == len(recallVars[0]) - 1 or trialNum != recallVars[0][ii+1]:
                trialNum += 1
                if absCorr == True:
                    absSpan += recallVars[1][ii]
                    
                absCorr = True
        
        d['span_Abs'] = absSpan              #sum sets in which all letters were recalled correctly
        d['span_Ttl'] = sum(recallVars[4])            #all letters recalled correctly
        d['span_MOSPAN'] = sum(mathVars[2])
        d['span_MOSPAN2'] = sum(self.scoreMathWithRecall(serial = False)[2])
        trialNum = 1
        pcus_score = 0
        total = 0
        setsize = 0
        for ii in range(len(recallVars[0])):
            if recallVars[4][ii] == 1: pcus_score += 1
            setsize += 1
            if ii == len(recallVars[0]) - 1 or trialNum != recallVars[0][ii+1]:            
                trialNum += 1
                total += float(pcus_score) / setsize
                pcus_score = 0
                setsize = 0
        total = total / trialNum * len(recallVars[0])
                

        d['span_PCUS'] = total
        self.globalData = d

        if append == True:
            keys = d.keys()
            keys.sort()

            if not os.path.isfile(fname):
                f = open(fname, 'a')
                for key in keys:
                    f.write(key + '\t')
                f.write('\n')
            else: f = open(fname, 'a')
            
            for key in keys:    
                f.write(str(d[key]) + '\t')
            f.write('\n')


        if ret == True: return d
            

    #  The next two loops follow the fact that stimuli are in the TrialList rows,
    #  while responses are under recalList.  Various idiosyncracies are taken into
    #  account.  See the E-DataAid spreadsheet for a better picture of what's happening

    #Goes through the rows where letter stimuli are.
    #Possible colName args: 'showProblem.RT', 'OPERATION.RT', 'OPERATION.ACC', 'letterstimuli'
    def getStimList(self, colName = None, data = None):
        if not colName: colName = self.TBR_STIM
        if not data: data = self.data
        #Iterate each row, checking block, group stimuli by trial
        startRow = self.findStartRow(data)
        stimCol = data[self.header].index(colName)            #col number for category
        blockCol = data[self.header].index('Running[SubTrial]')      
        stimList = []
        stims = []
        for row in xrange(startRow, len(data)):
            if data[row][blockCol] == 'TrialList':
                stims.append(data[row][stimCol])
                if data[row+1][blockCol] == 'recalList':
                    stimList.append(tuple(stims))
                    stims = []
        return stimList

    def getRespList(self, data = None):
        if not data: data = self.data
        #Similar to previous, only gather letter responses
        startRow = self.findStartRow(data)
        letterRespCol = data[self.header].index('WordSelection')
        blockCol = data[self.header].index('Running[SubTrial]')
        respList = []       #holds each resp var list
        resp = []           #set of responses for trial
        for row in xrange(startRow, len(data)):
            if data[row][blockCol] == 'recalList':
                if data[row][letterRespCol] in ['Enter', 'Exit']:              #clear resp, add to respList (OSPAN, RSPAN use 'Exit', SymmSpan uses 'Enter')
                    respList.append(tuple(resp))
                    resp = []
                elif not data[row][letterRespCol]:                  #skip blanks (not "blank", but "")
                    pass
                elif data[row][letterRespCol] == "InvalidResponse": #skip InvalidResponse (the eprime task ignores them when scoring)
                    pass
                elif data[row][letterRespCol] == "clear":           #start over if participant cleared
                    resp = []                                       
                else:
                    resp.append(data[row][letterRespCol])           #append responses
        return respList
    
    #Now obselete through getStimList (colName arg)
    def getMathRTList(self):
        startRow = self.findStartRow(data)
        showProbRTCol = self.data[self.header].index(self.PROC_STIM_RT)
        blockCol = data[self.header].index('Running[SubTrial]')
        MathRTList = []
        RTs = []
        for row in xrange(startRow, len(data)):
            if data[row][blockCol] == 'TrialList':
                stims.append(data[row][showProbRTCol])
                if data[row+1][blockCol] == 'recalList':
                    MathRTList.append(tuple(RTs))
                    RTs = []
        return MathRTList

    def findStartRow(self, data = None):
        if not data: data = self.data
        row = 0
        procCol = data[self.header].index('Procedure[Block]')
        for ii in range(2, len(data)):
            if data[ii][procCol] == 'SessionProc':
                row = ii
                break
        return row

    def checkMatch(self, stims, resps, retCols = True, serial = True):
        scoredList = []
        stimNum = []
        for ltr in range( len(stims) ):
            stimNum.append(ltr+1)
            if serial: incorrect = (ltr >= len(resps) or stims[ltr] != resps[ltr])         #match with specific response
            else: incorrect = (stims[ltr] not in resps)                   #see if stim in response list
            #if reach end of responses or answer doesn't match stim
            if incorrect: scoredList.append(0) 
            else: scoredList.append(1)

        if retCols == True:
            return stimNum, stims, resps, scoredList

        else:
            return zip(stimNum, stims, resps, scoredList)            # cuts off at shortest list, either stims or resps

