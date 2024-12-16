# I used some of the code from class in this file

import random as rnd
import copy
import numpy as np
from functools import reduce
import time
import csv
import cProfile
from assignta import overallocation, conflicts, undersupport, unwilling, unpreferred

class Evo:
    def __init__(self, tas_df, sections_df):
        self.pop = {}  # evaluation --> solution
        self.fitness = {}  # name --> objective function
        self.agents = {}  # name --> (operator function, num_solutions_input)
        self.tas_df = tas_df
        self.sections_df = sections_df

    def add_fitness_criteria(self, name, f):
        """Register an objective with the environment."""
        self.fitness[name] = f

    def add_agent(self, name, op, k=1):
        """Register an agent with the environment."""
        self.agents[name] = (op, k)

    def add_solution(self, sol):
        """Add a solution to the population."""
        eval = tuple([(name, f(sol)) for name, f in self.fitness.items()])
        self.pop[eval] = sol

    def initialize_population(self, num_solutions=10):
        """Initialize the population with random solutions."""
        for _ in range(num_solutions):
            sol = self.random_assignment(None)
            self.add_solution(sol)

    def random_assignment(self, _):
        num_tas = self.tas_df.shape[0]
        num_sections = self.sections_df.shape[0]
        max_sections_per_ta = 2
        assignment = np.zeros((num_tas, num_sections), dtype=int)

        for i in range(num_tas):
            sections = rnd.sample(range(num_sections), min(max_sections_per_ta, num_sections))
            assignment[i, sections] = 1

        return assignment

    def get_random_solutions(self, k=1):
        """Pick k random solutions from the population."""
        if len(self.pop) == 0:
            return []
        else:
            solutions = tuple(self.pop.values())
            return [copy.deepcopy(rnd.choice(solutions)) for _ in range(k)]

    def run_agent(self, name):
        """Invoke a named agent on the population."""
        op, k = self.agents[name]
        picks = self.get_random_solutions(k)
        new_solution = op(picks)
        self.add_solution(new_solution)

    def dominates(self, p, q):
        """Determine if solution p dominates solution q."""
        pscores = np.array([score for name, score in p])
        qscores = np.array([score for name, score in q])
        score_diffs = qscores - pscores
        return min(score_diffs) >= 0 and max(score_diffs) > 0.0

    def reduce_nds(self, S, p):
        return S - {q for q in S if self.dominates(p, q)}

    def remove_dominated(self):
        """Remove dominated solutions from the population."""
        nds = reduce(self.reduce_nds, self.pop.keys(), self.pop.keys())
        self.pop = {k: self.pop[k] for k in nds}

    def get_best_solution(self):
        """Return the solution with the lowest total penalty."""
        best_eval = min(self.pop.keys(), key=lambda eval: sum(score for _, score in eval))
        return best_eval, self.pop[best_eval]

    def evolve(self, n=1, dom=100, status=1000, time_limit=300):
        """Run random agents n times."""
        agent_names = list(self.agents.keys())
        start_time = time.time()
        for i in range(n):
            if time.time() - start_time > time_limit:
                break

            pick = rnd.choice(agent_names)
            self.run_agent(pick)

            if i % dom == 0:
                self.remove_dominated()

            if i % status == 0:
                self.remove_dominated()

        self.remove_dominated()

    def save_pareto_summary(self, pareto_solutions, tas_df, sections_df, group_name="nalika"):
        with open("pareto_summary.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["groupname", "overallocation", "conflicts", "undersupport", "unwilling", "unpreferred"])
        
            for solution in pareto_solutions:
                overallocation_score = overallocation(solution, tas_df)
                conflicts_score = conflicts(solution, sections_df)
                undersupport_score = undersupport(solution, sections_df)
                unwilling_score = unwilling(solution, tas_df)
                unpreferred_score = unpreferred(solution, tas_df)
            
                writer.writerow([group_name, overallocation_score, conflicts_score, undersupport_score, unwilling_score, unpreferred_score])

    def __str__(self):
        rslt = ""
        for eval, sol in self.pop.items():
            rslt += str(eval) + ":\t" + str(sol) + "\n"
        return rslt


def profile_evolution(tas_df, sections_df):
    evo = Evo(tas_df, sections_df)

    # fitness criteria
    evo.add_fitness_criteria("overallocation", lambda sol: overallocation(sol, tas_df))
    evo.add_fitness_criteria("conflicts", lambda sol: conflicts(sol, sections_df))
    evo.add_fitness_criteria("undersupport", lambda sol: undersupport(sol, sections_df))
    evo.add_fitness_criteria("unwilling", lambda sol: unwilling(sol, tas_df))
    evo.add_fitness_criteria("unpreferred", lambda sol: unpreferred(sol, tas_df))

    # agents
    def mutate_solution(solutions):
        """Mutate a random solution"""
        sol = copy.deepcopy(solutions[0])
        num_tas, num_sections = sol.shape
        i, j = rnd.randint(0, num_tas - 1), rnd.randint(0, num_sections - 1)
        sol[i, j] = 1 - sol[i, j]  
        return sol

    def crossover_solution(solutions):
        """crossover on two solutions"""
        sol1, sol2 = solutions
        num_tas, num_sections = sol1.shape
        crossover_point = rnd.randint(0, num_sections - 1)
        new_sol = np.hstack((sol1[:, :crossover_point], sol2[:, crossover_point:]))
        return new_sol
    
    def swap_solution(solutions):
        """Swap two random assignments between two solutions"""
        sol1, sol2 = solutions
        num_tas, num_sections = sol1.shape
        i1, j1 = rnd.randint(0, num_tas - 1), rnd.randint(0, num_sections - 1)
        i2, j2 = rnd.randint(0, num_tas - 1), rnd.randint(0, num_sections - 1)
        
        sol1[i1, j1], sol2[i2, j2] = sol2[i2, j2], sol1[i1, j1]
        
        return sol1, sol2

    # Add agents 
    evo.add_agent("random", evo.random_assignment, k=0)  
    evo.add_agent("mutate", mutate_solution, k=1)   
    evo.add_agent("crossover", crossover_solution, k=2)  
    evo.add_agent("swap",swap_solution,k=3)

    # Initialize (random solutions)
    evo.initialize_population(num_solutions=10)

    start_time = time.time()

    evo.evolve(n=1000000, dom=50, status=200, time_limit=300)

    elapsed_time = time.time() - start_time
    print(f"Evolution process completed in {elapsed_time:.2f} seconds")

    # best solution found
    best_eval, best_solution = evo.get_best_solution()
    print("Best Solution:")
    print("Evaluation Scores:", best_eval)
    print("Solution Matrix:\n", best_solution)


    # Save Pareto 
    pareto_solutions = list(evo.pop.values())  
    evo.save_pareto_summary(pareto_solutions, tas_df, sections_df)


if __name__ == "__main__":
    import pandas as pd

    tas_df = pd.read_csv("data/tas.csv", header=0)
    sections_df = pd.read_csv("data/sections.csv", header=0)

    cProfile.run('profile_evolution(tas_df, sections_df)', 'evolution_profile.prof')

    import pstats
    from pstats import SortKey

    p = pstats.Stats('evolution_profile.prof')
    p.sort_stats(SortKey.TIME).print_stats(10)
