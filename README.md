# Anki AI Language Vocab Helper

This is an Anki add-on for Language vocabulary flashcards. It asks the learner to translate an example sentence (context hint) for each card during review. This helps connect a word with how it's used. The example sentences are created on-the-fly and shown on the card during review, but the card itself is not edited - the changes are only in memory.

The add-on requires flashcards in a specific format:

*   **Front:** Word or expression in your source language (e.g. English if you're learning a new language as an English speaker)
*   **Back:** Translation in target language (the language you are trying to learn)

## Features

*   **Question:** An example sentence in the source language using the word in context is generated automatically on the question side of the card.
*   **Answer:** The target-language translation using the word being practiced is shown on the answer side.
*   **Seamless Integration:** Connects directly to the Anki review process. Card are not being edited.
*   **Caching:** Generated sentences are stored in memory during the session. The example sentence stays consistent when the card is flipped or reviewed again in the same session.
*   **Powered by Gemini:** Uses `gemini-2.0-flash` for high-quality examples.
*   **Language-agnostic:** Set your desired source and target languages in the config file. 

## Planned Features

*   **Persistent Storage:** Ability to save context hints to storage to reuse sentences across sessions and reduce LLM requests (with an opt-out for fresh generation). However, it is intentionally not planned to edit the cards themselves, so that the add-on's data stays segregated, backwards-compatible, and idempotent.
*   **Review UI:**
    *   Button to save the current sentence to storage.
    *   Button to generate a new sentence on demand.

## Setup

1.  Save the whole directory into your **Anki add-on folder**
2.  Replace the contents of the "api_key" file with your Google API key. You can create a free tier API key at https://aistudio.google.com/
3.  Set the source and target language in the "config.json" file. For example, if you're an English speaker and want to learn peninsular Spanish, you need to set "source_language" to "English" and "target_language" to "Spanish (peninsular)"
4.  **Restart** Anki.
