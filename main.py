import os
import datetime
import speech_recognition as sr
import pyttsx3
import threading
import time
import openai
from dotenv import load_dotenv
from elevenlabs import stream
from elevenlabs.client import ElevenLabs
from calendar_utility import add_outlook_event


# Load environment variables
load_dotenv()

# Now read them into variables
# ========= COnfigure OpenAI API Key =========
openai.api_key = os.environ.get("OPENAI_API_KEY")

ELClient = ElevenLabs(
    api_key= os.environ.get("ELEVENLABS_API_KEY"),
)


# ========= Initialize Text-to-Speech =========
engine = pyttsx3.init()

def speak(text, voice="Matilda"):
    """
    Use ElevenLabs to synthesize 'text' using the specified 'voice'.
    Then immediately play the audio.
    """
    try:
        # Generate the TTS audio
        audio_stream = ELClient.generate(
            text=text,
            stream=True, # Stream and play the audio as it's being generated
            voice=voice, # You can also specify 'stability' or 'similarity_boost' as needed
            model="eleven_multilingual_v2" # Or use 'eleven' for English only
        )
        # Play it directly
        stream(audio_stream)
    except Exception as e:
        print(f"Error using ElevenLabs TTS: {e}")
    

def listen_for_wake_phrase():
    """
    Continuously listen for the wake phrase "hey assistant".
    When heard, hand off to listen_for_command().
    """

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Listening for wake phrase...")

    with microphone as source:
        # Adjust for ambient noise to help with recognition accuracy
        recognizer.adjust_for_ambient_noise(source, duration=1)

    while True:
        try:
            # Open mic fresh every time we want to listen
            with microphone as source:
                # Add a phrase_time_limit or timeout
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)

            phrase = recognizer.recognize_google(audio).lower()
            print(f"Detected phrase: {phrase}")

            if "hey assistant" in phrase:
                speak("How can I help you?")
                print("Wake phrase detected.")
                listen_for_command()
        except sr.WaitTimeoutError:
            # No speech detected within the timout
            continue
        except sr.UnknownValueError:
            # Speec was not recognized (not clear or no speech)
            continue
        except Exception as e:
            print(f"Error: {e}")
            continue

def listen_for_command():
    """
    Listen for a single user command after the wake phrase is heard.
    """

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=8)
            command = recognizer.recognize_google(audio).lower()
            print(f"Recognized command: {command}")
            process_command(command)
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Please try again.")
        except sr.UnknownValueError:
            speak("I didn't catch that. Please repeat.")
        except Exception as e:
            speak(f"Error processing your command: {str(e)}")

def process_command(command):
    """
    Process the user command and either handle it directly or pass it to GPT
    """

    if "add a meeting" in command or "calendar" in command:
        speak("You want to manage your calendar. I'll help you with that soon!")
    elif "set a timer" in command:
        speak("You want to set a timer. I'll help you with that soon!")
    elif "what's the weather" in command:
        speak("I will be able to answer that soon")
    else:
        ask_gpt(command)

def ask_gpt(prompt):
    """
    Example usage of the OpenAI API's text completion endpoint.
    If you have access to GPT-4, you might switch to the ChatCompletion API.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )

        # Retrieve the assistant's reply
        answer = response.choices[0].message.content.strip()
        speak(answer)
        print(f"Assistant: {answer}")
    except Exception as e:
        speak("There was an error getting a response from the API.")
        print(f"Error with GPT API: {e}")

def handle_add_meeting_flow():
    """
    Ask the user for the meeting date/time and subject,
    then call add_outlook_event()
    """

    # Step 1: As for date/time
    speak("Sure, what date and time should I schedule the meeting?")
    user_datetime_text = listen_for_command()

    # Step 2: Parse the date/time from user speech
    start_dt = parse_datetime(user_datetime_text)
    if not start_dt:
        speak("I didn't understand the date and time. Setting for tomorrow at 9 AM.")
        start_dt = datetime.datetime.now() + datetime.timedelta(days=1, hours=9 - datetime.datetime.now().hour)
    
    # Step 3: Ask for subject/title
    speak("Got it. What would you like to call this event?")
    subject_text = listen_for_command()

    # Step 4: Create the event
    entry_id = add_outlook_event(subject=subject_text, start_time=start_dt, duration=60)
    speak(f"Your '{subject_text}' event has been scheduled for {start_dt.strftime('%A, %B %d at %I:%M %p')}.")

    print(f"(DEBUG) Created event with EntryID: {entry_id}")

def parse_datetime(text):
    """
    Naive placeholder that tries to parse a small set of phrases.
    For a real assistant, you'd install and user 'dateparser'.
    """
    text_lower = text.lower()

    now = datetime.datetime.now()

    

# Start the assistant
def main():
    speak("Starting your assistant. Say 'Hey Assistant' to wake me up!")
    # Use a separate thread to continuously listen for the wake phrase
    listen_for_wake_phrase()

    # Keep main thread alive (or do other tasks here)
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
