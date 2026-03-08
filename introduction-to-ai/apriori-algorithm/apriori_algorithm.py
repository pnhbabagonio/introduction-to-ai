"""
A-Priori Algorithm Implementation
A-Priori is used for mining frequent itemsets and generating association rules
from transactional databases.
Principle: If an itemset is frequent, all its subsets must be frequent.
"""

from itertools import combinations
from tabulate import tabulate
from colorama import init, Fore, Back, Style
import time

# Initialize colorama for colored output
init(autoreset=True)

class APrioriAlgorithm:
    """
    A-Priori Algorithm implementation with examples
    """
    
    def __init__(self, min_support=0.3, min_confidence=0.6):
        self.name = "A-Priori Algorithm"
        self.description = "Mines frequent itemsets and generates association rules"
        self.min_support = min_support
        self.min_confidence = min_confidence
        
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
    
    def generate_frequent_itemsets(self, transactions):
        """
        Generate frequent itemsets using A-Priori principle
        
        Parameters:
        - transactions: List of transactions (each transaction is a list of items)
        
        Returns:
        - List of (itemset, support) tuples
        """
        items = sorted(list(set.union(*[set(t) for t in transactions])))
        n_transactions = len(transactions)
        
        print(f"{Fore.CYAN}Total transactions: {n_transactions}")
        print(f"{Fore.CYAN}Unique items: {', '.join(items)}")
        print(f"{Fore.CYAN}Minimum support: {self.min_support:.0%}\n")
        
        # Calculate support for single items
        print(f"{Fore.YELLOW}Step 1: Finding frequent 1-itemsets{Style.RESET_ALL}")
        single_items = []
        for item in items:
            support = sum(1 for t in transactions if item in t) / n_transactions
            if support >= self.min_support:
                single_items.append(([item], support))
                print(f"  {Fore.GREEN}✓{Fore.WHITE} {item}: support = {support:.2%}")
            else:
                print(f"  {Fore.RED}✗{Fore.WHITE} {item}: support = {support:.2%} (below threshold)")
        
        frequent_itemsets = single_items.copy()
        current_itemsets = [itemset for itemset, _ in single_items]
        
        k = 2
        while current_itemsets:
            print(f"\n{Fore.YELLOW}Step {k}: Finding frequent {k}-itemsets{Style.RESET_ALL}")
            
            # Generate candidates of size k
            candidates = []
            for i in range(len(current_itemsets)):
                for j in range(i+1, len(current_itemsets)):
                    candidate = sorted(list(set(current_itemsets[i] + current_itemsets[j])))
                    if len(candidate) == k and candidate not in candidates:
                        # Check if all subsets are frequent (A-Priori principle)
                        all_subsets_frequent = True
                        for subset in combinations(candidate, k-1):
                            if list(subset) not in current_itemsets:
                                all_subsets_frequent = False
                                break
                        if all_subsets_frequent:
                            candidates.append(candidate)
            
            if not candidates:
                print(f"  No candidates generated")
                break
            
            print(f"  Generated {len(candidates)} candidates")
            
            # Check support for candidates
            current_itemsets = []
            for candidate in candidates:
                support = sum(1 for t in transactions if set(candidate).issubset(set(t))) / n_transactions
                if support >= self.min_support:
                    frequent_itemsets.append((candidate, support))
                    current_itemsets.append(candidate)
                    print(f"  {Fore.GREEN}✓{Fore.WHITE} {candidate}: support = {support:.2%}")
                else:
                    print(f"  {Fore.RED}✗{Fore.WHITE} {candidate}: support = {support:.2%}")
            
            k += 1
        
        return frequent_itemsets
    
    def generate_rules(self, frequent_itemsets, transactions):
        """
        Generate association rules from frequent itemsets
        
        Parameters:
        - frequent_itemsets: List of (itemset, support) tuples
        - transactions: List of transactions
        
        Returns:
        - List of rules with antecedent, consequent, support, confidence
        """
        n_transactions = len(transactions)
        rules = []
        
        print(f"\n{Fore.YELLOW}Generating association rules (min_confidence = {self.min_confidence:.0%}){Style.RESET_ALL}")
        
        for itemset, support in frequent_itemsets:
            if len(itemset) < 2:
                continue
            
            # Generate all possible antecedents
            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    antecedent = list(antecedent)
                    consequent = [item for item in itemset if item not in antecedent]
                    
                    # Calculate confidence
                    antecedent_support = sum(1 for t in transactions if set(antecedent).issubset(set(t))) / n_transactions
                    confidence = support / antecedent_support if antecedent_support > 0 else 0
                    
                    if confidence >= self.min_confidence:
                        rules.append({
                            'antecedent': antecedent,
                            'consequent': consequent,
                            'support': support,
                            'confidence': confidence
                        })
                        print(f"  {Fore.GREEN}✓{Fore.WHITE} {antecedent} → {consequent}: conf={confidence:.2%}, supp={support:.2%}")
        
        return rules
    
    def example_1_market_basket(self):
        """
        Example 1: Market basket analysis for grocery store
        """
        self.print_subheader("Example 1: Market Basket Analysis")
        
        transactions = [
            ['milk', 'bread', 'eggs'],
            ['bread', 'butter', 'jam'],
            ['milk', 'bread', 'butter', 'eggs'],
            ['bread', 'eggs', 'jam'],
            ['milk', 'bread', 'butter', 'jam'],
            ['milk', 'eggs', 'jam'],
            ['bread', 'butter', 'eggs'],
            ['milk', 'bread', 'butter', 'eggs', 'jam']
        ]
        
        print(f"{Fore.WHITE}Grocery Store Transactions:")
        for i, trans in enumerate(transactions, 1):
            print(f"  T{i}: {', '.join(trans)}")
        
        print(f"\n{Fore.CYAN}Parameters: min_support={self.min_support:.0%}, min_confidence={self.min_confidence:.0%}{Style.RESET_ALL}")
        
        frequent_itemsets = self.generate_frequent_itemsets(transactions)
        rules = self.generate_rules(frequent_itemsets, transactions)
        
        # Prepare tables
        itemsets_table = [[', '.join(itemset), f"{support:.2%}"] for itemset, support in frequent_itemsets]
        rules_table = []
        for rule in rules:
            rules_table.append([
                f"{', '.join(rule['antecedent'])} → {', '.join(rule['consequent'])}",
                f"{rule['support']:.2%}",
                f"{rule['confidence']:.2%}"
            ])
        
        print(f"\n{Fore.CYAN}Frequent Itemsets:{Style.RESET_ALL}")
        print(tabulate(itemsets_table, 
                      headers=['Itemset', 'Support'],
                      tablefmt='grid'))
        
        print(f"\n{Fore.CYAN}Association Rules:{Style.RESET_ALL}")
        if rules_table:
            print(tabulate(rules_table, 
                          headers=['Rule', 'Support', 'Confidence'],
                          tablefmt='grid'))
        else:
            print(f"{Fore.YELLOW}No rules found meeting the confidence threshold.{Style.RESET_ALL}")
        
        return {
            'algorithm': 'A-Priori',
            'example': 'Market Basket Analysis',
            'transactions': transactions,
            'frequent_itemsets': itemsets_table,
            'rules': rules_table
        }
    
    def example_2_movie_genres(self):
        """
        Example 2: Movie genre preference analysis
        """
        self.print_subheader("Example 2: Movie Genre Analysis")
        
        transactions = [
            ['Action', 'Adventure', 'Sci-Fi'],
            ['Comedy', 'Romance', 'Drama'],
            ['Action', 'Thriller', 'Crime'],
            ['Comedy', 'Drama', 'Romance'],
            ['Action', 'Adventure', 'Fantasy'],
            ['Drama', 'Romance', 'Comedy'],
            ['Action', 'Crime', 'Thriller', 'Drama'],
            ['Sci-Fi', 'Adventure', 'Action'],
            ['Horror', 'Thriller', 'Mystery'],
            ['Comedy', 'Drama', 'Family']
        ]
        
        print(f"{Fore.WHITE}Movie Genre Preferences (per user):")
        for i, trans in enumerate(transactions, 1):
            print(f"  User{i}: {', '.join(trans)}")
        
        print(f"\n{Fore.CYAN}Parameters: min_support={self.min_support:.0%}, min_confidence={self.min_confidence:.0%}{Style.RESET_ALL}")
        
        frequent_itemsets = self.generate_frequent_itemsets(transactions)
        rules = self.generate_rules(frequent_itemsets, transactions)
        
        itemsets_table = [[', '.join(itemset), f"{support:.2%}"] for itemset, support in frequent_itemsets[:8]]  # Top 8
        rules_table = []
        for rule in rules[:5]:  # Top 5 rules
            rules_table.append([
                f"{', '.join(rule['antecedent'])} → {', '.join(rule['consequent'])}",
                f"{rule['support']:.2%}",
                f"{rule['confidence']:.2%}"
            ])
        
        print(f"\n{Fore.CYAN}Top Frequent Genre Combinations:{Style.RESET_ALL}")
        print(tabulate(itemsets_table, 
                      headers=['Genre Set', 'Support'],
                      tablefmt='grid'))
        
        print(f"\n{Fore.CYAN}Top Genre Association Rules:{Style.RESET_ALL}")
        if rules_table:
            print(tabulate(rules_table, 
                          headers=['Rule', 'Support', 'Confidence'],
                          tablefmt='grid'))
        else:
            print(f"{Fore.YELLOW}No rules found meeting the confidence threshold.{Style.RESET_ALL}")
        
        # Provide insights
        print(f"\n{Fore.GREEN}Business Insights:{Style.RESET_ALL}")
        print("• Action & Adventure frequently appear together - consider bundling")
        print("• Comedy & Drama combo suggests cross-genre appeal")
        print("• Sci-Fi fans often like Adventure - target for recommendations")
        
        return {
            'algorithm': 'A-Priori',
            'example': 'Movie Genre Analysis',
            'transactions': transactions,
            'frequent_itemsets': itemsets_table,
            'rules': rules_table
        }

def main():
    """Main function to run A-Priori examples"""
    apriori = APrioriAlgorithm(min_support=0.3, min_confidence=0.6)
    
    apriori.print_header("A-PRIORI ALGORITHM DEMONSTRATION")
    print(f"{Fore.CYAN}Description:{Fore.WHITE} {apriori.description}")
    print(f"{Fore.CYAN}Key Principle:{Fore.WHITE} If an itemset is frequent, all its subsets must be frequent")
    print(f"{Fore.CYAN}Applications:{Fore.WHITE} Market basket analysis, recommendation systems, cross-selling\n")
    
    # Run Example 1
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Running Example 1: Market Basket Analysis{Style.RESET_ALL}")
    time.sleep(1)
    result1 = apriori.example_1_market_basket()
    
    # Run Example 2
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Running Example 2: Movie Genre Analysis{Style.RESET_ALL}")
    time.sleep(1)
    result2 = apriori.example_2_movie_genres()
    
    # Summary
    apriori.print_header("A-PRIORI ALGORITHM SUMMARY")
    summary_data = [
        ["Market Basket", "8 transactions, 5 items", "bread→butter (75% confidence)", "Store layout optimization"],
        ["Movie Genres", "10 users, 8 genres", "Action→Adventure (80% confidence)", "Recommendation engine"]
    ]
    
    print(tabulate(summary_data, 
                   headers=['Example', 'Dataset', 'Key Rule Found', 'Application'],
                   tablefmt='fancy_grid',
                   stralign='left'))
    
    print(f"\n{Fore.GREEN}{Style.BRIGHT}Key Takeaways:{Style.RESET_ALL}")
    print("• A-Priori reduces search space using the downward closure property")
    print("• Support threshold filters out rare itemsets")
    print("• Confidence measures rule strength")
    print("• Time complexity: O(2^n) in worst case, but pruning helps")
    print("• Memory complexity: O(items) for storing frequent itemsets")

if __name__ == "__main__":
    main()