# Gemini Audio Text-to-Speech CLI

**Last Updated:** October 22, 2024

This Python script provides a command-line interface to interact with the Google Gemini API for generating audio from text, applying various stylistic tones. It leverages websockets for real-time communication with the Gemini API and pygame for audio playback.

This project is inspired by the [Voice Cursor](https://github.com/googlecreativelab/gemini-demos/tree/main/voice-cursor) project, an experimental text editor showcasing Gemini 2.0's Native Audio capabilities. Our script aims to replicate the text-to-speech functionality but as a command-line tool.

## Current Functionalities

-   **Native Gemini Audio:** Direct integration with Gemini 2.0's text-to-speech capabilities via websockets.
-   **Multiple Voice Options:** Select from various pre-defined Gemini voices for the audio output.
-   **Rich Tone Selection:** Choose from a wide array of stylistic tones to apply to the text before generating audio.
-   **Flexible Input:** Input text directly or from a text file.
-   **Real-time Audio Playback:** Plays generated audio using pygame.

## Planned Enhancements

-   **Graphical User Interface (GUI):** Development of a GUI to provide an easier and more interactive way to use the script.

## Dependencies

- Python 3.9 or higher
- `asyncio`
- `websockets`
- `wave`
- `pygame`
- `numpy`
- `IPython` (for displaying Markdown, optional)

You can install these dependencies using pip:

```bash
pip install websockets pygame numpy ipython
Use code with caution.
Markdown
Configuration
GOOGLE_API_KEY: You must set this environment variable with your Google Gemini API key. Get your API key from Google AI Studio.

MODEL: (Optional) Specifies the Gemini model to use. The default value is models/gemini-2.0-flash-exp.

Available Voices: The script uses a predefined set of voices: Puck, Charon, Kore, Fenrir, and Aoede. The default voice is set to Kore, but you can change this in the code.

Usage
Set the GOOGLE_API_KEY environment variable. For example, in Linux or macOS, you can use:

export GOOGLE_API_KEY=your_api_key_here
Use code with caution.
Bash
Or, on Windows:

$env:GOOGLE_API_KEY="your_api_key_here"
Use code with caution.
Powershell
Run the script:

python your_script_name.py
Use code with caution.
Bash
The script will prompt you to:

Select a tone by entering the corresponding number. You can also enter 0 to skip tone selection.

Choose an input mode: 1 for direct text input, 2 for text from a file, or exit to quit.

Provide the required text, either by typing directly or providing a filename.

The script will process the text, generate the audio with the selected tone, and play it back using pygame.

Stylistic Tones
The script includes a variety of stylistic tones, each influencing the way the text is spoken. Here's a list of supported tones:

Number	Emoji	Name	Description
1	💬	Neutral	The text is spoken without specific emotion or style.
2	🔮	Mysterious	The text is spoken like a dramatic wizard with a mysterious tone.
3	😃	Excited	The text is spoken with high enthusiasm and energy.
4	😮	Surprised	The text is spoken with genuine shock and amazement.
5	😔	Sad	The text is spoken with a melancholic and dejected tone.
6	😡	Angry	The text is spoken with intense anger and frustration.
7	❓	Uncertain	The text is spoken as if asking a question, even if it isn't, and with confusion.
8	🦗	Whispering	The text is whispered in a hushed, secretive voice.
9	🗯️	Yelling	The text is shouted with maximum volume and urgency.
10	🐢	Slow	The text is spoken very slowly and deliberately.
11	🐰	Fast	The text is spoken rapidly and energetically.
12	🏄	Surfer	The text is spoken like a mellow surfer using surfer slang.
13	🎭	Shakespeare	The text is spoken like a Shakespearean actor during a dramatic monologue.
14	🏴‍☠️	Pirate	The text is spoken like a pirate, using pirate slang.
File Input
When selecting file input (2), the script will read the entire file content as a single block of text and apply the selected stylistic tone.

Error Handling
The script provides basic error handling for:

File operations (e.g., if a file is not found).

API connection errors.

Audio playback errors.

Code Structure
main(): Contains the main program loop, handling user input, API interaction, and audio output.

generate_audio(ws, text_input): Sends text to the Gemini API via websocket and processes the audio response.

audio_playback_task(file_name, stop_event): Plays audio using pygame until stopped.

wave_file(filename, channels, rate, sample_width): Context manager to handle wave file operations.

neutral(text), mysterious(text), etc.: Functions for applying stylistic tone transformations to text.

read_from_file(filename): Reads the content of a file.

Disclaimer
This project is an experiment showcasing Gemini API's text-to-speech capabilities and is not an official Google product. We'll do our best to support and maintain this experiment, but your mileage may vary. We encourage open-sourcing projects as a way of learning from each other. Please respect our and other creators' rights, including copyright and trademark rights when present, when sharing these works and creating derivative works. If you want more info on Google's policy, you can find it here.

License
Licensed under the Apache-2.0 license.