import subprocess

def record_audio(filename="audio.wav", duration=60):
    try:
        print(f"Recording {duration} seconds of audio to {filename}...")
        subprocess.run([
            "arecord",
            "-D", "plughw:1",   # Might be hw:1,0 or plughw:1 depending on your device
            "-f", "S16_LE",     # 16-bit little endian
            "-c", "1",          # Mono
            "-r", "16000",      # Sample rate: 16000 Hz
            "-d", str(duration),  # Duration in seconds
            filename
        ], check=True)
        print("Recording complete.")
    except subprocess.CalledProcessError as e:
        print(f"Recording failed: {e}")

if __name__ == "__main__":
    record_audio()
