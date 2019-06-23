
1.02
====

Trying out diffrent libraries which can generate sound in python

.. code:: ipython3

    from pyknon.genmidi import Midi
    from pyknon.music import NoteSeq
    import numpy as np

.. code:: ipython3

    def angel_trans(grad):
        rad = (grad *np.pi) / 180
        return rad


.. code:: ipython3

    frame_dur = [0,2,4,5,7,9,11]     #[1,3,5,6,8,10,12]
    
    def roud_to_frame(frame, num):
        array = np.asarray(frame)
        listnr = (np.abs(frame - num)).argmin()
        return frame[listnr]

.. code:: ipython3

    def mod12(n):
        return n % 12
    
    def note_name(number):
        notes = "C C# D D# E F F# G G# A A# B".split()
        return notes[mod12(number)]

.. code:: ipython3

    #--main--
    
    seq = ""
    for i in range(-90,270,20):
        sin = np.sin(angel_trans(i))
        normal = (sin+1)*6
        num = roud_to_frame(frame_dur, normal)
        note = note_name(num)
        seq = seq + note + " "

.. code:: ipython3

    print(seq)
    notes1 = NoteSeq(seq)
    midi = Midi(1, tempo=120)
    midi.seq_notes(notes1, track=0)
    midi.write("demo.mid")


.. parsed-literal::

    C C D D F G A B B B B B A G F D D C 


.. code:: ipython3

    import time
    import fluidsynth
    
    fs = fluidsynth.Synth()
    
    #fs.start()
    fs.start(driver="alsa")
    
    sfid = fs.sfload("/usr/share/sounds/sf3/MuseScore_General.sf3")
    fs.program_select(0, sfid, 35, 0)
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

    (0, 0, 0, b'')


.. code:: ipython3

    from midi2audio import FluidSynth
    fs = FluidSynth('/usr/share/sounds/sf3/MuseScore_General.sf3')
    #fs.play_midi('demo.mid')
    fs.midi_to_audio('demo.mid', 'output.flac')

.. raw:: html

    <audio controls="controls">
      <source src="https://raw.githubusercontent.com/schuhva/Music-Generation/master/doc/releases/1.01/output.flac" type="audio/flac">
      Your browser does not support the <code>audio</code> element. 
    </audio>
    
https://raw.githubusercontent.com/schuhva/Music-Generation/master/doc/releases/1.01/output.flac



