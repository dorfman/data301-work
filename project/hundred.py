def Equals100(polls, x=0):
    """If the polling data sum is less than 100, add remainder to 'Undecided'. 
       If it is greater, substract surplus from 'Undecided'. Huffpost Pollster's 
       data uses integers instead of floats.
       
    Parameters
    ----------
    polls : DataFrame
        Holds polling for each candidate grouped by dates.
    x : int
        Offset if polls not completely cleaned yet.
    """
    
    for p in range(len(polls[x:])):
        pollSum = sum(polls.iloc[p][x:].dropna())
        if pollSum != 100:
            polls.ix[p, 'Undecided'] += 100 - pollSum
        pollSum = sum(polls.iloc[p][x:].dropna())