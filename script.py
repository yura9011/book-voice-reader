"""
This script provides a command-line interface to interact with the Google Gemini API
to generate audio from text, applying various stylistic tones.

It utilizes websockets for communication with the Gemini API and pygame for audio playback.

Features:
    - Select from multiple pre-defined voices for audio output.
    - Choose from a variety of stylistic tones to apply to the text before generating audio.
    - Input text directly or from a file.

Dependencies:
    - asyncio
    - websockets
    - wave
    - pygame
    - numpy
    - IPython (for displaying Markdown)

Configuration:
    - GOOGLE_API_KEY: Set this environment variable with your Google Gemini API key.
    - MODEL:  Specifies the Gemini model to use (default: 'models/gemini-2.0-flash-exp').
    - Available voices are defined in the `voices` set. The default voice is 'Kore'.

Usage:
    1. Set the GOOGLE_API_KEY environment variable.
    2. Run the script: `python your_script_name.py`
    3. The script will prompt you to select a tone and input mode (text or file).
    4. Follow the on-screen instructions to provide the text and generate the audio.

Stylistic Tones:
    The script offers the following stylistic tones, influencing how the text is spoken:
    - Neutral
    - Mysterious
    - Excited
    - Surprised
    - Sad
    - Angry
    - Uncertain
    - Whispering
    - Yelling
    - Slow
    - Fast
    - Surfer
    - Shakespeare
    - Pirate

File Input:
    When using file input, the script reads the entire file content as a single block of text
    and applies the selected tone to it.

Error Handling:
    The script includes basic error handling for file operations, API connections, and audio playback.

"""

import asyncio
import base64
import json
import numpy as np
import os
import websockets
import wave
import contextlib
import pygame
from IPython.display import display, Markdown

# ANSI color codes for terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

# Available voices for the Gemini API
voices = {"Puck", "Charon", "Kore", "Fenrir", "Aoede"}

# --- Configuration ---
MODEL = 'models/gemini-2.0-flash-exp'
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise EnvironmentError("GOOGLE_API_KEY environment variable is not set.")
HOST = 'generativelanguage.googleapis.com'
URI = f'wss://{HOST}/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContent?key={GOOGLE_API_KEY}'

# Audio parameters
WAVE_CHANNELS = 1  # Mono audio
WAVE_RATE = 24000
WAVE_SAMPLE_WIDTH = 2

@contextlib.contextmanager
def wave_file(filename, channels=WAVE_CHANNELS, rate=WAVE_RATE, sample_width=WAVE_SAMPLE_WIDTH):
    """Context manager for creating and managing wave files."""
    try:
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            yield wf
    except wave.Error as e:
        print(f"{RED}Error opening wave file '{filename}': {e}{RESET}")
        raise

async def audio_playback_task(file_name, stop_event):
    """Plays audio using pygame until stopped."""
    print(f"{BLUE}Starting playback: {file_name}{RESET}")
    try:
        pygame.mixer.music.load(file_name)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() and not stop_event.is_set():
            await asyncio.sleep(0.1)
    except pygame.error as e:
        print(f"{RED}Pygame error during playback: {e}{RESET}")
    except Exception as e:
        print(f"{RED}Unexpected error during playback: {e}{RESET}")
    finally:
        print(f"{BLUE}Playback complete: {file_name}{RESET}")

async def generate_audio(ws, text_input: str) -> None:
    """
    Sends the text to the Gemini API, receives an audio response, saves it to a file, and plays it.
    """
    pygame.mixer.init()  # Initialize pygame mixer

    msg = {
        "client_content": {
            "turns": [{"role": "user", "parts": [{"text": text_input}]}],
            "turn_complete": True,
        }
    }
    await ws.send(json.dumps(msg))

    responses = []
    async for raw_response in ws:
        response = json.loads(raw_response.decode())
        server_content = response.get("serverContent")
        if server_content is None:
            break

        model_turn = server_content.get("modelTurn")
        if model_turn:
            parts = model_turn.get("parts")
            if parts:
                for part in parts:
                    if "inlineData" in part and "data" in part["inlineData"]:
                        pcm_data = base64.b64decode(part["inlineData"]["data"])
                        responses.append(np.frombuffer(pcm_data, dtype=np.int16))

        turn_complete = server_content.get("turnComplete")
        if turn_complete:
            break

    if responses:
        display(Markdown(f"{YELLOW}**Response >**{RESET}"))
        audio_array = np.concatenate(responses)
        file_name = 'output.wav'
        with wave_file(file_name) as wf:
            wf.writeframes(audio_array.tobytes())
        stop_event = asyncio.Event()
        try:
            await audio_playback_task(file_name, stop_event)
        except Exception as e:
            print(f"{RED}Error during audio playback: {e}{RESET}")
    else:
        print(f"{YELLOW}No audio received{RESET}")
    pygame.mixer.quit()  # Clean up pygame mixer

# Tone transformation functions (corresponding to JavaScript)
def neutral(text):
    return f"Say: \"{text}\""

def mysterious(text):
    return f"Say this like a dramatic wizard speaking very mysteriously: \"{text}\""

def excited(text):
    return f"Say this like a very enthusiastic excited fast-talking friend: \"{text.upper()}!\""

def surprised(text):
    return f"Say with genuine shock and amazement: \"Oh wow! {text}!\""

def sad(text):
    return f"Say in a melancholic and dejected tone: \"*sigh* {text}...\""

def angry(text):
    return f"Say with intense anger and frustration: \"{text.upper()}!!!\""

def uncertain(text):
    return f"Say this like a question, even if it's not a question, as if you are very uncertain and confused about what you're saying: \"Hmm... {text}?\""

def whispering(text):
    return f"Whisper in a hushed, secretive voice: \"{text.lower()}\""

def yelling(text):
    return f"Shout with maximum volume, with urgency like you are yelling at someone: \"{text.upper()}!!!\""

def slow(text):
    return f"Say very slowly and deliberately: \"{'... '.join(text.split())}...\""

def fast(text):
    return f"Say rapidly and energetically: \"{'-'.join(text.split())}\""

def surfer(text):
    return f"Say this like a mellow, laid-back surfer, speaking slowly and using surfer slang: \"Woah... {text}, like, totally radical!\""

def shakespeare(text):
    return f"Say this like a Shakespearean actor speaking a very dramatic monologue: \"{text}\""

def pirate(text):
    return f"Say this like a pirate: \"Arrg, {text.replace('r', 'rrr')}... arrg\""

def read_from_file(filename: str) -> str:
    """Reads text content from the specified file."""
    try:
        with open(filename, 'r') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        print(f"{RED}Error: File not found: {filename}{RESET}")
        return None
    except Exception as e:
        print(f"{RED}Error reading file: {e}{RESET}")
        return None

async def main():
    print(f"{GREEN}Available voices: {', '.join(voices)}{RESET}")
    default_voice = "Kore"
    print(f"{GREEN}Default voice is set to: {default_voice}, you can change it in the code{RESET}")

    tones = {
        1: {"emoji": "💬", "name": "Neutral", "transform": neutral},
        2: {"emoji": "🔮", "name": "Mysterious", "transform": mysterious},
        3: {"emoji": "😃", "name": "Excited", "transform": excited},
        4: {"emoji": "😮", "name": "Surprised", "transform": surprised},
        5: {"emoji": "😔", "name": "Sad", "transform": sad},
        6: {"emoji": "😡", "name": "Angry", "transform": angry},
        7: {"emoji": "❓", "name": "Uncertain", "transform": uncertain},
        8: {"emoji": "🦗", "name": "Whispering", "transform": whispering},
        9: {"emoji": "🗯️", "name": "Yelling", "transform": yelling},
        10: {"emoji": "🐢", "name": "Slow", "transform": slow},
        11: {"emoji": "🐰", "name": "Fast", "transform": fast},
        12: {"emoji": "🏄", "name": "Surfer", "transform": surfer},
        13: {"emoji": "🎭", "name": "Shakespeare", "transform": shakespeare},
        14: {"emoji": "🏴‍☠️", "name": "Pirate", "transform": pirate},
    }

    async with websockets.connect(URI) as ws:

        async def setup(ws) -> None:
            await ws.send(
                json.dumps(
                    {
                        "setup": {
                            "model": MODEL,
                            "generation_config": {
                                "response_modalities": ["AUDIO"],
                                "speech_config": {
                                    "voice_config": {
                                        "prebuilt_voice_config": {
                                            "voice_name": default_voice
                                        }
                                    }
                                }
                            },
                        }
                    }
                )
            )
            raw_response = await ws.recv()
            setup_response = json.loads(raw_response.decode("ascii"))
            print(f"{GREEN}Connected: {setup_response}{RESET}")

        await setup(ws)
        while True:
            print(f"{YELLOW}Available Tones:{RESET}")
            for key, tone in tones.items():
                print(f"{YELLOW}{key}: {tone['emoji']} {tone['name']}{RESET}")

            while True:
                try:
                    tone_choice = int(input(f"{YELLOW}Select a tone by number (or type '0' to skip tone selection): {RESET}"))
                    if tone_choice == 0:
                        selected_transform = neutral  # Keep the neutral function for skipping
                        break
                    if tone_choice in tones:
                        selected_transform = tones[tone_choice]['transform']
                        break
                    else:
                        print(f"{RED}Invalid tone option. Please enter a number from the list.{RESET}")
                except ValueError:
                    print(f"{RED}Invalid input. Please enter a number.{RESET}")

            while True:
                input_mode = input(f"{YELLOW}Enter input mode (1 for text, 2 for file, or 'exit' to quit): {RESET}").lower()
                if input_mode == 'exit':
                    break
                if input_mode == "1":
                    text_prompt = input(f"{YELLOW}Enter your text: {RESET}")
                    segments_with_tones = [(selected_transform(text_prompt), selected_transform)]
                    break
                elif input_mode == "2":
                    filename = input(f"{YELLOW}Enter filename: {RESET}")
                    file_content = read_from_file(filename)
                    if file_content:
                        segments_with_tones = [(selected_transform(file_content), selected_transform)]
                        break
                    else:
                        print(f"{RED}Error reading file, please try again{RESET}")
                else:
                    print(f"{RED}Invalid Input Mode: Please enter 1 for text or 2 for file, or exit.{RESET}")

            if input_mode == 'exit':
                break

            try:
                for text, transform in segments_with_tones:
                    await generate_audio(ws, text)

            except Exception as e:
                print(f"{RED}An error occurred: {e}{RESET}")

if __name__ == "__main__":
    asyncio.run(main())