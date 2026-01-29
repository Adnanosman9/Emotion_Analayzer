<div align="center">

# Emotion Analyzer

A webcam app that uses Google's Gemini-2.5-flash AI to analyze your appearance and roast you in real-time.

<img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/OpenCV-4.2+-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV">
<img src="https://img.shields.io/badge/Google_Gemini-2.5_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Gemini">

</div>

---

## Quick Start

```bash
# Install dependencies
pip install google-generativeai opencv-python python-dotenv Pillow pyttsx3

# Create .env file with your API key
echo GOOGLE_API_KEY=your_api_key_here > .env

# Run
python vision.py
```

Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

Press **Q** to quit.

---

## Development Journey & Debugging

Building this was honestly a mess. Here's what went wrong and how I fixed it (with a mess with AI).

### Problem 1: Video Freezing During Analysis

The video would freeze for 3-4 seconds every time the AI analyzed a frame. The Gemini API call was blocking the entire video loop.

**The Fix:**
Moved the analysis to a background thread so the video keeps running:

```python
def process():
    result = analyze(frame)
    print(result)
    speak(result)

threading.Thread(target=process, daemon=True).start()
```

### Problem 2: Analysis Not Working Properly

After adding threading, the app would only analyze once and then stop. The state tracking logic was broken because the thread hadn't finished when the flag was set.

**The Fix:**
Replaced complex state tracking with a simple 10-second timer:

```python
if len(faces) > 0 and (time.time() - last_time) >= 10:
    last_time = time.time()
    # analyze in background thread
```

### Honest Truth

I didn't really understand threading or the `time` library that well before this. Most of the debugging was done with **Claude Sonnet 4.5** helping me figure out why things weren't working. 

Pro tip: AI loves to fix one bug and casually introduce two more like it's doing me a favor. The AI-generated code had some "dummy" patterns that I tried to clean up, but there are probably still some AI fingerpr in there.

<div align="center">

**Debugged with:**

<img src="https://img.shields.io/badge/Claude-Sonnet_4.5-CC785C?style=for-the-badge&logo=anthropic&logoColor=white" alt="Claude Sonnet 4.5">

</div>

---

## How It Works

1. Camera opens with DirectShow backend
2. Detects faces every frame using Haar Cascade
3. Every 10 seconds (if face detected) → send frame to Gemini AI
4. AI analyzes appearance and gives blunt feedback
5. Results printed to console and spoken out loud (both in background threads)
6. Video keeps running smoothly throughout

---

## Troubleshooting

**Camera not working?**

- Close other apps using the camera
- Check Windows camera permissions
- Make sure you're using `cv2.CAP_DSHOW`

**API errors?**

- Check your API key in `.env`
- Verify internet connection
- You might've hit the free tier limit

**Video still freezing?**

- The threading should fix this, but if not, try reducing the analysis frequency

---

## License

MIT License

Note : This project is a humorous experiment in AI interaction and please don't take it's answers seriouslyt if it hurts you personally

