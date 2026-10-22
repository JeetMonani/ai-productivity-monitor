import cv2
import time
import os
import urllib.request
import threading
import pygetwindow as gw
import pyttsx3
import dotenv
from google import genai

dotenv.config()

def speak_threaded(text):
    def run_speech(msg):
        print(f"🤖 AI: {msg}")
        engine = pyttsx3.init()
        engine.setProperty('rate', 170)
        engine.say(msg)
        engine.runAndWait()
        
    threading.Thread(target=run_speech, args=(text,), daemon=True).start()

# 2. Setup Gemini Client
# Make sure your system environment variable set GEMINI_API_KEY="your-api-key"
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def generate_roast(reason):
    prompt = f"""
    You are a passive-aggressive, sarcastic AI productivity companion.
    The user was just caught violating workplace productivity/posture rules.
    
    Violation: {reason}
    
    Write a short, witty, 1-sentence passive-aggressive roast directly addressing the user. 
    Keep it under 20 words so it can be spoken out loud quickly. Do not use emojis, hashtags, or markdown formatting.
    """
    try:
        # Using gemini-2.5-flash with standard prompt generate
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"⚠️ API Warning: {e}")
        return f"Stand up straight. {reason} is completely unacceptable."

# 3. Load Haar Cascade Face Classifier
CASCADE_FILE = "haarcascade_frontalface_default.xml"
if not os.path.exists(CASCADE_FILE):
    print("📥 XML file missing. Downloading Haar Cascade face detector...")
    url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
    urllib.request.urlretrieve(url, CASCADE_FILE)

face_cascade = cv2.CascadeClassifier(CASCADE_FILE)

# Trackers & Configs
DISTRACTING_APPS = ["reddit", "youtube", "twitter", "x", "instagram", "netflix", "tiktok"]
slouch_start_time = None
distraction_start_time = None
TRIGGER_COOLDOWN = 12  # Seconds between roasts
last_trigger_time = 0
SLOUCH_Y_THRESHOLD = 260  

def get_active_window_title():
    try:
        win = gw.getActiveWindow()
        return win.title.lower() if win else ""
    except Exception:
        return ""

cap = cv2.VideoCapture(0)
print("👀 Passive-Aggressive Vision Engine Active with AI Voice. Press 'q' to quit.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    current_time = time.time()
    trigger_reason = None

    # Check Screen Distraction
    active_title = get_active_window_title()
    is_distracted = any(app in active_title for app in DISTRACTING_APPS)

    if is_distracted:
        if distraction_start_time is None:
            distraction_start_time = current_time
        elif current_time - distraction_start_time > 3.0:
            trigger_reason = f"browsing '{active_title[:25]}' instead of working"
    else:
        distraction_start_time = None

    # Check Posture
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(60, 60))
    if len(faces) > 0:
        (x, y, fw, fh) = max(faces, key=lambda rect: rect[2] * rect[3])
        face_center_y = y + (fh // 2)

        cv2.rectangle(frame, (x, y), (x + fw, y + fh), (255, 0, 0), 2)
        cv2.line(frame, (0, SLOUCH_Y_THRESHOLD), (w, SLOUCH_Y_THRESHOLD), (0, 0, 255), 1)

        if face_center_y > SLOUCH_Y_THRESHOLD:
            if slouch_start_time is None:
                slouch_start_time = current_time
            elif current_time - slouch_start_time > 3.0:
                trigger_reason = "slouching down like a melted marshmallow"
        else:
            slouch_start_time = None

    # Trigger LLM Roast & Speech Output asynchronously
    if trigger_reason and (current_time - last_trigger_time > TRIGGER_COOLDOWN):
        last_trigger_time = current_time
        print(f"\n🚨 TRIGGERED: {trigger_reason}")
        roast = generate_roast(trigger_reason)
        speak_threaded(roast)

    # Overlay UI
    cv2.putText(frame, f"Active Window: {active_title[:25]}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    cv2.imshow("Passive-Aggressive Monitor", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()