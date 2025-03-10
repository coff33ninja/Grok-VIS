"""
Knowledge and information functionality for GrokVIS.
Handles Wikipedia lookups, news, definitions, and translations.
"""
import logging
import requests
import wikipedia
import json
import re
from bs4 import BeautifulSoup
from datetime import datetime

# Import from core module
from grokvis.speech import speak

def get_wikipedia_summary(topic, sentences=2):
    """Get a summary of a topic from Wikipedia."""
    try:
        # Search for the topic
        search_results = wikipedia.search(topic)
        if not search_results:
            speak(f"I couldn't find any information about {topic} on Wikipedia.")
            return None
        
        # Get the page for the first result
        try:
            page = wikipedia.page(search_results[0])
        except wikipedia.DisambiguationError as e:
            # If there's a disambiguation page, take the first option
            page = wikipedia.page(e.options[0])
        
        # Get the summary
        summary = wikipedia.summary(page.title, sentences=sentences)
        
        # Clean up the summary
        summary = re.sub(r'\([^)]*\)', '', summary)  # Remove parenthetical content
        summary = re.sub(r'\s+', ' ', summary).strip()  # Remove extra whitespace
        
        speak(f"According to Wikipedia: {summary}")
        speak(f"The article is titled '{page.title}'. Would you like to know more?")
        return page.title
    except Exception as e:
        logging.error(f"Wikipedia Error: {e}")
        speak(f"Sorry, I had trouble finding information about {topic}.")
        return None

def get_news_headlines(country='us', category='general', count=5):
    """Get top news headlines from NewsAPI."""
    try:
        # Replace with your actual API key
        api_key = "YOUR_NEWSAPI_KEY"
        url = f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={api_key}"
        
        response = requests.get(url)
        news_data = response.json()
        
        if news_data['status'] != 'ok' or news_data['totalResults'] == 0:
            speak("Sorry, I couldn't fetch any news headlines right now.")
            return
        
        speak(f"Here are the top {min(count, len(news_data['articles']))} headlines:")
        
        for i, article in enumerate(news_data['articles'][:count]):
            headline = article['title']
            source = article['source']['name']
            speak(f"{i+1}. From {source}: {headline}")
            
        speak("Would you like me to read any of these articles in full?")
    except Exception as e:
        logging.error(f"News API Error: {e}")
        speak("Sorry, I couldn't fetch the news headlines.")

def get_word_definition(word):
    """Look up the definition of a word using the Free Dictionary API."""
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(url)
        
        if response.status_code == 404:
            speak(f"Sorry, I couldn't find a definition for '{word}'.")
            return
            
        data = response.json()
        
        if not data or not isinstance(data, list):
            speak(f"Sorry, I couldn't find a definition for '{word}'.")
            return
            
        entry = data[0]
        word = entry.get('word', word)
        phonetic = entry.get('phonetic', '')
        
        speak(f"The word is {word} {phonetic}")
        
        for i, meaning in enumerate(entry.get('meanings', [])[:3]):
            part_of_speech = meaning.get('partOfSpeech', '')
            definitions = meaning.get('definitions', [])
            
            if definitions:
                definition = definitions[0].get('definition', '')
                example = definitions[0].get('example', '')
                
                speak(f"As a {part_of_speech}: {definition}")
                
                if example:
                    speak(f"Example: {example}")
                    
            if i >= 2:  # Limit to 3 meanings
                break
    except Exception as e:
        logging.error(f"Dictionary API Error: {e}")
        speak(f"Sorry, I had trouble looking up the definition of '{word}'.")

def translate_text(text, target_language):
    """Translate text using the LibreTranslate API."""
    try:
        # Map common language names to language codes
        language_map = {
            'spanish': 'es',
            'french': 'fr',
            'german': 'de',
            'italian': 'it',
            'portuguese': 'pt',
            'russian': 'ru',
            'japanese': 'ja',
            'chinese': 'zh',
            'arabic': 'ar',
            'hindi': 'hi',
            'english': 'en'
        }
        
        # Get the language code
        lang_code = language_map.get(target_language.lower())
        if not lang_code:
            speak(f"Sorry, I don't support translation to {target_language} yet.")
            return
            
        # Use LibreTranslate API (no key required)
        url = "https://libretranslate.de/translate"
        
        payload = {
            "q": text,
            "source": "auto",
            "target": lang_code
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        translation_data = response.json()
        
        if 'translatedText' in translation_data:
            translated_text = translation_data['translatedText']
            speak(f"In {target_language}, '{text}' is: {translated_text}")
        else:
            speak("Sorry, I couldn't translate that text.")
    except Exception as e:
        logging.error(f"Translation API Error: {e}")
        speak("Sorry, I had trouble with the translation service.")