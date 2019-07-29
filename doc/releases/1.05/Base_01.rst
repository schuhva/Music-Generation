
1.05 Instruments
================

Adding **instruments** to the tracks and improving **gen\_midi( )** such
that the number of tracks does not mater.

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

**Instruments:** Available are at least the 128 General-Midi (GM)
Instruments. Depending on the sound-fonts there is a bigger choise. A
list of the GM instruments can be found here.
https://en.wikipedia.org/wiki/General\_MIDI#Program\_change\_events
Remeber to substract 1 as the list starts with 1 and not 0.

.. code:: python3

    major = [0,2,4,5,7,9,11,12]
    minor = [0,2,3,5,7,8,10,12]
    
    
    def tune_D():    
        tune_name = 'tune_D'   # A row of major chords
        notes1 = NoteSeq( [Note(no) for no in major] )
        notes2 = NoteSeq( [Note(no +4) for no in major] )
        notes3 = NoteSeq( [Note(no +7) for no in major] )
        notes = [notes1, notes2, notes3]
        instruments = [12, 12, 12]
        return notes, instruments,tune_name
    
    def tune_E():    
        tune_name = 'tune_E'            # somtimes forming diatonic chords
        major2 = major[:-1] + major[::-1]  # cut last element and adding the reverse
        notes1 = NoteSeq( [Note(no) for no in major2] )
        notes2 = NoteSeq( [Rest(0.5)] + [Note(no) for no in major2] )
        notes3 = NoteSeq( [Rest(1)]   + [Note(no) for no in major2] )
        notes = [notes1, notes2, notes3]
        instruments = [66, 42, 19]
        return notes, instruments,tune_name
    
    
    
    def gen_midi():
    #     squezze into a MIDI framework
        notes, instruments, tune_name = tune_E() #  <--- select a tune  <<--     <<<<<<<<<--- select a tune -----
        nTracks = len(notes)
        
        m = Midi(number_tracks=nTracks, tempo=100, instrument=instruments)
        for iTrack in range(nTracks):
            m.seq_notes(notes[iTrack], track=iTrack)
    
        #--- write the MIDI file -----
        midi_file_name = tune_name +'.mid'   # set the name of the file
        m.write(midi_file_name)
        return midi_file_name

Midi: Play and Generate audio-file
----------------------------------

Externel players offered a better sound quality in comparison with
python liaberys. We uses **VLC** and **Musescore**

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
    midi_audio(midi_file_name)
    midi_png(midi_file_name)

.. raw:: html

    <br><audio controls="controls" src="https://raw.githubusercontent.com/schuhva/Music-Generation/master/doc/releases/1.05/tune_D.flac" type="audio/flac"></audio>
     tune_D
     
    <br><audio controls="controls" src="https://raw.githubusercontent.com/schuhva/Music-Generation/master/doc/releases/1.05/tune_E.flac" type="audio/flac"></audio>
     tune_E
     
    <br><img src="https://raw.githubusercontent.com/schuhva/Music-Generation/master/doc/releases/1.05/tune_E-1.png">
     tune_E (the saxaphone is a transposing instrument)
     


 
