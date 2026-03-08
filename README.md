# 🧠 Algorithm Demonstration using Python
# PHILIP NEEL H. BABAGONIO
## 📚 Overview

This project demonstrates three fundamental algorithms in computer science, each representing different problem-solving approaches:

1. **A* Search Algorithm** - Pathfinding and graph traversal
2. **A-Priori Algorithm** - Frequent pattern mining and association rule learning  
3. **Genetic Algorithm** - Evolution-inspired optimization

Each algorithm is implemented with two practical examples, featuring beautiful console output with color coding, tabulated results, and detailed step-by-step execution.

---

## 🎯 Algorithms Explained

### 1. 🔍 A* Search Algorithm

**What it is:**
A* is an informed graph traversal and pathfinding algorithm that uses heuristics to find the shortest path between nodes. It combines the actual cost from the start node with an estimated cost to the goal.

**Formula:**
```
f(n) = g(n) + h(n)
```
- `g(n)`: Actual cost from start to node n
- `h(n)`: Heuristic estimated cost from node n to goal
- `f(n)`: Total estimated cost

**Key Characteristics:**
- Guarantees optimal path when heuristic is admissible (never overestimates)
- Uses priority queue for efficient node selection
- Time complexity: O(b^d) where b is branching factor, d is solution depth
- Space complexity: O(b^d) as it stores all generated nodes

**Examples Implemented:**

#### 🏙️ Example 1: City Navigation
- Finds shortest route between cities using road distances
- Uses straight-line distance as heuristic
- Demonstrates real-world GPS navigation concept

#### 🧩 Example 2: Maze Solving
- Navigates through a grid-based maze avoiding walls
- Uses Manhattan distance as heuristic
- Visualizes the path found through the maze

---

### 2. 📊 A-Priori Algorithm

**What it is:**
A-Priori is used for mining frequent itemsets and generating association rules from transactional databases. It's based on the principle that all subsets of a frequent itemset must also be frequent.

**Key Concepts:**
- **Support**: Frequency of itemset occurrence in transactions
- **Confidence**: Conditional probability of rule (how often rule is true)
- **Lift**: How much more likely consequent is given antecedent
- **A-Priori Principle**: Prunes infrequent candidate itemsets early

**Key Characteristics:**
- Reduces search space using downward closure property
- Time complexity: O(2^n) in worst case, but pruning helps significantly
- Memory complexity: O(items) for storing frequent itemsets
- Widely used in market basket analysis and recommendation systems

**Examples Implemented:**

#### 🛒 Example 1: Market Basket Analysis
- Analyzes grocery store transactions
- Finds patterns like "bread → butter" with high confidence
- Helps in store layout optimization and promotions

#### 🎬 Example 2: Movie Genre Analysis
- Analyzes user genre preferences
- Finds associations like "Action → Adventure"
- Used for recommendation engine development

---

### 3. 🧬 Genetic Algorithm (Evolution-Inspired)

**What it is:**
Genetic Algorithms mimic natural evolution to solve optimization problems. They maintain a population of solutions that evolve through selection, crossover, and mutation over generations.

**Evolutionary Process:**
```
1. INITIALIZATION → 2. SELECTION → 3. CROSSOVER → 4. MUTATION → 5. EVALUATION → (repeat)
```

**Key Components:**
- **Population**: Set of potential solutions
- **Fitness Function**: Measures solution quality
- **Selection**: Tournament selection (fittest individuals chosen)
- **Crossover**: Single-point crossover combines parent traits
- **Mutation**: Random changes to maintain diversity
- **Elitism**: Best solution preserved across generations

**Key Characteristics:**
- No gradient information needed - works with any fitness function
- Excellent for complex optimization problems
- Population diversity is crucial for exploration
- Time complexity: O(generations × population_size × fitness_evaluation)
- Memory complexity: O(population_size × gene_length)

**Examples Implemented:**

#### 🎒 Example 1: 0/1 Knapsack Problem
- Maximizes value while respecting weight constraint
- Items: Item1(60/10), Item2(100/20), Item3(120/30)
- Evolves to optimal selection (Items 2 and 3 = 220 value)

#### 📅 Example 2: Task Scheduling
- Schedules 8 tasks with 4 types (A, B, C, D)
- Maximizes variety and minimizes consecutive same tasks
- Fitness = 100 - (10 × conflicts) + (5 × unique types)

---

## 📁 Project Structure

```
introduction-to-ai/
├──astar-algorithm/
    ├── astar_algorithm.py          # A* Algorithm implementation
├──apriori-algorithm/              
    ├── apriori_algorithm.py        # A-Priori Algorithm implementation
├──genetic-algorithm/            
    ├── genetic_algorithm.py         # Genetic Algorithm implementation
│
├── requirements.txt             # Required Python packages
├── README.md                    # This file
└── screenshots/                    # Example outputs and screenshots
    ├── apriori
    ├── astar
    └── genetic
```

---

## ⚙️ Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/algorithm-demonstration.git
cd algorithm-demonstration
```

2. **Install required packages:**
```bash
pip install -r requirements.txt
```

**Requirements:**
```
numpy>=1.19.0
pandas>=1.2.0
tabulate>=0.8.9
matplotlib>=3.3.0
colorama>=0.4.4
```

---

## 🚀 Usage

Run each algorithm separately:

### For A* Algorithm:
```bash
python astar_algorithm.py
```

### For A-Priori Algorithm:
```bash
python apriori_algorithm.py
```

### For Genetic Algorithm:
```bash
python genetic_algorithm.py
```

Each script will display:
- Algorithm explanation and key concepts
- Step-by-step execution of examples
- Color-coded output for better visualization
- Tabulated results
- Summary and key takeaways

---

## 🎨 Features

### Visual Enhancements
- **Color-coded console output** using Colorama
- **Tabulated results** using Tabulate library
- **Progress indicators** for long-running operations
- **Evolution plots** for Genetic Algorithm (matplotlib)

### Interactive Elements
- Press Enter to continue between examples
- Real-time progress updates
- Step-by-step execution visualization

### Educational Value
- Clear algorithm explanations
- Practical real-world examples
- Performance characteristics discussion
- Key takeaways for each algorithm

---

## 📊 Sample Output

### A* Algorithm - City Navigation
```
A* SEARCH ALGORITHM DEMONSTRATION
============================================================

Example 1: City Navigation
----------------------------------------
Starting A* search from A to G...
Exploring node A with f=6.0, g=0.0
  Added neighbor B with f=8.0
  Added neighbor C with f=7.0
✓ Goal reached!

Results:
  Path found: A → C → D → F → G
  Total distance: 8 km
```

### A-Priori Algorithm - Market Basket
```
A-PRIORI ALGORITHM DEMONSTRATION
============================================================

Example 1: Market Basket Analysis
----------------------------------------
Step 1: Finding frequent 1-itemsets
  ✓ milk: support = 62.50%
  ✓ bread: support = 87.50%
  
Frequent Itemsets:
┌───────────────┬──────────┐
│ Itemset       │ Support  │
├───────────────┼──────────┤
│ bread         │ 87.50%   │
│ milk          │ 62.50%   │
│ bread, milk   │ 50.00%   │
└───────────────┴──────────┘
```

### Genetic Algorithm - Knapsack Problem
```
GENETIC ALGORITHM DEMONSTRATION
============================================================

Example 1: 0/1 Knapsack Problem
----------------------------------------
Starting Evolution Process...
Gen   0: Best= 120.0, Avg= 85.3, Worst=  60.0
Gen  10: Best= 180.0, Avg= 162.7, Worst= 120.0
✓ Perfect solution found at generation 12!

Best Solution Found:
┌─────────┬───────────────┬─────────┬──────────┐
│ Item    │ Status        │ Value   │ Weight   │
├─────────┼───────────────┼─────────┼──────────┤
│ Item1   │ Not Selected  │ -       │ -        │
│ Item2   │ Selected      │ 100     │ 20       │
│ Item3   │ Selected      │ 120     │ 30       │
└─────────┴───────────────┴─────────┴──────────┘
Total Value: 220
Total Weight: 50/50
```

---

## 🎯 Applications in Real World

| Algorithm | Real-World Applications |
|-----------|------------------------|
| **A*** | GPS navigation, Video game pathfinding, Robotics, Network routing |
| **A-Priori** | Market basket analysis, Recommendation systems, Cross-selling, Fraud detection |
| **Genetic Algorithm** | Resource optimization, Scheduling, Engineering design, Machine learning |

---

## 📈 Performance Summary

| Algorithm | Time Complexity | Space Complexity | Best Use Case |
|-----------|----------------|------------------|---------------|
| A* | O(b^d) | O(b^d) | Pathfinding with good heuristics |
| A-Priori | O(2^n) worst | O(items) | Pattern mining in transactions |
| Genetic | O(g×p×f) | O(p) | Complex optimization problems |

*where: b=branching factor, d=depth, n=items, g=generations, p=population size, f=fitness evaluation time*

---

## 🤝 Contributing

Contributions are welcome! Here are ways to contribute:

1. **Add new examples** for existing algorithms
2. **Implement additional algorithms** (Dijkstra, FP-Growth, Particle Swarm, etc.)
3. **Improve visualizations** with more plots and graphs
4. **Optimize code** for better performance
5. **Add unit tests** for reliability

---

## 📝 Introduction to AI Course

This is part of Introduction to AI curriculum. Used only for educational Purposes.

---

**⭐ If you find this project useful, please consider giving it a star!**

---

*Happy Coding!* 🚀
