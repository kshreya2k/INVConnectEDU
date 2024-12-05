
from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Function to generate recommendations
def generate_recommendation(income, savings_goal, risk_level):
    if risk_level == "low":
        recommendation = "Consider investing in government bonds or low-risk mutual funds."
    elif risk_level == "medium":
        recommendation = "Diversify your portfolio with index funds and ETFs."
    else:
        recommendation = "Explore high-growth stocks or cryptocurrency investments."
    return recommendation

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get user input
    name = request.form['name']
    income = float(request.form['income'])
    savings_goal = float(request.form['savings_goal'])
    risk_level = request.form['risk_level']
    
    # Generate recommendation
    recommendation = generate_recommendation(income, savings_goal, risk_level)
    
    # Create a bar chart visualization
    data = {'Savings Goal': savings_goal, 'Income': income}
    df = pd.DataFrame(data.items(), columns=['Category', 'Amount'])
    plt.figure(figsize=(6, 4))
    plt.bar(df['Category'], df['Amount'], color=['#0056b3', '#80c6ff'])
    plt.title('Income vs. Savings Goal', fontsize=14)
    plt.xlabel('Category', fontsize=12)
    plt.ylabel('Amount', fontsize=12)
    plt.tight_layout()

    # Save the plot to static folder
    plot_path = 'static/images/plot.png'
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    plt.savefig(plot_path)
    plt.close()

    return render_template(
        'result.html',
        name=name,
        recommendation=recommendation,
        plot_url=f'/{plot_path}'
    )

if __name__ == "__main__":
    app.run(debug=True)
