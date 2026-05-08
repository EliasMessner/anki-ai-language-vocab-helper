import sys
import os
from aqt import gui_hooks
from pathlib import Path
import json

# Add the 'libs' folder to the Python path before other imports
sys.path.append(os.path.join(os.path.dirname(__file__), "libs"))

from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`
api_file_path = os.path.join(os.path.dirname(__file__), "api_key")
config_file_path = os.path.join(os.path.dirname(__file__), "config.json")
prompt_file_path = os.path.join(os.path.dirname(__file__), "prompt")
os.environ["GOOGLE_API_KEY"] = open(api_file_path).read()

client = genai.Client()

last_generated_contexts = dict()


def get_gpt_sentence(source_language_expression, target_language_expression):
    config_properties = read_config_file()
    source_language = config_properties["source_language"]
    target_language = config_properties["target_language"]
    
    prompt = Path(prompt_file_path).read_text()\
        .replace("{source_language}", source_language)\
        .replace("{target_language}", target_language)\
        .replace("{source_language_expression}", source_language_expression)\
        .replace("{target_language_expression}", target_language_expression)
    
    try:    
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        if "RESOURCE_EXHAUSTED" in str(e):
            return "Error: API quota exhausted.|Error: API quota exhausted."
        return f"Error: {str(e)}|Error: {str(e)}"
    
def read_config_file():
    with open(config_file_path, 'r') as file:
        data = json.load(file)
    return data

def render_source_language_sentence(sentence):
    return f"<div style='color:gray; font-size:0.8em; margin-top:20px;'>{sentence}</div>"


def render_target_language_sentence(sentence):
    return f"<hr><div style='font-style:italic;'>{sentence}</div>"


def on_card_will_show(text, card, kind):
    global last_generated_contexts

    if kind.startswith("reviewQuestion"):
        if card.id in last_generated_contexts.keys():
            source_language_sent = last_generated_contexts[card.id]["source_lang_sentence"]
        else:
            llm_output = get_gpt_sentence(card.note().fields[0], card.note().fields[1])
            target_language_sent, source_language_sent = [s.strip() for s in llm_output.split("|")[:2]]
            if not (target_language_sent.startswith("Error") and source_language_sent.startswith("Error")):
                last_generated_contexts[card.id] = {"source_lang_sentence": source_language_sent, "target_lang_sentence": target_language_sent}
        return text + render_source_language_sentence(source_language_sent)
    
    elif kind.startswith("reviewAnswer"):
        if card.id in last_generated_contexts.keys():
            target_language_sent = last_generated_contexts[card.id]["target_lang_sentence"]
            source_language_sent = last_generated_contexts[card.id]["source_lang_sentence"]
            # display front and back
            return text\
                .replace("<hr id=answer>", 
                         render_source_language_sentence(source_language_sent) + "<hr id=answer>") \
                            + render_target_language_sentence(target_language_sent)

    return text


gui_hooks.card_will_show.append(on_card_will_show)
