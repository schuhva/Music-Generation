
1.02
====

Trying out diffrent libraries which can generate sound in python

pyknon
------

1. output only as midi
2. has many features

.. code:: python3

    from pyknon.genmidi import Midi
    from pyknon.music import NoteSeq
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


midi2audio
----------

midi to audio converter with FluidSynth

.. code:: python3

    from midi2audio import FluidSynth
    fs = FluidSynth('/usr/share/sounds/sf3/MuseScore_General.sf3')
    #fs.play_midi('demo.mid')  # This runs FluidSyth with Jack. 
    fs.midi_to_audio('demo.mid', 'output.flac')

.. raw:: html

    <audio controls="controls">
      <source src="https://raw.githubusercontent.com/schuhva/Music-Generation/master/doc/releases/1.02/output.flac" type="audio/flac">
      Your browser does not support the <code>audio</code> element. 
    </audio>
    
https://raw.githubusercontent.com/schuhva/Music-Generation/master/doc/releases/1.02/output.flac



FluidSynth manualy
------------------

problem with midi2audio: onyl over jack sound driver attmpt to change to
alsa failed

.. code:: python3

    import subprocess
    
    sound_font = '/usr/share/sounds/sf3/MuseScore_General.sf3'
    midi_file = 'demo.mid'
    sample_rate = 44100
    subprocess.call(['fluidsynth', '-i', sound_font, midi_file, '-r', str(sample_rate), '-a', 'pulseaudio'])




.. parsed-literal::

    0




