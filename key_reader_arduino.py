import mido
import serial
import time

# ==================== KONFIGURATION ====================

# Serielle Verbindung zum Arduino (Port anpassen!)
ARDUINO_PORT = '/dev/cu.usbmodem1401'  # Windows: COM3, COM4, etc. | Linux/Mac: /dev/ttyUSB0, /dev/ttyACM0
BAUD_RATE = 115200

# LED-Strip Konfiguration (muss mit Arduino übereinstimmen)
NUM_LEDS = 60
LEDS_PER_KEY = 1  # Wie viele LEDs pro Taste

# MIDI-Mapping (88 Tasten Piano: A0=21 bis C8=108)
# Dein LED-Strip hat 60 LEDs, also z.B. 5 Oktaven á 12 LEDs
MIDI_NOTE_START = 36  # C2 (mittlere Oktave beginnt bei C4=60)
MIDI_NOTE_END = 96  # C7

# Refresh-Einstellungen
REFRESH_INTERVAL = 0.01  # Alle 10ms refreshen

# ==================== GLOBALE VARIABLEN ====================

# Dictionary um gehaltene Tasten zu tracken: {note: (led_index, velocity)}
active_notes = {}
last_refresh_time = 0


# ==================== FUNKTIONEN ====================

def midi_note_to_led(note):
    """Konvertiert MIDI-Note zu LED-Index"""
    if note < MIDI_NOTE_START or note > MIDI_NOTE_END:
        return None

    # Lineare Zuordnung: Note 36-96 -> LED 0-59
    led_index = int((note - MIDI_NOTE_START) * NUM_LEDS / (MIDI_NOTE_END - MIDI_NOTE_START + 1))
    return min(led_index, NUM_LEDS - 1)


def send_to_arduino(ser, led_index, velocity):
    """Sendet LED-Befehl an Arduino"""
    # Format: "L<LED_INDEX>,<VELOCITY>\n"
    # Velocity 0-127 wird zu Helligkeit 0-255
    brightness = int((velocity / 127.0) * 255)
    command = f"L{led_index},{brightness}\n"
    ser.write(command.encode())


def clear_all_leds(ser):
    """Alle LEDs ausschalten"""
    ser.write(b"C\n")
    print("  → Arduino: Alle LEDs ausgeschaltet")


def refresh_active_notes(arduino):
    """Refresht alle aktiven LEDs um Fade zu verhindern"""
    global last_refresh_time

    current_time = time.time()

    # Nur alle REFRESH_INTERVAL Sekunden refreshen
    if current_time - last_refresh_time >= REFRESH_INTERVAL:
        for note, (led_index, velocity) in active_notes.items():
            send_to_arduino(arduino, led_index, velocity)
        last_refresh_time = current_time


# ==================== HAUPTPROGRAMM ====================

def main():
    global active_notes

    # MIDI-Ports anzeigen
    print("=" * 50)
    print("MIDI → Arduino LED Controller")
    print("=" * 50)
    print("\nVerfügbare MIDI-Eingänge:")
    input_ports = mido.get_input_names()

    if not input_ports:
        print("  Keine MIDI-Geräte gefunden!")
        return

    for i, port in enumerate(input_ports):
        print(f"  [{i}] {port}")

    # MIDI-Port auswählen
    port_index = int(input("\nWähle MIDI-Port (Nummer): "))
    midi_port_name = input_ports[port_index]

    # Arduino-Verbindung herstellen
    print(f"\nVerbinde mit Arduino auf {ARDUINO_PORT}...")
    try:
        arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Arduino Reset abwarten
        print("  ✓ Arduino verbunden")
    except serial.SerialException as e:
        print(f"  ✗ Fehler: {e}")
        print(f"\nTipp: Passe ARDUINO_PORT an (aktuell: {ARDUINO_PORT})")
        return

    # LEDs initial löschen
    clear_all_leds(arduino)

    # MIDI-Eingang öffnen und Nachrichten verarbeiten
    print(f"\nÖffne MIDI-Port: {midi_port_name}")
    print("Bereit! Spiel auf deinem Keyboard...\n")
    print("Drücke Ctrl+C zum Beenden\n")

    try:
        with mido.open_input(midi_port_name) as inport:
            # Non-blocking MIDI reading mit Timeout
            for msg in inport.iter_pending():
                # Process any pending MIDI messages
                pass

            while True:
                # Check for new MIDI messages (non-blocking)
                for msg in inport.iter_pending():
                    if msg.type in ['note_on', 'note_off']:
                        note = msg.note
                        velocity = msg.velocity

                        # Note Off oder Note On mit Velocity 0 = Taste losgelassen
                        if msg.type == 'note_off' or velocity == 0:
                            # Note aus active_notes entfernen
                            if note in active_notes:
                                led_index = active_notes[note][0]
                                del active_notes[note]
                                send_to_arduino(arduino, led_index, 0)
                                print(f"Note {note} losgelassen → LED {led_index} AUS")
                        else:
                            # Note On mit Velocity > 0
                            led_index = midi_note_to_led(note)

                            if led_index is not None:
                                # Note zu active_notes hinzufügen
                                active_notes[note] = (led_index, velocity)
                                send_to_arduino(arduino, led_index, velocity)
                                print(f"Note {note} gedrückt (V:{velocity}) → LED {led_index} AN")
                            else:
                                print(f"Note {note} außerhalb des LED-Bereichs")

                # Refresh aktive LEDs (verhindert Fade)
                if active_notes:
                    refresh_active_notes(arduino)

                # Kurze Pause um CPU zu schonen
                time.sleep(0.001)

    except KeyboardInterrupt:
        print("\n\nBeende...")
        clear_all_leds(arduino)
        arduino.close()
        print("Alle LEDs ausgeschaltet. Tschüss!")


if __name__ == "__main__":
    main()