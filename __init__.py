import sys
import os
from aqt import gui_hooks

# Add the 'libs' folder to the Python path before other imports
sys.path.append(os.path.join(os.path.dirname(__file__), "libs"))

from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`
api_file_path = os.path.join(os.path.dirname(__file__), "api_key")
os.environ["GOOGLE_API_KEY"] = open(api_file_path).read()

client = genai.Client()

last_generated_contexts = dict()


def get_gpt_sentence(en_expression, es_expression):
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=f"""
            Provide a Spanish sentence using the given expression below in a context, 
            followed by its English translation. Ignore all image or formatting text. 
            In case of many word forms, pick any. Format: 'Spanish sentence | English translation' 
            
            \n\n\nExpression: EN: {en_expression}, ES: {es_expression}"""
        )
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)} | Error: {str(e)}"
    

def render_english_sentence(sentence):
    return f"<div style='color:gray; font-size:0.8em; margin-top:20px;'>Context hint: {sentence}</div>"


def render_spanish_sentence(sentence):
    return f"<hr><div style='font-style:italic;'>{sentence}</div>"


def on_card_will_show(text, card, kind):
    global last_generated_contexts

    if kind.startswith("reviewQuestion"):
        if card.id in last_generated_contexts.keys():
            english_sent = last_generated_contexts[card.id]["en"]
        else:
            llm_output = get_gpt_sentence(card.note().fields[0], card.note().fields[1])
            spanish_sent, english_sent = [s.strip() for s in llm_output.split("|")[:2]]
            if not (spanish_sent.startswith("Error") and english_sent.startswith("Error")):
                last_generated_contexts[card.id] = {"en": english_sent, "es": spanish_sent}
        return text + render_english_sentence(english_sent)
    
    elif kind.startswith("reviewAnswer"):
        if card.id in last_generated_contexts.keys():
            spanish_sent = last_generated_contexts[card.id]["es"]
            english_sent = last_generated_contexts[card.id]["en"]
            # display front and back
            return text\
                .replace("<hr id=answer>", 
                         render_english_sentence(english_sent) + "<hr id=answer>") \
                            + render_spanish_sentence(spanish_sent)

    return text


gui_hooks.card_will_show.append(on_card_will_show)
