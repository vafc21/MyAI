
# MyAI

**MyAI** is a Python-based personal assistant, capable of recognizing speech, speaking responses, answering questions using both a **local AI model (GPT-Neo)** and **OpenAI's GPT-4o**, browsing the web, and sending emails.

---

## Features

- 🎙️ Voice recognition (Speech-to-Text)  
- 🔊 Text-to-Speech (TTS) output  
- 🧠 Dual AI support:
  - Local inference using **GPT-Neo-1.3B** (runs on GPU)
  - Cloud inference using **OpenAI GPT-4o**
- 🌐 Open websites (e.g., Google)
- ⏰ Tell the current time
- 📧 Send emails (function structure present, needs implementation)
- 🖥️ Basic GUI groundwork (Tkinter imported but not yet used)

---

## Requirements

- Python 3.8+
- CUDA-capable GPU (for local model inference)
- Internet connection (for GPT-4o, web, and email features)

### Python Libraries

Install all required packages:

```bash
pip install speechrecognition pyttsx3 requests torch transformers openai pyaudio
```

*(Note: If installing PyAudio fails on Windows, you might need to use a `.whl` file manually.)*

---

## Setup

1. Install all dependencies.
2. *(Optional)* Add your OpenAI API key inside the code where indicated.
3. Run the program:

```bash
python MyAI.py
```

Your AI assistant (named "Jarvis" by default) will start listening for voice commands.

---

## Usage

You can say things like:

- **"Open Google"** → Opens Google in your web browser.
- **"What time is it?"** → Speaks the current time.
- **"Send email"** → Begins asking for email details (*Note: `send_email()` needs to be fully implemented*).
- **Ask any general question** → The assistant responds using either the local GPT model or OpenAI's GPT-4o, depending on the setting.

---

## Notes

- **Local Mode:** Uses GPT-Neo-1.3B model running on your GPU.
- **Cloud Mode:** Uses OpenAI GPT-4o via API.
- The `send_email()` method is referenced but **currently missing** — you need to add the function to enable email sending.
- `onWhat` variable switches between `'pc'` (local model) and online mode.

---

## Future Improvements

- Implement the missing `send_email()` method.
- Add a Tkinter GUI interface.
- Implement wake-word detection ("Hey Jarvis") for passive listening.
- Expand supported commands (weather updates, reminders, etc.)
- Add robust error handling.

---

## License

This project is licensed under the [MIT License](LICENSE).

© 2025 [vafc21](https://github.com/vafc21)
