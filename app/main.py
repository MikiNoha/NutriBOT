from flask import Flask, render_template, request, redirect, url_for
from utils import generate_meal_plan

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        ingredients = request.form.get("ingredients")
        budget = request.form.get("budget")

        # Validate inputs
        if not ingredients or not budget:
            return "Error: Please provide both ingredients and a budget."

        # Generate the meal plan
        meal_plan = generate_meal_plan(ingredients, budget)

        # Render the result page
        return render_template("result.html", meal_plan=meal_plan)

    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
