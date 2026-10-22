# AI Productivity Monitor

A real-time, AI-powered productivity companion built with Python, OpenCV, and Google's Gemini API. The application monitors webcam input for potential slouching and checks the active desktop window for distracting applications. When a violation is detected, Gemini generates a short, sarcastic roast that is delivered through text-to-speech.

## Features

- **Real-Time Face Detection:** Uses OpenCV's Haar Cascade classifier to detect faces through a webcam.
- **Posture Monitoring:** Tracks the vertical position of the detected face and flags potential slouching when it remains below a configurable threshold.
- **Distraction Detection:** Monitors the active window title and checks for configured distracting platforms, including YouTube, Reddit, Instagram, Netflix, and TikTok.
- **AI-Generated Responses:** Integrates Google's Gemini API to generate short, context-aware, sarcastic responses to detected violations.
- **Voice Feedback:** Uses `pyttsx3` to speak generated responses aloud.
- **Asynchronous Speech:** Runs speech output in a separate thread to help keep the webcam monitoring loop responsive.
- **Cooldown Mechanism:** Implements a cooldown period between alerts to reduce repeated interruptions.
- **Live Visual Feedback:** Displays the webcam feed with face-detection rectangles, a posture threshold line, and the active window title.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| OpenCV | Webcam processing and face detection |
| Haar Cascade | Face detection classifier |
| Google Gemini API | AI-generated responses |
| `pyttsx3` | Offline text-to-speech |
| `PyGetWindow` | Active desktop window monitoring |
| `python-dotenv` | Environment variable management |
| Threading | Asynchronous speech output |

## How It Works

1. **Capture:** The application captures live video frames from the default webcam.
2. **Detect:** OpenCV processes each frame and identifies faces using a Haar Cascade classifier.
3. **Monitor posture:** The vertical center of the largest detected face is compared against a configurable threshold. If the face remains below that threshold for more than three seconds, a potential slouching event is triggered.
4. **Monitor distractions:** The application reads the active desktop window title and checks whether it contains the name of a configured distracting platform. A distraction is flagged if the matching window remains active for more than three seconds.
5. **Generate a response:** The detected violation is passed to the Gemini API, which generates a short, witty response.
6. **Speak:** The response is printed to the terminal and spoken using `pyttsx3` in a background thread.
7. **Prevent excessive alerts:** A cooldown timer limits how frequently new alerts can be triggered.

## Limitations

- **Basic posture estimation:** The application uses face position as a heuristic rather than a dedicated pose-estimation model. It cannot reliably distinguish slouching from normal movement or changes in camera position.
- **Window-title matching:** Distraction detection depends on active window titles and keyword matching. It may produce false positives or miss distracting activity.
- **Platform compatibility:** Active-window monitoring depends on operating-system support and may behave differently outside Windows.
- **Internet connection:** Gemini response generation requires network access and a working API key. A fallback message is used if the API request fails.
- **Speech output:** Voice availability and behavior depend on the operating system's text-to-speech support.
- **Alert concurrency:** Speech runs in background threads; rapid or overlapping triggers may cause speech to overlap.

This project is a productivity experiment and is not intended to provide medical advice or a reliable ergonomic assessment.

## Future Improvements

- Replace fixed-coordinate posture checks with MediaPipe Pose or another landmark-based pose-estimation model.
- Introduce a speech queue with a single worker to prevent overlapping voice alerts.
- Add configurable monitoring thresholds and user-defined distraction lists.
- Improve error handling for webcam, API, and speech failures.
- Add a simple settings interface and session statistics.


## Author

**Jeet Parimal Monani**

- GitHub: [JeetMonani](https://github.com/JeetMonani)
- LinkedIn: [jeetmonani](https://linkedin.com/in/jeetmonani)
