# Anki AI Spanish Vocab Helper

This is an Anki add-on for Spanish-English vocabulary flashcards. It asks the learner to translate an example sentence (context hint) for each card during review. This helps connect a word with how it's used. The example sentences are created on-the-fly.

The add-on requires flashcards in a specific format:

*   **Front:** English word or expression
*   **Back:** Spanish translation

## Features

*   **Question:** An English example sentence using the word in context is generated automatically on the question side of the card.
*   **Answer:** The Spanish translation using the word being practiced is shown on the answer side.
*   **Seamless Integration:** Connects directly to the Anki review process. No manual editing of notes is needed.
*   **Caching:** Generated sentences are stored during the session. The example sentence stays consistent when the card is flipped or reviewed again in the same session.
*   **Powered by Gemini:** Uses `gemini-2.0-flash` for high-quality examples.

## Planned Features

*   **Persistent Storage:** Ability to save context hints to storage to reuse sentences across sessions and reduce LLM requests (with an opt-out for fresh generation).
*   **Review UI:**
    *   Button to save the current sentence to storage.
    *   Button to generate a new sentence on demand.
*   **Expanded Language Support:** Support for languages beyond Spanish.

## Setup

1.  Save the whole directory in your **Anki add-on folder**.
2.  Put your Google API key in a file called `api_key` in the top directory of the add-on folder.
3.  **Restart** Anki.
