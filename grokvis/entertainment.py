"""
Entertainment functionality for GrokVIS.
Handles jokes, music, movie information, and random facts.
"""
import logging
import requests
import random
import time
import json
import os
from datetime import datetime

# Import from core module
from grokvis.speech import speak
from grokvis.core import executor

def tell_joke():
    """Tell a random joke from the JokeAPI."""
    try:
        # Get a random joke from the JokeAPI
        url = "https://v2.jokeapi.dev/joke/Programming,Miscellaneous,Pun?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=twopart"
        response = requests.get(url)
        joke_data = response.json()
        
        if joke_data['error']:
            # Fallback to a built-in joke if the API fails
            jokes = [
                {"setup": "Why do programmers prefer dark mode?", "punchline": "Because light attracts bugs!"},
                {"setup": "Why did the developer go broke?", "punchline": "Because he used up all his cache!"},
                {"setup": "What's a computer's favorite snack?", "punchline": "Microchips!"},
                {"setup": "Why don't programmers like nature?", "punchline": "It has too many bugs and no debugging tool!"}
            ]
            joke = random.choice(jokes)
            setup = joke["setup"]
            punchline = joke["punchline"]
        else:
            setup = joke_data["setup"]
            punchline = joke_data["delivery"]
        
        speak(setup)
        time.sleep(1.5)  # Dramatic pause
        speak(punchline)
    except Exception as e:
        logging.error(f"Joke API Error: {e}")
        speak("Sorry, my joke generator is feeling a bit serious today.")

def play_music(genre=None):
    """Simulate playing music of a specific genre."""
    try:
        genres = {
            "rock": ["Queen", "Led Zeppelin", "AC/DC", "The Beatles"],
            "pop": ["Taylor Swift", "Ed Sheeran", "Ariana Grande", "Justin Bieber"],
            "jazz": ["Miles Davis", "John Coltrane", "Ella Fitzgerald", "Louis Armstrong"],
            "classical": ["Mozart", "Beethoven", "Bach", "Chopin"],
            "hip hop": ["Kendrick Lamar", "Drake", "Jay-Z", "Eminem"],
            "electronic": ["Daft Punk", "Deadmau5", "Calvin Harris", "Skrillex"]
        }
        
        if genre and genre.lower() in genres:
            artists = genres[genre.lower()]
            artist = random.choice(artists)
            speak(f"Playing {genre} music. Here's some {artist} for you.")
        else:
            # If no genre specified or not recognized, pick a random one
            genre = random.choice(list(genres.keys()))
            artist = random.choice(genres[genre])
            speak(f"Playing some {genre} music. How about {artist}?")
            
        # In a real implementation, this would connect to a music service API
        speak("🎵 Imagine your favorite song playing right now... 🎵")
    except Exception as e:
        logging.error(f"Music Error: {e}")
        speak("Sorry, I couldn't play music right now.")

def get_movie_listings(location="nearby"):
    """Get movie listings for theaters in the area."""
    try:
        # This would normally use a real movie API
        # For demonstration, we'll use mock data
        
        movies = [
            {"title": "The Matrix Resurrections", "rating": "PG-13", "showtime": "7:30 PM"},
            {"title": "Spider-Man: No Way Home", "rating": "PG-13", "showtime": "6:15 PM, 9:00 PM"},
            {"title": "Dune", "rating": "PG-13", "showtime": "5:45 PM, 8:30 PM"},
            {"title": "No Time to Die", "rating": "PG-13", "showtime": "7:00 PM"},
            {"title": "Eternals", "rating": "PG-13", "showtime": "6:30 PM, 9:30 PM"}
        ]
        
        speak(f"Here are some movies playing {location} today:")
        
        for movie in movies:
            speak(f"{movie['title']}, rated {movie['rating']}, showing at {movie['showtime']}.")
            
        speak("Would you like me to find tickets for any of these movies?")
    except Exception as e:
        logging.error(f"Movie Listings Error: {e}")
        speak("Sorry, I couldn't fetch movie listings right now.")

def share_random_fact():
    """Share a random interesting fact."""
    try:
        # Get a random fact from the uselessfacts API
        url = "https://uselessfacts.jsph.pl/random.json?language=en"
        response = requests.get(url)
        fact_data = response.json()
        
        if 'text' in fact_data:
            fact = fact_data['text']
            speak(f"Here's a random fact: {fact}")
        else:
            # Fallback to built-in facts if the API fails
            facts = [
                "A day on Venus is longer than a year on Venus.",
                "The shortest war in history was between Britain and Zanzibar in 1896. Zanzibar surrendered after 38 minutes.",
                "A group of flamingos is called a 'flamboyance'.",
                "The world's oldest known living tree is over 5,000 years old.",
                "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly good to eat."
            ]
            speak(f"Here's a random fact: {random.choice(facts)}")
    except Exception as e:
        logging.error(f"Random Fact API Error: {e}")
        speak("Sorry, my fact generator is taking a break right now.")