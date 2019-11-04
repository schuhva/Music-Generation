
1.04 Start and Basics
=====================

Pyknon offers to easily generate midi files, rather to modify the
MIDI-file directly and manually with noteOn and noteOff commands.

.. code:: python3

    from pyknon.genmidi import Midi
    from pyknon.music import Rest, Note, NoteSeq
    import numpy as np

Pyknon
------

There exist two different notations one with the **Note()** function and
a simplified **plain text** version

Note(value , octave , dur , volume)

-  value: integer, note hight in semitones, 0 = middle C = midi 60
-  octave: octave number
-  dur: duration, 0.25 = quarter note
-  volume: from 1 to 127

.. code:: python3

    def tune_A():
        notes1 = NoteSeq(      "C4 D E F G A B C''")   # Apostroph ' = "gestrichen" = Höhe der Oktave
        notes2 = NoteSeq("r1 r1 C4'' B' A G F E D C")   # r = rest = Pause; Zahl = Länge der Pause
        return notes1, notes2
    
    def tune_B():
        notes1 = NoteSeq("Db4- F#8 A Bb4")   # Zahl = Länge des Tones: 1=ganz, 4=Viertel
        notes2 = NoteSeq([Note(2, dur=1/4), Note(6, dur=1/8), Note(9, dur=1/8), Note(10, dur=1/4)])
        return notes1, notes2
    
    def tune_C():
        major = [0,2,4,5,7,9,11]
        minor = [0,2,3,5,7,8,10]
        track1 = major + [12]
        track2 = minor[::-1]                           # reverse
        notes1 = NoteSeq( [Note(no) for no in track1] )
        notes2 = NoteSeq( [Rest(2)] + [Note(no) for no in track2] )
        return notes1, notes2
    
    def generate_midi():
        #--- choose the tune 
        notes1, notes2 = tune_C()        
    
        #--- squezze into a MIDI framework 
        m = Midi(2, tempo=120)     #  
        m.seq_notes(notes1, track=0)
        m.seq_notes(notes2, track=1)
    
        #--- write the MIDI file 
        midi_file_name =  "tune_C.mid"       # set the name of the file
        m.write(midi_file_name)
        return midi_file_name
    
    generate_midi()




.. parsed-literal::

    'tune_C.mid'



MIDI: Play and Generate audio-file
----------------------------------

External players offered a better sound quality in comparison with
python libraries. We use **VLC** and **Musescore**.

.. code:: python3

    import subprocess
    default_soundfont = '/usr/share/sounds/sf3/MuseScore_General.sf3'
    
    def midi_play(midi_in, soundfont= default_soundfont):
        subprocess.call(['cvlc', midi_in , 'vlc://quit'])   # cvlc = vlc without gui
        
    def midi_audio(midi_in, name_out = 'none', soundfont= default_soundfont):
        if name_out == 'none' :
            name_out = midi_in.replace('.mid', '.flac')
        else:
            name_out = name_out + '.flac'
        subprocess.call(['mscore', '-o', name_out, midi_in]) # -o = export as
    
    def midi_png(midi_in, name_out = 'none'):
        if name_out == 'none' :
            name_out = midi_in.replace('.mid', '.png')
        else:
            name_out = name_out + '.png'
        subprocess.call(['mscore', '-o', name_out, '-T', '2', midi_in]) # -o = export as , -T 0 = cut page with 0 pixel
        
        
    midi_play('tune_C.mid')
    midi_audio('tune_C.mid')
    midi_png('tune_C.mid')

.. raw:: html

    <br><audio controls="controls" src="https://raw.githubusercontent.com/schuhva/Music-Generation/master/doc/releases/1.04_poc/tune_A.flac" type="audio/flac"></audio>
     tune_A
    <br><audio controls="controls" src="https://raw.githubusercontent.com/schuhva/Music-Generation/master/doc/releases/1.04_poc/tune_B.flac" type="audio/flac"></audio>
     tune_B
    <br><audio controls="controls" src="https://raw.githubusercontent.com/schuhva/Music-Generation/master/doc/releases/1.04_poc/tune_C.flac" type="audio/flac"></audio>
     tune_C
    <br><img alt="self-Logo" src="https://raw.githubusercontent.com/schuhva/Music-Generation/master/doc/releases/1.04_poc/tune_C-1.png">
    <br>tune_C
 

