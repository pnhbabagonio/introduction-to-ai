"""
A* Search Algorithm Implementation
A* is an informed graph traversal and pathfinding algorithm that uses heuristics
to find the shortest path between nodes.
Formula: f(n) = g(n) + h(n) where h(n) is the heuristic estimate
"""

import heapq
from tabulate import tabulate
from colorama import init, Fore, Back, Style
import time

# Initialize colorama for colored output
init(autoreset=True)

class AStarAlgorithm:
    """
    A* Search Algorithm implementation with examples
    """
    
    def __init__(self):
        self.name = "A* Search Algorithm"
        self.description = "Finds shortest path using heuristic-guided search"
        self.results = {}
        
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
        
    def search(self, graph, start, goal, heuristic):
        """
        A* search implementation
        
        Parameters:
        - graph: Dictionary representing the graph {node: {neighbor: cost}}
        - start: Starting node
        - goal: Goal node
        - heuristic: Dictionary of heuristic values {node: estimated_cost}
        
        Returns:
        - path: List of nodes in the path
        - cost: Total cost of the path
        - steps: List of search steps for visualization
        """
        # Priority queue: (f_score, counter, node, path)
        open_set = [(0, 0, start, [start])]
        counter = 1
        
        # Track visited nodes and their g_scores
        g_scores = {start: 0}
        visited = set()
        
        # For visualization
        steps = []
        
        print(f"{Fore.CYAN}Starting A* search from {start} to {goal}...{Style.RESET_ALL}")
        
        while open_set:
            f_score, _, current, path = heapq.heappop(open_set)
            
            steps.append({
                'current': current,
                'path': '→'.join(path),
                'g_score': g_scores[current],
                'f_score': f_score
            })
            
            print(f"{Fore.WHITE}Exploring node {Fore.YELLOW}{current}{Fore.WHITE} with f={f_score:.1f}, g={g_scores[current]:.1f}")
            
            if current == goal:
                print(f"{Fore.GREEN}✓ Goal reached!{Style.RESET_ALL}")
                return path, g_scores[current], steps
            
            if current in visited:
                continue
                
            visited.add(current)
            
            for neighbor, cost in graph[current].items():
                if neighbor in visited:
                    continue
                    
                tentative_g = g_scores[current] + cost
                
                if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                    g_scores[neighbor] = tentative_g
                    f_score = tentative_g + heuristic[neighbor]
                    new_path = path + [neighbor]
                    heapq.heappush(open_set, (f_score, counter, neighbor, new_path))
                    counter += 1
                    print(f"{Fore.WHITE}  Added neighbor {Fore.BLUE}{neighbor}{Fore.WHITE} with f={f_score:.1f}")
        
        print(f"{Fore.RED}✗ No path found!{Style.RESET_ALL}")
        return None, float('inf'), steps
    
    def example_1_city_navigation(self):
        """
        Example 1: Finding shortest path between cities
        Uses road distances and straight-line heuristics
        """
        self.print_subheader("Example 1: City Navigation")
        
        # Graph representing cities with distances (km)
        graph = {
            'A': {'B': 4, 'C': 2},
            'B': {'A': 4, 'D': 5, 'E': 3},
            'C': {'A': 2, 'D': 1, 'F': 7},
            'D': {'B': 5, 'C': 1, 'E': 2, 'F': 3},
            'E': {'B': 3, 'D': 2, 'G': 4},
            'F': {'C': 7, 'D': 3, 'G': 2},
            'G': {'E': 4, 'F': 2}
        }
        
        # Straight-line distance heuristic (simplified Euclidean estimates)
        heuristic = {
            'A': 6, 'B': 4, 'C': 5, 'D': 3, 'E': 2, 'F': 3, 'G': 0
        }
        
        start, goal = 'A', 'G'
        
        print(f"{Fore.WHITE}City Map: {Fore.YELLOW}{list(graph.keys())}")
        print(f"{Fore.WHITE}Starting City: {Fore.GREEN}{start}")
        print(f"{Fore.WHITE}Destination: {Fore.GREEN}{goal}")
        print(f"{Fore.WHITE}Heuristic values (straight-line estimates):")
        for city, h in heuristic.items():
            print(f"  {city}: {h} km")
        
        path, distance, steps = self.search(graph, start, goal, heuristic)
        
        if path:
            # Prepare results for tabulation
            steps_table = []
            for i, step in enumerate(steps):
                steps_table.append([i+1, step['current'], step['path'], f"{step['g_score']:.1f}", f"{step['f_score']:.1f}"])
            
            result = {
                'algorithm': 'A*',
                'example': 'City Navigation',
                'graph': graph,
                'start': start,
                'goal': goal,
                'path': path,
                'distance': distance,
                'steps': steps_table
            }
            
            print(f"\n{Fore.CYAN}Results:{Style.RESET_ALL}")
            print(f"  Path found: {Fore.GREEN}{' → '.join(path)}{Style.RESET_ALL}")
            print(f"  Total distance: {Fore.GREEN}{distance} km{Style.RESET_ALL}")
            
            print(f"\n{Fore.CYAN}Search Steps:{Style.RESET_ALL}")
            print(tabulate(steps_table[:8],  # Show first 8 steps
                          headers=['Step', 'Current', 'Path', 'g(n)', 'f(n)'],
                          tablefmt='grid',
                          numalign='center'))
            
            return result
        else:
            print(f"{Fore.RED}No path found!{Style.RESET_ALL}")
            return None
    
    def example_2_maze_solving(self):
        """
        Example 2: Solving a maze using Manhattan distance heuristic
        """
        self.print_subheader("Example 2: Maze Solving")
        
        # Simple maze represented as grid
        maze = [
            ['S', '.', '#', '.', '.'],
            ['#', '.', '#', '.', '#'],
            ['.', '.', '.', '#', '.'],
            ['#', '#', '.', '.', 'G'],
            ['.', '.', '#', '.', '.']
        ]
        
        print(f"{Fore.WHITE}Maze layout:")
        print(f"{Fore.GREEN}S{Fore.WHITE}=Start, {Fore.RED}G{Fore.WHITE}=Goal, {Fore.BLACK}#{Fore.WHITE}=Wall, .=Path")
        print(f"{Fore.YELLOW}" + "-" * 20)
        for row in maze:
            colored_row = []
            for cell in row:
                if cell == 'S':
                    colored_row.append(f"{Fore.GREEN}S{Style.RESET_ALL}")
                elif cell == 'G':
                    colored_row.append(f"{Fore.RED}G{Style.RESET_ALL}")
                elif cell == '#':
                    colored_row.append(f"{Fore.BLACK}#{Style.RESET_ALL}")
                else:
                    colored_row.append(f"{Fore.WHITE}.{Style.RESET_ALL}")
            print(' '.join(colored_row))
        print(f"{Fore.YELLOW}" + "-" * 20)
        
        # Convert maze to graph
        graph = {}
        heuristic = {}
        rows, cols = len(maze), len(maze[0])
        
        # Find start and goal
        start = goal = None
        for i in range(rows):
            for j in range(cols):
                if maze[i][j] == 'S':
                    start = f"{i},{j}"
                elif maze[i][j] == 'G':
                    goal = f"{i},{j}"
        
        # Build graph
        directions = [(0,1), (1,0), (0,-1), (-1,0)]
        for i in range(rows):
            for j in range(cols):
                if maze[i][j] != '#':
                    node = f"{i},{j}"
                    graph[node] = {}
                    for di, dj in directions:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < rows and 0 <= nj < cols and maze[ni][nj] != '#':
                            graph[node][f"{ni},{nj}"] = 1
        
        # Manhattan distance heuristic
        goal_i, goal_j = map(int, goal.split(','))
        for i in range(rows):
            for j in range(cols):
                node = f"{i},{j}"
                if node in graph:
                    heuristic[node] = abs(i - goal_i) + abs(j - goal_j)
        
        print(f"{Fore.WHITE}Start position: {Fore.GREEN}{start}")
        print(f"{Fore.WHITE}Goal position: {Fore.RED}{goal}")
        
        path, steps_count, steps = self.search(graph, start, goal, heuristic)
        
        if path:
            result = {
                'algorithm': 'A*',
                'example': 'Maze Solving',
                'maze': maze,
                'start': start,
                'goal': goal,
                'path': path,
                'steps': steps_count
            }
            
            print(f"\n{Fore.CYAN}Results:{Style.RESET_ALL}")
            print(f"  Path found: {Fore.GREEN}{' → '.join(path)}{Style.RESET_ALL}")
            print(f"  Steps taken: {Fore.GREEN}{steps_count}{Style.RESET_ALL}")
            
            # Visualize path on maze
            path_positions = [tuple(map(int, node.split(','))) for node in path]
            print(f"\n{Fore.CYAN}Path visualization (* = path):{Style.RESET_ALL}")
            for i in range(rows):
                row_str = ""
                for j in range(cols):
                    if (i, j) in path_positions:
                        if maze[i][j] == 'S':
                            row_str += f"{Fore.GREEN}S{Style.RESET_ALL} "
                        elif maze[i][j] == 'G':
                            row_str += f"{Fore.RED}G{Style.RESET_ALL} "
                        else:
                            row_str += f"{Fore.YELLOW}*{Style.RESET_ALL} "
                    else:
                        if maze[i][j] == '#':
                            row_str += f"{Fore.BLACK}#{Style.RESET_ALL} "
                        elif maze[i][j] == 'S':
                            row_str += f"{Fore.GREEN}S{Style.RESET_ALL} "
                        elif maze[i][j] == 'G':
                            row_str += f"{Fore.RED}G{Style.RESET_ALL} "
                        else:
                            row_str += f"{Fore.WHITE}.{Style.RESET_ALL} "
                print(row_str)
            
            return result
        else:
            print(f"{Fore.RED}No path found!{Style.RESET_ALL}")
            return None

def main():
    """Main function to run A* examples"""
    astar = AStarAlgorithm()
    
    astar.print_header("A* SEARCH ALGORITHM DEMONSTRATION")
    print(f"{Fore.CYAN}Description:{Fore.WHITE} {astar.description}")
    print(f"{Fore.CYAN}Formula:{Fore.WHITE} f(n) = g(n) + h(n)")
    print(f"{Fore.CYAN}Key concept:{Fore.WHITE} Uses heuristic to guide search towards goal\n")
    
    # Run Example 1
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Running Example 1: City Navigation{Style.RESET_ALL}")
    time.sleep(1)
    result1 = astar.example_1_city_navigation()
    
    # Run Example 2
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Running Example 2: Maze Solving{Style.RESET_ALL}")
    time.sleep(1)
    result2 = astar.example_2_maze_solving()
    
    # Summary
    astar.print_header("A* ALGORITHM SUMMARY")
    summary_data = [
        ["City Navigation", "Road network with distances", "Straight-line distance", "Optimal path found"],
        ["Maze Solving", "Grid with obstacles", "Manhattan distance", "Shortest path through maze"]
    ]
    
    print(tabulate(summary_data, 
                   headers=['Example', 'Problem Type', 'Heuristic Used', 'Result'],
                   tablefmt='fancy_grid',
                   stralign='left'))
    
    print(f"\n{Fore.GREEN}{Style.BRIGHT}Key Takeaways:{Style.RESET_ALL}")
    print("• A* guarantees optimal path when heuristic is admissible (never overestimates)")
    print("• Performance depends heavily on heuristic quality")
    print("• Time complexity: O(b^d) where b is branching factor, d is solution depth")
    print("• Space complexity: O(b^d) as it stores all generated nodes")

if __name__ == "__main__":
    main()