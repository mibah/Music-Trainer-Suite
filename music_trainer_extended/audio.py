# audio.py
import sounddevice as sd
import numpy as np
import aubio

class PitchDetector:
    def __init__(self, samplerate=44100, buf_size=1024, volume_threshold=0.01):
        self.pitch_o = aubio.pitch("default", buf_size*2, buf_size, samplerate)
        self.pitch_o.set_unit("Hz")
        self.pitch_o.set_silence(-100)
        self.samplerate = samplerate
        self.buf_size = buf_size
        self.volume_threshold = volume_threshold
        self.stream = None

    def start(self, callback):
        def audio_callback(indata, frames, time, status):
            samples = np.mean(indata, axis=1).astype(np.float32)
            rms = np.sqrt(np.mean(samples**2))
            if rms < self.volume_threshold:
                return
            pitch = self.pitch_o(samples)[0]
            callback(pitch)

        self.stream = sd.InputStream(callback=audio_callback, channels=1,
                                     samplerate=self.samplerate, blocksize=self.buf_size)
        self.stream.start()

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()