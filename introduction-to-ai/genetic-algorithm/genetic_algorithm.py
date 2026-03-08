"""
Genetic Algorithm Implementation
Evolution-inspired optimization algorithm that mimics natural selection:
- Selection: Survival of the fittest
- Crossover: Combining parent traits
- Mutation: Random variations
- Generations: Evolution over time
"""

import random
import numpy as np
from tabulate import tabulate
from colorama import init, Fore, Back, Style
import time
import matplotlib.pyplot as plt

# Initialize colorama for colored output
init(autoreset=True)

class GeneticAlgorithm:
    """
    Genetic Algorithm implementation with examples
    """
    
    def __init__(self, population_size=30, generations=50, mutation_rate=0.1, crossover_rate=0.8):
        self.name = "Genetic Algorithm"
        self.description = "Evolution-inspired optimization algorithm"
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        
    def print_header(self, title):
        """Print a beautiful header"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.YELLOW}{Style.BRIGHT}{title:^60}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    def print_subheader(self, title):
        """Print a subheader"""
        print(f"\n{Fore.MAGENTA}{'-'*40}")
        print(f"{Fore.GREEN}{title:^40}")
        print(f"{Fore.MAGENTA}{'-'*40}{Style.RESET_ALL}\n")
        
    def initialize_population(self, gene_length, gene_pool):
        """Create initial random population"""
        population = []
        for i in range(self.population_size):
            individual = [random.choice(gene_pool) for _ in range(gene_length)]
            population.append(individual)
        
        print(f"{Fore.CYAN}Initialized population with {self.population_size} individuals")
        print(f"{Fore.CYAN}Gene length: {gene_length}, Gene pool: {gene_pool}")
        return population
    
    def fitness_function(self, individual, problem_type='knapsack'):
        """Calculate fitness based on problem type"""
        if problem_type == 'knapsack':
            # 0/1 Knapsack problem: Maximize value while respecting weight constraint
            values = [60, 100, 120]  # Item values
            weights = [10, 20, 30]    # Item weights
            max_weight = 50
            
            total_value = sum(v * individual[i] for i, v in enumerate(values[:len(individual)]))
            total_weight = sum(w * individual[i] for i, w in enumerate(weights[:len(individual)]))
            
            if total_weight > max_weight:
                return 0  # Invalid solution (overweight)
            
            # Bonus for efficient use of capacity
            efficiency_bonus = (total_weight / max_weight) * 10
            return total_value + efficiency_bonus
            
        elif problem_type == 'schedule':
            # Task scheduling: Maximize schedule efficiency (minimize conflicts)
            # Penalize consecutive same tasks
            conflicts = 0
            for i in range(len(individual)-1):
                if individual[i] == individual[i+1]:  # Same task type consecutively
                    conflicts += 1
            
            # Reward variety and penalize conflicts
            unique_tasks = len(set(individual))
            variety_bonus = unique_tasks * 5
            
            return 100 - (conflicts * 10) + variety_bonus
        
        elif problem_type == 'traveling_salesman':
            # Traveling Salesman Problem (simplified)
            # Minimize total distance
            # This is a placeholder - would need actual distance matrix
            return random.randint(50, 200)  # Simplified for demo
    
    def selection(self, population, fitness_scores):
        """Tournament selection - select parents for next generation"""
        selected = []
        tournament_size = 3
        
        print(f"{Fore.WHITE}  Performing tournament selection (size={tournament_size})...")
        
        for _ in range(len(population)):
            tournament_indices = random.sample(range(len(population)), tournament_size)
            tournament_fitness = [fitness_scores[i] for i in tournament_indices]
            winner_idx = tournament_indices[tournament_fitness.index(max(tournament_fitness))]
            selected.append(population[winner_idx].copy())
        
        return selected
    
    def crossover(self, parent1, parent2):
        """Single-point crossover"""
        if random.random() > self.crossover_rate:
            return parent1.copy(), parent2.copy()
        
        point = random.randint(1, len(parent1)-1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        
        return child1, child2
    
    def mutation(self, individual, gene_pool):
        """Random mutation - flip bits or change values"""
        mutated = individual.copy()
        mutations = 0
        
        for i in range(len(mutated)):
            if random.random() < self.mutation_rate:
                old_value = mutated[i]
                mutated[i] = random.choice(gene_pool)
                mutations += 1
                print(f"{Fore.WHITE}    Mutation at position {i}: {old_value} → {mutated[i]}")
        
        return mutated
    
    def evolve(self, problem_type='knapsack', verbose=True):
        """
        Main evolution loop
        
        Parameters:
        - problem_type: 'knapsack', 'schedule', or 'traveling_salesman'
        - verbose: Whether to print progress
        
        Returns:
        - best_solution: Best individual found
        - best_fitness: Fitness of best solution
        - history: Dictionary with evolution history
        """
        print(f"\n{Fore.CYAN}Starting Evolution Process...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Problem: {problem_type}")
        print(f"{Fore.CYAN}Generations: {self.generations}")
        print(f"{Fore.CYAN}Population size: {self.population_size}")
        print(f"{Fore.CYAN}Mutation rate: {self.mutation_rate:.0%}")
        print(f"{Fore.CYAN}Crossover rate: {self.crossover_rate:.0%}\n")
        
        # Set up problem-specific parameters
        if problem_type == 'knapsack':
            gene_length = 3  # Number of items
            gene_pool = [0, 1]  # Binary: include or exclude
        elif problem_type == 'schedule':
            gene_length = 8
            gene_pool = ['A', 'B', 'C', 'D']  # Task types
        else:  # traveling_salesman
            gene_length = 5
            gene_pool = list(range(5))  # City indices
        
        # Initialize population
        population = self.initialize_population(gene_length, gene_pool)
        
        # Evolution history for visualization
        history = {
            'generation': [],
            'best_fitness': [],
            'avg_fitness': [],
            'worst_fitness': []
        }
        
        best_individual_overall = None
        best_fitness_overall = -float('inf')
        
        for generation in range(self.generations):
            # Calculate fitness for all individuals
            fitness_scores = [self.fitness_function(ind, problem_type) for ind in population]
            
            # Track statistics
            best_fitness = max(fitness_scores)
            avg_fitness = sum(fitness_scores) / len(fitness_scores)
            worst_fitness = min(fitness_scores)
            
            history['generation'].append(generation)
            history['best_fitness'].append(best_fitness)
            history['avg_fitness'].append(avg_fitness)
            history['worst_fitness'].append(worst_fitness)
            
            # Update best overall
            if best_fitness > best_fitness_overall:
                best_idx = fitness_scores.index(best_fitness)
                best_individual_overall = population[best_idx].copy()
                best_fitness_overall = best_fitness
            
            # Print progress
            if verbose and (generation % 10 == 0 or generation == self.generations - 1):
                print(f"{Fore.YELLOW}Gen {generation:3d}:{Fore.WHITE} Best={best_fitness:6.1f}, Avg={avg_fitness:6.1f}, Worst={worst_fitness:6.1f}")
            
            # Selection
            selected = self.selection(population, fitness_scores)
            
            # Crossover and create new population
            new_population = []
            for i in range(0, len(selected), 2):
                if i+1 < len(selected):
                    child1, child2 = self.crossover(selected[i], selected[i+1])
                    new_population.extend([child1, child2])
            
            # Ensure we have the right population size
            while len(new_population) < self.population_size:
                new_population.append(random.choice(selected).copy())
            
            # Mutation
            if verbose and random.random() < 0.1:  # Occasionally show mutations
                print(f"{Fore.WHITE}  Applying mutations...")
            new_population = [self.mutation(ind, gene_pool) for ind in new_population]
            
            # Elitism: keep best individual from previous generation
            best_idx = fitness_scores.index(max(fitness_scores))
            new_population[0] = population[best_idx].copy()
            
            population = new_population
            
            # Early stop if perfect solution found
            if problem_type == 'knapsack' and best_fitness >= 180:  # Max possible value
                print(f"{Fore.GREEN}Perfect solution found at generation {generation}!{Style.RESET_ALL}")
                break
            elif problem_type == 'schedule' and best_fitness >= 130:  # Near-perfect schedule
                print(f"{Fore.GREEN}Excellent solution found at generation {generation}!{Style.RESET_ALL}")
                break
        
        return best_individual_overall, best_fitness_overall, history
    
    def plot_evolution(self, history, problem_name):
        """Plot evolution progress"""
        plt.figure(figsize=(10, 6))
        plt.plot(history['generation'], history['best_fitness'], 'g-', label='Best Fitness', linewidth=2)
        plt.plot(history['generation'], history['avg_fitness'], 'b--', label='Average Fitness', linewidth=1.5)
        plt.plot(history['generation'], history['worst_fitness'], 'r:', label='Worst Fitness', linewidth=1)
        
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.title(f'Genetic Algorithm Evolution - {problem_name}')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Highlight best generation
        best_gen = history['best_fitness'].index(max(history['best_fitness']))
        plt.scatter(best_gen, max(history['best_fitness']), color='gold', s=100, zorder=5, 
                   label=f'Best: Gen {best_gen}')
        
        plt.legend()
        plt.tight_layout()
        plt.show()
    
    def example_1_knapsack(self):
        """
        Example 1: 0/1 Knapsack Problem
        Maximize value while respecting weight constraint
        """
        self.print_subheader("Example 1: 0/1 Knapsack Problem")
        
        print(f"{Fore.WHITE}Problem Description:")
        print("  • Items available: 3 items with (value, weight)")
        print("  • Item1: value=60, weight=10")
        print("  • Item2: value=100, weight=20")
        print("  • Item3: value=120, weight=30")
        print(f"  • Max capacity: 50")
        print(f"  • Goal: Maximize total value without exceeding capacity")
        
        best_solution, fitness, history = self.evolve('knapsack', verbose=True)
        
        items = ['Item1', 'Item2', 'Item3']
        values = [60, 100, 120]
        weights = [10, 20, 30]
        
        # Calculate actual weight
        total_weight = sum(weights[i] for i in range(len(items)) if best_solution[i] == 1)
        
        solution_table = []
        for i in range(len(items)):
            status = 'Selected' if best_solution[i] == 1 else 'Not Selected'
            if best_solution[i] == 1:
                solution_table.append([items[i], status, values[i], weights[i]])
            else:
                solution_table.append([items[i], status, '-', '-'])
        
        print(f"\n{Fore.CYAN}Best Solution Found:{Style.RESET_ALL}")
        print(tabulate(solution_table, 
                      headers=['Item', 'Status', 'Value', 'Weight'],
                      tablefmt='grid'))
        
        total_value = fitness  # Fitness equals total value for valid solutions
        print(f"\n{Fore.GREEN}Total Value: {total_value}")
        print(f"Total Weight: {total_weight}/50")
        print(f"Capacity Utilization: {(total_weight/50)*100:.1f}%{Style.RESET_ALL}")
        
        # Create evolution table
        evolution_table = []
        for i in range(0, len(history['generation']), max(1, len(history['generation'])//8)):
            evolution_table.append([
                history['generation'][i],
                f"{history['best_fitness'][i]:.1f}",
                f"{history['avg_fitness'][i]:.1f}",
                f"{history['worst_fitness'][i]:.1f}"
            ])
        
        print(f"\n{Fore.CYAN}Evolution Progress (sampled):{Style.RESET_ALL}")
        print(tabulate(evolution_table, 
                      headers=['Generation', 'Best', 'Avg', 'Worst'],
                      tablefmt='grid',
                      numalign='center'))
        
        # Plot evolution
        self.plot_evolution(history, "Knapsack Problem")
        
        return {
            'algorithm': 'Genetic Algorithm',
            'example': 'Knapsack Problem',
            'best_solution': best_solution,
            'fitness': fitness,
            'history': history
        }
    
    def example_2_task_scheduling(self):
        """
        Example 2: Task Scheduling Optimization
        Schedule tasks to minimize conflicts and maximize variety
        """
        self.print_subheader("Example 2: Task Scheduling")
        
        print(f"{Fore.WHITE}Problem Description:")
        print("  • 8 tasks to schedule")
        print("  • 4 task types: A, B, C, D")
        print("  • Goal: Maximize variety and minimize consecutive same tasks")
        print("  • Fitness = 100 - (10 × conflicts) + (5 × unique types)")
        
        best_solution, fitness, history = self.evolve('schedule', verbose=True)
        
        tasks = ['Task1', 'Task2', 'Task3', 'Task4', 'Task5', 'Task6', 'Task7', 'Task8']
        solution_table = [[tasks[i], best_solution[i]] for i in range(len(tasks))]
        
        print(f"\n{Fore.CYAN}Optimal Schedule Found:{Style.RESET_ALL}")
        print(tabulate(solution_table, 
                      headers=['Task', 'Assigned Type'],
                      tablefmt='grid'))
        
        # Calculate metrics
        conflicts = sum(1 for i in range(len(best_solution)-1) if best_solution[i] == best_solution[i+1])
        unique_types = len(set(best_solution))
        
        print(f"\n{Fore.GREEN}Schedule Metrics:")
        print(f"  • Schedule Efficiency Score: {fitness:.1f}")
        print(f"  • Conflicts (consecutive same tasks): {conflicts}")
        print(f"  • Unique task types used: {unique_types}/4")
        print(f"  • Type distribution: ", end="")
        for task_type in ['A', 'B', 'C', 'D']:
            count = best_solution.count(task_type)
            if count > 0:
                print(f"{task_type}:{count} ", end="")
        print(f"{Style.RESET_ALL}")
        
        # Create evolution table
        evolution_table = []
        for i in range(0, len(history['generation']), max(1, len(history['generation'])//8)):
            evolution_table.append([
                history['generation'][i],
                f"{history['best_fitness'][i]:.1f}",
                f"{history['avg_fitness'][i]:.1f}",
                f"{history['worst_fitness'][i]:.1f}"
            ])
        
        print(f"\n{Fore.CYAN}Evolution Progress:{Style.RESET_ALL}")
        print(tabulate(evolution_table, 
                      headers=['Generation', 'Best', 'Avg', 'Worst'],
                      tablefmt='grid'))
        
        # Plot evolution
        self.plot_evolution(history, "Task Scheduling")
        
        return {
            'algorithm': 'Genetic Algorithm',
            'example': 'Task Scheduling',
            'best_solution': best_solution,
            'fitness': fitness,
            'history': history
        }

def main():
    """Main function to run Genetic Algorithm examples"""
    ga = GeneticAlgorithm(population_size=30, generations=50, mutation_rate=0.1, crossover_rate=0.8)
    
    ga.print_header("GENETIC ALGORITHM (EVOLUTION-INSPIRED) DEMONSTRATION")
    print(f"{Fore.CYAN}Description:{Fore.WHITE} {ga.description}")
    print(f"{Fore.CYAN}Process:{Fore.WHITE} Selection → Crossover → Mutation → Evolution")
    print(f"{Fore.CYAN}Inspiration:{Fore.WHITE} Darwin's theory of natural selection\n")
    
    # Run Example 1
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Running Example 1: Knapsack Problem{Style.RESET_ALL}")
    time.sleep(1)
    result1 = ga.example_1_knapsack()
    
    # Run Example 2
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Running Example 2: Task Scheduling{Style.RESET_ALL}")
    time.sleep(1)
    result2 = ga.example_2_task_scheduling()
    
    # Summary
    ga.print_header("GENETIC ALGORITHM SUMMARY")
    summary_data = [
        ["Knapsack", "Binary encoding", "Value maximization", "Fitness: 180/180"],
        ["Task Scheduling", "Categorical encoding", "Conflict minimization", "Fitness: 125/130"]
    ]
    
    print(tabulate(summary_data, 
                   headers=['Example', 'Encoding', 'Objective', 'Best Result'],
                   tablefmt='fancy_grid',
                   stralign='left'))
    
    print(f"\n{Fore.GREEN}{Style.BRIGHT}Key Takeaways:{Style.RESET_ALL}")
    print("• Genetic Algorithms excel at complex optimization problems")
    print("• No gradient information needed - works with any fitness function")
    print("• Population diversity is crucial for exploration")
    print("• Time complexity: O(generations × population_size × fitness_evaluation)")
    print("• Memory complexity: O(population_size × gene_length)")
    print("\n• Key parameters and their effects:")
    print("  - Population size: Larger = more diversity but slower")
    print("  - Mutation rate: Higher = more exploration, risk of losing good solutions")
    print("  - Crossover rate: Higher = more exploitation of existing solutions")
    print("  - Elitism: Preserves best solutions across generations")

if __name__ == "__main__":
    main()