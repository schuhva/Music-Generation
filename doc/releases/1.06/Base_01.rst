
1.06 Rythem, Volumes and Ornaments
==================================

Integrating the **dur** and **volume** arguments of the **Note()**
funktion.

Adding **Ornaments** to the melody. The same Onaments appers each or
many notes. When a Melodic paatern is used several times on a diffrent
hight it's called a Sequence.

.. code:: python3

    from pyknon.genmidi import Midi
    from pyknon.music import Rest, Note, NoteSeq
    import numpy as np

Pyknon
------

There exist two diffrent notations one with the **Note()** function and
in a simpyfied **plain text** version

**Note(value , octave , dur , volume)**

-  value: integer, note hight in semitones, 0 = middel C = midi 60
-  octave: octave number
-  dur: duration, 0.25 = quarter note
-  volume: from 1 to 127

**Instruments:** Available are at lest the 128 General-Midi (GM)
Instruments. Depending on the sound-fonts there is a bigger choise. A
list of the GM instruments can be found here.
https://en.wikipedia.org/wiki/General\_MIDI#Program\_change\_events
Remeber to substract 1, as the list starts with 1 and not 0.

.. code:: python3

    major = [0,2,4,5,7,9,11,12]
    minor = [0,2,3,5,7,8,10,12]
    ryt_1 = [1/4 + 1/8 ,1/8]
    ryt_2 = [0.125,0.125,0.125, 0.125,0.125,0.125, 0.25,0.25,0.25,] # Rythem from west side Story: America
    var   = np.array([-1,0,2])
    
    def fade(start,end,steps):
        fade = np.around( np.linspace(start,end,num=steps))
        fade = fade.astype(int)
        return fade
    
    # tune_E with difrent instruments, and fading de volume
    def tune_F():    
        tune_name = 'tune_F'              # somtimes forming diatonic chords
        major2  = major[:-1] + major[::-1]                 # cut last element and reverse
        volumes = np.r_[ fade(30,110,8), fade(103,60,7)]   # creat volume track
        rythem  = np.r_[ np.tile(ryt_1, 7), [0.5]]
        
        notes1 = NoteSeq(            [Note(no-12, octave=5, dur=du, volume=vo) for no,du,vo in zip(major2,rythem,volumes)] )  # -12 = an octave deeper
        notes2 = NoteSeq( [Rest(0.5)] + [Note(no, octave=5, dur=du, volume=vo) for no,du,vo in zip(major2,rythem,volumes)] )
        notes3 = NoteSeq( [Rest(1)]   + [Note(no, octave=5, dur=du, volume=vo) for no,du,vo in zip(major2,rythem,volumes)] )
        notes = [notes1, notes2, notes3]
        instruments = [33, 56, 21]
        return notes, instruments,tune_name

**tune\_G**

-  Not anymore using the scale direclty. First creating an Index-Tune
   whitch is then convertet in to the tune with the notes.
-  adding an Ornament on each note of the scale. (Seqeuncing)
-  Using a rythmic-pattern instead of just quarter-notes.

.. code:: python3

    def tune_G():
        tune_name = 'tune_G' # ryt_2
        
        iscale = np.arange(1,9)   # index of a scale
        imelody = np.array([])    # creating index melody
        for i in iscale:                            # adding the Ornament on each note
            imelody = np.append(imelody, var + i)
        imelody = np.append(imelody, [5,3,1])
        imelody = imelody.astype(int)
        major2 = [-1]+major +[14,16]
        melody = [major2[i] for i in imelody] # creating the tune out of the index-tune
        
        rythem = np.tile(ryt_2, 3)
        volumes = np.int_(np.zeros(len(melody)) +100)
        
        notes1 = NoteSeq( [Rest(0.5)] + [Note(no, octave=5, dur=du, volume=vo) for no,du,vo in zip(melody,rythem,volumes)] )
        instruments = [66]
        notes = [notes1]
        return notes, instruments,tune_name


.. code:: python3

    
    def gen_midi():
    #     squezze into a MIDI framework
        notes, instruments, tune_name = tune_G() #  <--- select a tune  <<--     <<<<<<<<<--- select a tune -----
        nTracks = len(notes)
        
        m = Midi(number_tracks=nTracks, tempo=120, instrument=instruments)
        for iTrack in range(nTracks):
            m.seq_notes(notes[iTrack], track=iTrack)
    
        #--- write the MIDI file -----
        midi_file_name = tune_name +'.mid'   # set the name of the file
        m.write(midi_file_name)
        return midi_file_name

Midi: Play and Generate audio-file
----------------------------------

Externel players offered a better sound quality in comparison with
python liaberys. We use **VLC** and **Musescore**

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

.. code:: python3

    ######---  Main  ---######
    midi_file_name = gen_midi()
    
    midi_play(midi_file_name)
    #midi_audio(midi_file_name)
    #midi_png(midi_file_name)

.. raw:: html

    <br><audio controls="controls" src="https://raw.githubusercontent.com/schuhva/Music-Generation/master/doc/releases/1.06/tune_F.flac" type="audio/flac"></audio>
     tune_F
     
    <br><audio controls="controls" src="https://raw.githubusercontent.com/schuhva/Music-Generation/master/doc/releases/1.06/tune_G.flac" type="audio/flac"></audio>
     tune_G
     
    <br><img alt="self-Logo" src="https://raw.githubusercontent.com/schuhva/Music-Generation/master/doc/releases/1.06/tune_G-1.png">
     tune_G (the saxaphone is a transposing instrument)
     
     Unfortunately I couldn't print it as 6/8 time signature, as it should be.
     


 
