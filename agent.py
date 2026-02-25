"""
LangChain Agent for Titanic Dataset Analysis
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from typing import Dict, Any, Tuple, Optional, Callable
import re

from data_loader import load_titanic_data

# Set visualization style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

class TitanicAnalyzer:
    """Analyzer class for Titanic dataset"""
    
    def __init__(self):
        self.df = load_titanic_data()
        self.fig = None
    
    def get_data_summary(self) -> str:
        """Get summary statistics of the dataset"""
        summary = f"""
Titanic Dataset Summary:
- Total Passengers: {len(self.df)}
- Columns: {', '.join(self.df.columns)}
- Survival Rate: {self.df['Survived'].mean()*100:.2f}%
"""
        return summary
    
    def analyze_gender(self) -> str:
        """Analyze gender distribution"""
        total = len(self.df)
        male_count = len(self.df[self.df['Sex'] == 'male'])
        female_count = len(self.df[self.df['Sex'] == 'female'])
        male_pct = (male_count / total) * 100
        female_pct = (female_count / total) * 100
        
        return f"""Gender Distribution:
- Male: {male_count} ({male_pct:.2f}%)
- Female: {female_count} ({female_pct:.2f}%)
"""
    
    def analyze_age(self) -> Tuple[str, Optional[str]]:
        """Analyze age statistics"""
        age_stats = self.df['Age'].describe()
        result = f"""Age Statistics:
- Mean Age: {age_stats['mean']:.2f} years
- Median Age: {self.df['Age'].median():.2f} years
- Min Age: {age_stats['min']:.2f} years
- Max Age: {age_stats['max']:.2f} years
- Std Dev: {age_stats['std']:.2f}
"""
        return result, None
    
    def analyze_fare(self) -> str:
        """Analyze ticket fare statistics"""
        fare_stats = self.df['Fare'].describe()
        return f"""Ticket Fare Statistics:
- Mean Fare: ${fare_stats['mean']:.2f}
- Median Fare: ${self.df['Fare'].median():.2f}
- Min Fare: ${fare_stats['min']:.2f}
- Max Fare: ${fare_stats['max']:.2f}
- Std Dev: ${fare_stats['std']:.2f}
"""
    
    def analyze_embarkation(self) -> str:
        """Analyze embarkation ports"""
        embark_counts = self.df['Embarked'].value_counts()
        total = len(self.df.dropna(subset=['Embarked']))
        
        result = "Embarkation Port Distribution:\n"
        for port, count in embark_counts.items():
            pct = (count / total) * 100
            port_name = {'S': 'Southampton', 'C': 'Cherbourg', 'Q': 'Queenstown'}.get(port, port)
            result += f"- {port_name} ({port}): {count} passengers ({pct:.2f}%)\n"
        
        return result
    
    def analyze_survival(self) -> str:
        """Analyze survival rates"""
        survival_by_sex = self.df.groupby('Sex')['Survived'].mean() * 100
        survival_by_class = self.df.groupby('Pclass')['Survived'].mean() * 100
        
        result = "Survival Analysis:\n"
        result += f"- Overall Survival Rate: {self.df['Survived'].mean()*100:.2f}%\n\n"
        result += "By Sex:\n"
        for sex, rate in survival_by_sex.items():
            result += f"  - {sex.capitalize()}: {rate:.2f}%\n"
        
        result += "\nBy Class:\n"
        for pclass, rate in survival_by_class.items():
            result += f"  - Class {pclass}: {rate:.2f}%\n"
        
        return result
    
    # Visualization methods
    def plot_age_histogram(self) -> str:
        """Create age histogram"""
        self.fig, ax = plt.subplots(figsize=(10, 6))
        self.df['Age'].dropna().hist(bins=30, ax=ax, edgecolor='black', alpha=0.7)
        ax.set_xlabel('Age', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.set_title('Distribution of Passenger Ages', fontsize=14, fontweight='bold')
        plt.tight_layout()
        return self._fig_to_base64()
    
    def plot_gender_pie(self) -> str:
        """Create gender pie chart"""
        self.fig, ax = plt.subplots(figsize=(8, 8))
        gender_counts = self.df['Sex'].value_counts()
        colors = ['#FF6B6B', '#4ECDC4']
        ax.pie(gender_counts.values, labels=gender_counts.index, autopct='%1.1f%%', 
               colors=colors, explode=(0.05, 0), startangle=90)
        ax.set_title('Gender Distribution', fontsize=14, fontweight='bold')
        plt.tight_layout()
        return self._fig_to_base64()
    
    def plot_embarkation_bar(self) -> str:
        """Create embarkation bar chart"""
        self.fig, ax = plt.subplots(figsize=(10, 6))
        embark_counts = self.df['Embarked'].value_counts()
        port_names = {'S': 'Southampton', 'C': 'Cherbourg', 'Q': 'Queenstown'}
        labels = [port_names.get(p, p) for p in embark_counts.index]
        colors = ['#3498db', '#e74c3c', '#2ecc71']
        bars = ax.bar(labels, embark_counts.values, color=colors, edgecolor='black')
        ax.set_xlabel('Port', fontsize=12)
        ax.set_ylabel('Number of Passengers', fontsize=12)
        ax.set_title('Passengers by Embarkation Port', fontsize=14, fontweight='bold')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom', fontsize=11)
        
        plt.tight_layout()
        return self._fig_to_base64()
    
    def plot_fare_histogram(self) -> str:
        """Create fare histogram"""
        self.fig, ax = plt.subplots(figsize=(10, 6))
        self.df['Fare'].hist(bins=30, ax=ax, edgecolor='black', alpha=0.7, color='#9b59b6')
        ax.set_xlabel('Fare ($)', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.set_title('Distribution of Ticket Fares', fontsize=14, fontweight='bold')
        plt.tight_layout()
        return self._fig_to_base64()
    
    def plot_survival_by_class(self) -> str:
        """Create survival by class bar chart"""
        self.fig, ax = plt.subplots(figsize=(10, 6))
        survival_by_class = self.df.groupby('Pclass')['Survived'].mean() * 100
        colors = ['#e74c3c', '#f39c12', '#27ae60']
        bars = ax.bar([f'Class {c}' for c in survival_by_class.index], 
                     survival_by_class.values, color=colors, edgecolor='black')
        ax.set_xlabel('Passenger Class', fontsize=12)
        ax.set_ylabel('Survival Rate (%)', fontsize=12)
        ax.set_title('Survival Rate by Passenger Class', fontsize=14, fontweight='bold')
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%', ha='center', va='bottom', fontsize=11)
        
        plt.tight_layout()
        return self._fig_to_base64()
    
    def _fig_to_base64(self) -> str:
        """Convert matplotlib figure to base64 string"""
        buffer = io.BytesIO()
        self.fig.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close(self.fig)
        return image_base64


class TitanicAgent:
    """Main agent for handling Titanic dataset queries"""
    
    def __init__(self):
        self.analyzer = TitanicAnalyzer()
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a natural language query and return response with optional visualization.
        
        Args:
            query: User's natural language question
            
        Returns:
            Dict containing 'answer' and optional 'visualization' (base64 encoded)
        """
        query_lower = query.lower()
        response = {"answer": "", "visualization": None}
        
        # Determine which analysis to perform based on keywords
        if any(word in query_lower for word in ['male', 'male percentage', 'male passengers', 'gender', 'sex']):
            if 'percentage' in query_lower or 'what' in query_lower:
                response["answer"] = self.analyzer.analyze_gender()
            
            if 'show' in query_lower or 'pie' in query_lower or 'chart' in query_lower or 'visual' in query_lower:
                response["visualization"] = self.analyzer.plot_gender_pie()
        
        elif any(word in query_lower for word in ['age', 'ages', 'old']):
            if 'average' in query_lower or 'mean' in query_lower or 'median' in query_lower:
                response["answer"] = self.analyzer.analyze_age()[0]
            elif 'histogram' in query_lower or 'show' in query_lower or 'distribution' in query_lower:
                response["answer"] = "Here is the histogram of passenger ages:"
                response["visualization"] = self.analyzer.plot_age_histogram()
            else:
                response["answer"] = self.analyzer.analyze_age()[0]
        
        elif any(word in query_lower for word in ['fare', 'ticket', 'price', 'cost']):
            if 'average' in query_lower or 'mean' in query_lower or 'what' in query_lower:
                response["answer"] = self.analyzer.analyze_fare()
            elif 'histogram' in query_lower or 'show' in query_lower or 'distribution' in query_lower:
                response["answer"] = "Here is the histogram of ticket fares:"
                response["visualization"] = self.analyzer.plot_fare_histogram()
            else:
                response["answer"] = self.analyzer.analyze_fare()
        
        elif any(word in query_lower for word in ['embark', 'port', 'board', 'from']):
            if 'how many' in query_lower or 'count' in query_lower or 'each' in query_lower:
                response["answer"] = self.analyzer.analyze_embarkation()
            
            if 'show' in query_lower or 'bar' in query_lower or 'chart' in query_lower or 'visual' in query_lower:
                response["visualization"] = self.analyzer.plot_embarkation_bar()
        
        elif any(word in query_lower for word in ['surviv', 'died', 'dead']):
            response["answer"] = self.analyzer.analyze_survival()
            
            if 'show' in query_lower or 'chart' in query_lower or 'class' in query_lower:
                response["visualization"] = self.analyzer.plot_survival_by_class()
        
        elif 'summary' in query_lower or 'overview' in query_lower or 'info' in query_lower:
            response["answer"] = self.analyzer.get_data_summary()
        
        else:
            # Default to summary if query not recognized
            response["answer"] = f"I can help you analyze the Titanic dataset! Try asking about:\n"
            response["answer"] += "- Gender distribution (e.g., 'What percentage were male?')\n"
            response["answer"] += "- Age analysis (e.g., 'Show me a histogram of ages')\n"
            response["answer"] += "- Ticket fares (e.g., 'What was the average fare?')\n"
            response["answer"] += "- Embarkation ports (e.g., 'How many from each port?')\n"
            response["answer"] += f"\nCurrent dataset has {len(self.analyzer.df)} passengers."
        
        return response


# Test the agent
if __name__ == "__main__":
    agent = TitanicAgent()
    
    # Test queries
    test_queries = [
        "What percentage of passengers were male on the Titanic?",
        "Show me a histogram of passenger ages",
        "What was the average ticket fare?",
        "How many passengers embarked from each port?"
    ]
    
    for q in test_queries:
        print(f"\nQuery: {q}")
        result = agent.process_query(q)
        print(f"Answer: {result['answer'][:200]}...")
        print(f"Has visualization: {result['visualization'] is not None}")
