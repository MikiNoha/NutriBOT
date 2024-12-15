import openai
from config import Config

def generate_meal_plan(ingredients, budget):
    """Generate a meal plan using GPT-4o Mini."""
    # Set the API key
    openai.api_key = Config.OPENAI_API_KEY

    # Define the prompt
    prompt = f"""
    Create a 4-day meal plan for 2 people using these ingredients:
    {ingredients}

    The budget is {budget} CZK per day. Include detailed recipes for each meal (breakfast, lunch, dinner) and a shopping list for all the required ingredients.
    """

    try:
        # Call the GPT-4o Mini API
        response = openai.ChatCompletion.create(
            model="gpt-4-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates meal plans and shopping lists."},
                {"role": "user", "content": prompt}
            ]
        )
        # Extract and return the response content
        return response['choices'][0]['message']['content']
    except openai.error.OpenAIError as e:
        return f"Error: {str(e)}"
