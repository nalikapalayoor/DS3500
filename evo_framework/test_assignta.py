import pytest
import pandas as pd
import numpy as np
import sys
from assignta import overallocation, conflicts, undersupport, unwilling, unpreferred

tas_df = pd.read_csv('data/tas.csv')
sections_df = pd.read_csv('data/sections.csv')

def test_overallocation():
    for test_num, expected in zip([1, 2, 3], [37, 41, 23]):
        solution_df = pd.read_csv(f'data/test{test_num}.csv',header=None)  
        solution = solution_df.to_numpy()  
        result = overallocation(solution, tas_df)
        assert result == expected

def test_conflicts():
    for test_num, expected in zip([1, 2, 3], [8, 5, 2]):
        solution_df = pd.read_csv(f'data/test{test_num}.csv',header=None)  
        solution = solution_df.to_numpy()  
        result = conflicts(solution, sections_df)
        assert result == expected

def test_undersupport():
    for test_num, expected in zip([1, 2, 3], [1, 0, 7]):
        solution_df = pd.read_csv(f'data/test{test_num}.csv',header=None)
        solution = solution_df.to_numpy()  
        result = undersupport(solution, sections_df)
        assert result == expected

def test_unwilling():
    for test_num, expected in zip([1, 2, 3], [53, 58, 43]):
        solution_df = pd.read_csv(f'data/test{test_num}.csv',header=None)  
        solution = solution_df.to_numpy()  
        result = unwilling(solution, tas_df)
        assert result == expected

def test_unpreferred():
    for test_num, expected in zip([1, 2, 3], [15, 19, 10]):
        solution_df = pd.read_csv(f'data/test{test_num}.csv',header=None)  
        solution = solution_df.to_numpy()  
        result = unpreferred(solution, tas_df)
        assert result == expected

# I got this code from chat gpt because I didnt know how to save the test results to a txt file
with open('test_results.txt', 'w') as f:
    sys.stdout = f
    pytest.main(['test_assignta.py'])
    sys.stdout = sys.__stdout__