import os
import wave
import pyaudio
from transformers import pipeline

def record_audio(filename="final_output.wav", duration=15, chunk=1024, channels=1, rate=44100):
    # Clear the file if it exists
    if os.path.exists(filename):
        open(filename, 'wb').close()
        print(f"[INFO] Existing file '{filename}' has been emptied.")

    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    print(f"[INFO] Recording started for {duration} seconds... 🎤")
    frames = []

    for i in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
        if i % int(rate / chunk) == 0:
            print(f"[DEBUG] Recording... {i * chunk / rate:.1f} sec elapsed", end='\r')

    print("\n[INFO] Recording finished. ✅")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

    print(f"[INFO] Recording saved to '{filename}'\n")
    return filename

def analyze_emotion(filename="final_output.wav"):
    print("[INFO] Loading audio emotion classifier... 🎧")
    classifier = pipeline(
        task='audio-classification',
        model='superb/hubert-large-superb-er'
    )

    print(f"[INFO] Analyzing emotion in '{filename}'...")
    result = classifier(filename)

    print("\n[RESULT] Full model output:")
    for r in result:
        print(f" - {r['label']}: {r['score']*100:.1f}%")

    top_emotion = max(result, key=lambda x: x['score'])
    print(f"\n[SUMMARY] Detected emotion: {top_emotion['label'].upper()} ({top_emotion['score']*100:.1f}%)\n")

def main():
    print("=== AI Voice Emotion Demo ===\n")
    filename = record_audio(duration=15)
    analyze_emotion(filename)
    print("=== Demo Complete ===")

if __name__ == "__main__":
    main()
