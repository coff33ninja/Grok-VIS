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


def play_trivia(category=None):
    """Play a trivia game with questions from OpenTrivia API."""
    try:
        # Category mapping (simplified for demo, full list at https://opentdb.com/api_config.php)
        categories = {
            "general": 9,
            "history": 23,
            "science": 17,
            "movies": 11,
            "music": 12,
        }

        category_id = (
            categories.get(category.lower())
            if category and category.lower() in categories
            else None
        )
        url = f"https://opentdb.com/api.php?amount=1&type=multiple{'&category=' + str(category_id) if category_id else ''}"
        response = requests.get(url)
        trivia_data = response.json()

        if trivia_data["response_code"] == 0 and trivia_data["results"]:
            question_data = trivia_data["results"][0]
            question = question_data["question"]
            correct_answer = question_data["correct_answer"]
            options = question_data["incorrect_answers"] + [correct_answer]
            random.shuffle(options)

            speak(f"Here's your trivia question: {question}")
            time.sleep(1)
            speak("Here are your options:")
            for i, option in enumerate(options, 1):
                speak(f"{i}. {option}")
            time.sleep(1)
            speak(f"The correct answer is: {correct_answer}")
        else:
            # Fallback question
            fallback = {
                "question": "What is the capital of France?",
                "options": ["Paris", "London", "Berlin", "Madrid"],
                "correct": "Paris",
            }
            speak(f"Here's a trivia question: {fallback['question']}")
            for i, option in enumerate(fallback["options"], 1):
                speak(f"{i}. {option}")
            time.sleep(1)
            speak(f"The correct answer is: {fallback['correct']}")
    except Exception as e:
        logging.error(f"Trivia API Error: {e}")
        speak("Sorry, I couldn't fetch a trivia question right now.")


def play_rock_paper_scissors():
    """Play a game of rock-paper-scissors."""
    try:
        choices = ["rock", "paper", "scissors"]
        ai_choice = random.choice(choices)

        speak("Let's play rock-paper-scissors! I'll make my choice... ready?")
        time.sleep(1)
        speak(f"I chose {ai_choice}. Imagine you picked one too!")
        speak(
            "For fun, if you picked rock, paper beats it; if paper, scissors beats it; if scissors, rock beats it."
        )
        speak("Did I win, or did you? Let's call it a tie for now!")
    except Exception as e:
        logging.error(f"Rock-Paper-Scissors Error: {e}")
        speak("Oops, something went wrong with our game!")


def tell_story(genre=None):
    """Tell a short public domain story using Gutendex API."""
    try:
        # Simplified genre mapping for demo (Gutendex uses subjects)
        url = "https://gutendex.com/books?mime_type=text/plain&sort=popular"
        response = requests.get(url)
        story_data = response.json()

        if story_data["results"]:
            book = random.choice(story_data["results"])
            title = book["title"]
            author = book["authors"][0]["name"] if book["authors"] else "Unknown Author"
            # Simulate fetching a short excerpt (API doesn't provide full text directly)
            speak(f"Here's a story: {title} by {author}.")
            speak(
                "Once upon a time, in a land far away, there was a curious adventurer... Imagine the tale unfolding!"
            )
        else:
            speak(
                "Here's a short tale: Once, a clever fox tricked a crow into dropping its cheese. The end!"
            )
    except Exception as e:
        logging.error(f"Storytelling API Error: {e}")
        speak(
            "Sorry, I couldn't fetch a story right now. How about imagining your own adventure?"
        )


def recommend_book(genre=None):
    """Recommend a book based on genre using Open Library API."""
    try:
        genres = {
            "fiction": "fiction",
            "mystery": "mystery",
            "science fiction": "science+fiction",
            "fantasy": "fantasy",
            "history": "history",
        }

        search_term = (
            genres.get(genre.lower())
            if genre and genre.lower() in genres
            else "fiction"
        )
        url = f"https://openlibrary.org/search.json?q={search_term}&limit=5"
        response = requests.get(url)
        book_data = response.json()

        if book_data["docs"]:
            book = random.choice(book_data["docs"])
            title = book.get("title", "Unknown Title")
            author = book.get("author_name", ["Unknown Author"])[0]
            speak(f"I recommend: {title} by {author}. Enjoy your reading!")
        else:
            speak(
                "I suggest: 'To Kill a Mockingbird' by Harper Lee. A classic for any reader!"
            )
    except Exception as e:
        logging.error(f"Book Recommendation API Error: {e}")
        speak("Sorry, I couldn't find a book recommendation right now.")


def tell_riddle():
    """Tell a riddle and reveal the answer."""
    try:
        url = "https://riddles-api.vercel.app/random"
        response = requests.get(url)
        riddle_data = response.json()

        if "riddle" in riddle_data and "answer" in riddle_data:
            riddle = riddle_data["riddle"]
            answer = riddle_data["answer"]
            speak(f"Here's a riddle: {riddle}")
            time.sleep(2)  # Pause for thinking
            speak(f"The answer is: {answer}")
        else:
            fallback = {
                "riddle": "I speak without a mouth and hear without ears. What am I?",
                "answer": "An echo",
            }
            speak(f"Here's a riddle: {fallback['riddle']}")
            time.sleep(2)
            speak(f"The answer is: {fallback['answer']}")
    except Exception as e:
        logging.error(f"Riddle API Error: {e}")
        speak("Sorry, my riddle box is empty right now!")
