import google.generativeai as genai
from PIL import Image
import cv2
import os
from dotenv import load_dotenv
import pyttsx3
import threading
import time

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
model = genai.GenerativeModel('gemini-2.5-flash')


def speak(text):
    def run():
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    threading.Thread(target=run, daemon=True).start()


def analyze(frame):
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    prompt = """Analyze this person briefly and bluntly (2-3 sentences max):
    - If messy/unkempt: "Why are you so ugly?"
    - If sad: "Why are you so sad?"
    - If tired: "Why do you look so tired?"
    - If happy: "You look happy today!"
    - If well-dressed: "Looking sharp!"

    Add one quick comment about their appearance. Be direct, no fluff."""

    return model.generate_content([prompt, img]).text


cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

last_time = 0
result = ""

print("press q to quit\n")

while True:
    success, frame = cam.read()
    if not success:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0 and (time.time() - last_time) >= 10:
        last_time = time.time()


        def process():
            global result
            result = analyze(frame)
            print(result)
            speak(result)


        threading.Thread(target=process, daemon=True).start()

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if result:
        y = 30
        for line in result.split('. '):
            if line:
                cv2.putText(frame, line[:60], (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                y += 25

    cv2.imshow('vision', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("\nGoodbye!")
        speak("Goodbye!")
        break

cam.release()
cv2.destroyAllWindows()
