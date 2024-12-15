from flask import Flask, render_template, request
from utils import generate_meal_plan
import openai
from config import Config

# Initialize the Flask app
app = Flask(__name__)

# Load OpenAI API key
openai.api_key = Config.OPENAI_API_KEY

# Home route
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        ingredients = request.form.get("ingredients")
        budget = request.form.get("budget")

        # Simple validation
        if not ingredients or not budget:
            return "Error: Please provide ingredients and a budget."

        # Validate budget
        try:
            budget = float(budget)  # Ensure budget is numeric
            if budget <= 0:
                return "Error: Budget must be a positive number."
        except ValueError:
            return "Error: Budget must be a numeric value."

        # Generate the meal plan
        meal_plan = generate_meal_plan(ingredients, budget)
        print(meal_plan)

        # Render the result page with the meal plan
        return render_template("result.html", meal_plan=meal_plan)

    # Render the home page
    return render_template("home.html")

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
