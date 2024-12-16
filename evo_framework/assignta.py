import pandas as pd
import numpy as np

sections_df = pd.read_csv('data/sections.csv',header=None)
tas_df = pd.read_csv('data/tas.csv',header = None, skiprows=1)

# for each ta (row in tests1-3 (solution)), check the number of sections they are assigned to and compare this to the 
# maximum number of lab sections they can ta in (column 3 in tas.csv)
def overallocation(solution, tas_df):
    penalty = 0
    for row in range(len(tas_df)):
        if row < len(solution):
            solution_row_sum = np.sum(solution[row])
        else:
            solution_row_sum = 0
        
        max_assigned = tas_df.loc[row,'max_assigned']
        
        amount_overallocated = solution_row_sum - max_assigned

        if amount_overallocated > 0:
            penalty += amount_overallocated
    
    return penalty

      

# for each ta (row in tests1-3 (solution)), check the number of times that they are assigned to multiple sections with the same
# daytime (column 3 in sections.csv)
def conflicts(solution, sections_df):
    daytimes = sections_df.iloc[:, 2].values
    penalty = 0
    for i in range(solution.shape[0]):
        assigned_sections = np.where(solution[i, :] == 1)[0]
        assigned_daytimes = daytimes[assigned_sections]
        if len(assigned_daytimes) > len(np.unique(assigned_daytimes)):
            penalty += 1  
    return penalty


# for each section, check the minimum number of tas (column 7 of sections.csv). compare it to the total number of tas 
# assigned to it, the penalty is the sum of the amount of tas down each section is. 

def undersupport(solution, sections_df):
    min_tas = sections_df.iloc[:,6].values
    penalty = 0
    for i in range (solution.shape[1]):
        assigned_tas = np.sum(solution[:,i])
        if assigned_tas < int(min_tas[i]):
            penalty += min_tas[i] - assigned_tas

    return penalty


# for each ta (row in tas.csv), count the number of times a ta is assigned to a section they are unwilling to support (this means there 
# is a U for the column labeled that number section in tas.csv). 
def unwilling1(solution, tas_df):
    penalty = 0
    for i in range(solution.shape[0]):
        for j in range(solution.shape[1]):
            if solution[i,j] == 1 and tas_df.iloc[i+1,j+2] == 'U':
                penalty += 1
    return penalty


def unwilling(solution, tas_df):
    penalty = 0
    num_tas, num_sections = solution.shape

    for i in range(num_tas):
        for j in range(num_sections):
            if tas_df.iloc[i, j + 3] == 'U':  
                if solution[i, j] == 1:
                    penalty += 1

    return penalty



# for each ta, count the number of times they are assigned to a section W but not P


def unpreferred(solution, tas_df):
    penalty = 0
    num_tas, num_sections = solution.shape

    for i in range(num_tas):
        for j in range(num_sections):
            willing_col = j + 3  
            preferred_col = j + 3  

            if willing_col < tas_df.shape[1]:
                if solution[i, j] == 1 and tas_df.iloc[i, willing_col] == 'W' and tas_df.iloc[i, willing_col] != 'P':
                    penalty += 1

    return penalty
