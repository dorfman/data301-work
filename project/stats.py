import pandas as pd

def AllGreaterThan(perc, num):
    """Returns a list of candidates that gained over num percent of supporters gained.
    
    Parameters
    ----------
    perc : Series
        A Series holding a list of floats of percents of supporters gained after a candidate drops their campaign. Index by
        candidates still in the race.
    num : float
        The percent threshold for a candidate to be considered a winner.
    """
    
    cands = []
    for b in range(len(perc)):
        if perc[b] > num:
            cands.append(perc[perc == perc[b]])
    return cands
            
def Winner(perc):
    """Returns a list of candidates that gained over half of all gained supporters. If not half, than 0.375. 
    If not 0.375, than 0.3.
    
    Parameters
    ----------
    perc : Series
        A Series holding a list of floats of percents of supporters gained after a candidate drops their campaign. Index by
        candidates still in the race.
    """
        
    cands = AllGreaterThan(perc, 0.5)
    if not cands:
        cands = AllGreaterThan(perc, 0.375)
        if not cands:
            cands = AllGreaterThan(perc, 0.3)
            if not cands:
                cands = AllGreaterThan(perc, 0.25)
    return cands

def WinnerNames(perc):
    """Returns a list of candidates' NAMES that gained over half of all gained supporters. If not half, than 0.375. 
    If not 0.375, than 0.3.
    
    Parameters
    ----------
    perc : Series
        A Series holding a list of floats of percents of supporters gained after a candidate drops their campaign. Index by
        candidates still in the race.
    """
    
    return list(pd.DataFrame(Winner(perc)).columns)

def WinnerPercs(perc):
    """Returns a list of candidates' PERCENTAGES that gained over half of all gained supporters. If not half, than 0.375. 
    If not 0.375, than 0.3.
    
    Parameters
    ----------
    perc : Series
        A Series holding a list of floats of percents of supporters gained after a candidate drops their campaign. Index by
        candidates still in the race.
    """
    
    winnings = Winner(perc)
    return [winnings[x][0] for x in range(len(winnings))]

def GetPollsStats(polls, dropout, names):
    """Returns a list of winners' actual polling data from a specific snippet of the polls DataFrame.
    
    Parameters
    ----------
    polls : DataFrame
        A snippet of the main DataFrame used sliced to only include polls take a week prior to and a week 
        after the dropout suspends their campaign.
    dropout : str
        The name of the candidate that dropped out.
    names : list(str)
        The names of the candidates who "won" the most supporters after the dropout suspended their campaign.
    """
    
    nums = []
    for n in names:
        nums.append(polls.loc[dropout][n])   
    return nums


def GenStats(PollingBeforeDrop, PollingAfterDrop, PollingDiff):
    statList = []
    cands = list(PollingDiff.index)
    for c in cands:
        stats = {'name': c,
                 'Polling Differences': PollingDiff.loc[c],
                 'Polling of Dropout': PollingDiff.loc[c][c]}

        stats['Polling Differences'][c] = 0
        stats['Polling Sum Negative'] = sum([b for b in stats['Polling Differences'] if b < 0])
        stats['Polling Sum Positive'] = sum([b for b in stats['Polling Differences'] if b > 0])
        stats['Polling Sum Positive Percentages'] = pd.Series([0 if b < 0 else b / stats['Polling Sum Positive'] \
                                             for b in stats['Polling Differences']], stats['Polling Differences'].index)

        stats['Winner Names'] = WinnerNames(stats['Polling Sum Positive Percentages'])
        stats['Winner Percs'] = WinnerPercs(stats['Polling Sum Positive Percentages'])[::-1] # came out backwards
        stats['Winner Polls Before'] = GetPollsStats(PollingBeforeDrop, stats['name'], stats['Winner Names'])
        stats['Winner Polls After'] = GetPollsStats(PollingAfterDrop, stats['name'], stats['Winner Names'])
        stats['Winner Polls Diff'] = GetPollsStats(PollingDiff, stats['name'], stats['Winner Names'])

        statList.append(stats)
    return statList