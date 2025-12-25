# 🎹 Music Trainer Suite

**AI-Powered Musical Learning with Real-Time Visual Feedback**

An interactive music learning platform that combines pitch detection, chord recognition, and physical LED feedback to help musicians practice effectively—no MIDI required!

## ✨ What Makes This Special

Most music learning tools require expensive MIDI keyboards. This suite works with **any instrument**—guitar, saxophone, voice, piano—using AI-powered audio analysis to detect what you're playing in real-time.

## 🎯 Features

### Software Modules
- 🎼 **Full Keyboard Trainer** - 88-key visual piano for melody practice
- 🎯 **Extended Trainer** - Single octave focus for beginners
- 🎵 **Chord Trainer** - Polyphonic chord recognition with Librosa
- 🎸 **Arpeggio Trainer** - Sequential pattern practice
- 💡 **Arduino-Integrated Version** - Physical LED strip feedback

### Hardware System (Optional)
- 💡 Arduino LED Controller with WS2811 strip (60 LEDs)
- 🌊 Ultrasonic motion sensor for ambient patterns
- 🎨 Three modes: Motion patterns, MIDI visualization, Trainer integration
- ✋ Touch controls for brightness adjustment

## 🤖 Technology Stack

**Audio Analysis:**
- **Aubio YIN Algorithm** - Real-time pitch detection for melodies
- **Librosa Chromagram** - STFT-based chord recognition
- **SoundDevice** - Low-latency audio capture

**Visualization:**
- **Pygame** - On-screen piano keyboard
- **Arduino + FastLED** - Physical LED feedback
- **Serial Communication** - Python ↔ Arduino integration

## 🚀 Quick Start
```bash
# Install dependencies
pip install pygame sounddevice aubio numpy librosa pyserial

# Run melody trainer
cd music_trainer_full_keyboard
python main.py

# With Arduino LED feedback
cd music_trainer_full_keyboard_arduino
python main.py  # Auto-detects Arduino
```

## 🎨 Dual Feedback System

**Screen Display:**
- ✓ Precise note identification
- ✓ Full keyboard context
- ✓ Lives counter & score

**LED Strip (Optional):**
- ✓ Peripheral vision feedback
- ✓ No screen distraction
- ✓ Immersive environment
- ✓ Color-coded responses (🟢 correct / 🔴 wrong)

> 💡 **Pro Tip:** The LED strip lets you focus on your instrument while getting instant visual feedback in your peripheral vision!

## 📁 Project Structure
```
music_trainer_suite/
├── music_trainer_full_keyboard/          # Core melody trainer
├── music_trainer_extended/               # Single octave version
├── music_trainer_chords/                 # Chord recognition
├── music_trainer_arpeggios/              # Arpeggio practice
├── music_trainer_full_keyboard_arduino/  # LED-integrated version
└── arduino/
    └── TripleModeLEDController.ino       # Arduino code (3 modes)
```

## 🔧 Hardware Setup (Optional)

**Components:**
- Arduino (Uno/Nano/Mega)
- WS2811 LED Strip (60 LEDs)
- HC-SR04 Ultrasonic Sensor
- 2x Touch Sensors
- 5V Power Supply

**Wiring:**
- LED Data → Pin 9
- Ultrasonic Trigger → Pin 7
- Ultrasonic Echo → Pin 8
- Touch Sensors → Pins 4 & 5

**Arduino Modes:**
1. 🌈 **Motion Patterns** - Ambient LED animations
2. 🎹 **MIDI Visualization** - Keyboard light-up (via separate script)
3. 🎯 **Trainer Mode** - Synchronized with Python trainer

Hold both touch sensors for 1s to cycle modes!

## 🎓 How It Works

1. **Audio Capture** - Microphone records your playing
2. **AI Analysis** - Aubio/Librosa detects pitch/chords
3. **Note Matching** - Compares to target with tolerance
4. **Visual Feedback** - Screen + LED respond instantly

### Single Note Detection (Melody/Arpeggio)
```python
# Aubio YIN algorithm
pitch_o = aubio.pitch("default", buf_size*2, buf_size, samplerate)
pitch = pitch_o(audio_samples)[0]  # Frequency in Hz
```

### Chord Detection
```python
# Librosa chromagram
chroma = librosa.feature.chroma_stft(y=audio, sr=samplerate)
chroma_mean = np.mean(chroma, axis=1)  # 12-tone vector
score = np.dot(chroma_mean, chord_template)
```

## 🎯 Use Cases

- 🎼 **Practice melodies** from sheet music
- 🎵 **Learn chord progressions** for songs
- 🎸 **Master arpeggios** and scales
- 👂 **Train your ear** with real-time feedback
- 🎹 **No MIDI needed** - works with any instrument!

## 📊 Example: Custom Melody
```python
from melody_game import MelodyTrainer

# Define your practice sequence
notes = ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"]

# With Arduino LED feedback
trainer = MelodyTrainer(notes, use_arduino=True)
trainer.play()
```

## 🛠️ Customization

**Adjust detection sensitivity:**
```python
trainer = MelodyTrainer(
    notes,
    tolerance=0.5,        # ±0.5 semitones
    timeout=3,            # 3 seconds per note
    volume_threshold=0.01 # Noise gate
)
```

**Add custom chords:**
```python
# In music_trainer_chords/utils.py
CHORD_NOTE_MAP = {
    "Cmaj7": ["C4", "E4", "G4", "B4"],
    "Dm9": ["D4", "F4", "A4", "C5", "E5"]
}
```

## 🐛 Troubleshooting

- **No audio detected?** → Check microphone permissions
- **Wrong notes?** → Reduce background noise, increase `tolerance`
- **Arduino not found?** → Specify port: `arduino_port='/dev/ttyUSB0'`
- **LEDs not responding?** → Hold both touch sensors to cycle modes

## 🌟 Why This Project?

I built this to help my girlfriend learn piano, but discovered how fun it is to push AI-powered music education forward. Unlike expensive MIDI-only solutions, this works with **any instrument** and adds an immersive LED component that keeps you focused on playing, not screens.

## 📜 License

MIT License - Feel free to use, modify, and share!

## 🤝 Contributing and Support

Issues and PRs welcome! This is a learning project that grew beyond expectations.
<pre><code><span style="font-size:150%;">Happy about a ☕️ <a href="https://ko-fi.com/mikelbahn">https://ko-fi.com/mikelbahn</a> if you like the project.</span></code></pre>
---

**🎶 Happy practicing! Remember: the LEDs are just feedback—the real magic happens in your hands. 🎹✨**