from openai import OpenAI
from config import Config
import logging
import os
from dotenv import load_dotenv

load_dotenv()
# Debug mode
DEBUG = True

# Valid models
VALID_MODELS = ["gpt-4o-mini", "gpt-3.5-turbo"]

# Set the OpenAI API key
# openai.api_key = Config.OPENAI_API_KEY
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if DEBUG:
    print(f"OpenAI API Key Loaded: {Config.OPENAI_API_KEY is not None}")


# response = client.chat.completions.create(
#     model="gpt-4o-mini",  # Replace with your desired model
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Tell me a fun fact about Python programming."}
#     ]
# )

def generate_meal_plan(ingredients, budget, model="gpt-4o-mini"):
    """
    Vytvoří plán jídel pomocí OpenAI ChatCompletion.
    :param ingredients: Seznam ingrediencí poskytnutých uživatelem.
    :param budget: Rozpočet na den (CZK).
    :param model: Model OpenAI, který se má použít (výchozí: gpt-4.0-mini).
    :return: Vygenerovaný plán jídel nebo chybová zpráva.
    """

    # Validate model
    if model not in VALID_MODELS:
        return f"Chyba: Neplatný model '{model}'. Platné modely jsou: {', '.join(VALID_MODELS)}."

    # Define the prompt
    prompt = f"""
    Vytvoř 4denní jídelní plán pro 2 osoby.
    Ingredience, které máme doma:
    {ingredients}
    U každého jídla rozepíšeš suroviny, které je třeba k vyhotovení jídla, a které je třeba nakoupit.

    Rozpočet je {budget} CZK na den. 
    """
    # prompt = "odpověz, že tu jsi a posloucháš"

    try:
        # Call the OpenAI API
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": """   Jsi nutriční asistent dvoučelnné domácnosti. 
                                                    Připravuješ jídelní plány v českém jazyce na základě parametrů, které od uživatele dostaneš. Jsi kulinářským expertem a dokážeš dané suroviny analyzovat a postavit na základě nich recepty.
                                                    recepty nemusí obsahovat pouze suroviny dodané uživatelem, jen je vhodné je občas do jídel zakomponovat, aby nebylo třeba vše kupovat.
                                                    Poté, co vymyslíš daný počet jídel, rozepíšeš suroviny, které je třeba k vyhotovení jídla, a které je třeba nakoupit. Zároveň vezmeš v potaz rozpočet, který k surovinám dosaneš."""},
                {"role": "user", "content": prompt}
            ]
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content

        
    except openai.APIConnectionError as e:
        logging.error(f"The server could not be reached: {e}")
        return "Chyba: Nepodařilo se připojit k serveru. Zkuste to prosím znovu později."

    except openai.RateLimitError as e:
        logging.error(f"A rate limit error occurred: {e}")
        return "Chyba: Překročen limit požadavků. Počkejte chvíli a zkuste to znovu."

    except openai.APIStatusError as e:
        logging.error(f"A non-200 status code was received: {e.status_code}, {e.response}")
        return f"Chyba: Server vrátil neočekávaný stav: {e.status_code}."

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return "Došlo k neočekávané chybě. Zkontrolujte vstupy a zkuste to znovu."
