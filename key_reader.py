import mido

# Liste aller verfügbaren MIDI-Ports anzeigen
print("Verfügbare MIDI-Eingänge:")
for port in mido.get_input_names():
    print(port)

# Hier den passenden Port auswählen (z.B. durch Kopieren des Namens)
port_name = input("Gib den MIDI-Port ein, den du verwenden willst: ")

# MIDI-Eingang öffnen
with mido.open_input(port_name) as inport:
    print("Starte das Auslesen. Drücke Tasten auf deinem Piano...")
    try:
        for msg in inport:
            if msg.type in ['note_on', 'note_off']:
                note = msg.note
                velocity = msg.velocity
                action = "gedrückt" if msg.type == 'note_on' and velocity > 0 else "losgelassen"
                print(f"Note {note} {action} (Velocity: {velocity})")
    except KeyboardInterrupt:
        print("Beendet.")
