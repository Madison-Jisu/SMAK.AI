import pyaudio
import wave
import os

def record_audio(filename="speech.wav", duration=10, chunk=1024, channels=1, rate=44100):
    # Clear the file if it exists
    if os.path.exists(filename):
        open(filename, 'wb').close()
        print(f"Existing file '{filename}' has been emptied.")

    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    print("Recording started...")
    frames = []

    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Recording finished.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

    print(f"Recording saved to {filename}")
    return filename

def main():
    filename = record_audio()  # Uses default filename and duration
    print(f"Recorded file path: {filename}")

if __name__ == "__main__":
    main()
