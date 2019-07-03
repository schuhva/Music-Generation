
1.03
====

With pyknon ex.1 , ex.2 and midi2audio I have evything to generate midi
and to play and export them as music file. With pyknon NoteSeq funktion
i have a usabel interface to build the farmes and so to give structure
to the music.

pyknon ex.1
-----------

1. output only as midi
2. has many features

.. code:: python3

    from pyknon.genmidi import Midi
    from pyknon.music import Rest, Note, NoteSeq
    import numpy as np

.. code:: python3

    def angel_trans(grad):
        rad = (grad *np.pi) / 180
        return rad


a simpele major frame in which the melody can play

.. code:: python3

    frame_dur = [0,2,4,5,7,9,11,12]
    frame_moll = [0,2,3,5,7,8,10,12]
    
    def roud_to_frame(frame, num):
        array = np.asarray(frame)
        listnr = (np.abs(frame - num)).argmin()
        return frame[listnr]

.. code:: python3

    def mod12(n):
        return n % 12
    
    def note_name(number):
        notes = "C C# D D# E F F# G G# A A# B C".split()
        return notes[mod12(number)]

.. code:: python3

    #--main--
    
    seq = ""
    for i in range(-90,270,20):
        sin = np.sin(angel_trans(i))
        normal = (sin+1)*6
        num = roud_to_frame(frame_moll, normal)
        note = note_name(num)
        seq = seq + note + " "

.. code:: python3

    print(seq)
    notes1 = NoteSeq(seq)
    midi = Midi(1, tempo=120)
    midi.seq_notes(notes1, track=0)
    midi.write("demo.mid")


.. parsed-literal::

    C C D D# F G G# A# C C C A# G# G F D# D C 


pyknon ex.2
-----------

.. code:: python3

    #=== section: music generation =================================
    def tune_A():
        notes1 = NoteSeq(      "C4 D E F G A B C''")   # Apostroph ' = "gestrichen" = Höhe der Oktave
        notes2 = NoteSeq("r1 r1 C4'' B' A G F E D C")   # r = rest = Pause; Zahl = Länge der Pause
        return notes1, notes2
    
    def tune_B():
        notes1 = NoteSeq("Db4- F#8 A Bb4")   # Zahl = Länge des Tones: 1=ganz, 4=Viertel
        notes2 = NoteSeq([Note(2, dur=1/4), Note(6, dur=1/8), Note(9, dur=1/8), Note(10, dur=1/4)])
        return notes1, notes2
    
    
    def generate_midi_pyknon():
        #--- choose the tune 
        notes1, notes2 = tune_A()         # <<<---- select a tune <<<------
    
        #--- squezze ir into a MIDI framework 
        m = Midi(2, tempo=120)     #
        m.seq_notes(notes1, track=0)
        m.seq_notes(notes2, track=1)
    
        #--- write the MIDI file 
        midi_file_name =  "myMidi.mid"       # set the name of the file
        m.write(midi_file_name)
        return midi_file_name
    
    
    generate_midi_pyknon()




.. parsed-literal::

    'myMidi.mid'



--------------

pyfluidsynth
------------

more or less an python api for fluidsynth direct sound output suports
several channels with diffrent instruments (Gneral-Midi) todo: ouput as
an audio file.

.. code:: python3

    import time
    import fluidsynth
    
    fs = fluidsynth.Synth()
    
    #fs.start()
    fs.start(driver="alsa")
    
    sfid = fs.sfload("/usr/share/sounds/sf3/MuseScore_General.sf3")
    fs.program_select(0, sfid, 0, 33)   #(tracknr , sondfontid, ??, instrumentnr)
    print(fs.channel_info(0))
    
    fs.noteon(0, 60, 30)
    fs.noteon(0, 67, 30)
    fs.noteon(0, 76, 30)
    
    time.sleep(1.0)
    
    fs.noteon(0, 60, 30)
    fs.noteon(0, 67, 30)
    fs.noteon(0, 76, 30)
    
    time.sleep(1.0)
    
    fs.noteoff(0, 60)
    fs.noteoff(0, 67)
    fs.noteoff(0, 76)
    
    time.sleep(1.0)
    
    fs.delete()


.. parsed-literal::

    (1, 0, 33, b'Fingered Bass')


Midi: Play and Generate audio-file
----------------------------------

For generating audio-files I use midi2audio.

midi2audio
~~~~~~~~~~

midi to audio converter with FluidSynth. But only over jack sound driver
in Linux.

| **When using play\_midi in Linux with Pulseaudio**
| --> with pulseaudio it is nessecary to change the source code of
  midi2audio:

.. code:: python3

    '''
    replace:
    def play_midi(self, midi_file):
        subprocess.call(['fluidsynth', '-i', self.sound_font, midi_file, '-r', str(self.sample_rate)])
        
    with:
    def play_midi(self, midi_file):
        subprocess.call(['fluidsynth', '-i', self.sound_font, midi_file, '-r', str(self.sample_rate), '-a', 'pulseaudio'])
    '''
    ''




.. parsed-literal::

    ''



otherwise FluidSyth can also used manualy. See below.

.. code:: python3

    from midi2audio import FluidSynth
    default_soundfont = '/usr/share/sounds/sf3/MuseScore_General.sf3'
    soundfont = default_soundfont
    
    def midi_play(midi_in, soundfont= default_soundfont):
        fs = FluidSynth(soundfont)
        fs.play_midi(midi_in)  # This runs FluidSyth with Jack. 
    
        
    def midi_audio(midi_in, name_out = 'none', soundfont= default_soundfont):
        fs = FluidSynth(soundfont)
        if name_out == 'none' :
            name_out = midi_in.replace('.mid', '.flac')
        else:
            name_out = name_out + '.flac'
            
        fs.midi_to_audio(midi_in, name_out)
        
        
    #midi_audio('scale.mid')
    midi_play('myMidi.mid')

.. raw:: html

    <audio controls="controls">
      <source src="https://raw.githubusercontent.com/schuhva/Music-Generation/master/doc/releases/1.03/scale.flac" type="audio/flac">
      Your browser does not support the <code>audio</code> element. 
    </audio>
    
https://raw.githubusercontent.com/schuhva/Music-Generation/master/doc/releases/1.03/scale.flac



FluidSynth manualy
~~~~~~~~~~~~~~~~~~

.. code:: python3

    import subprocess
    
    sound_font = '/usr/share/sounds/sf3/MuseScore_General.sf3'
    midi_file = 'scale.mid'
    sample_rate = 44100
    subprocess.call(['fluidsynth', '-i', sound_font, midi_file, '-r', str(sample_rate), '-a', 'pulseaudio'])




.. parsed-literal::

    0


