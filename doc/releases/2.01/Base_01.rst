
2.01 Controlled Random: Rests and Rhythm
========================================

Now we introduce random, starting with rests and rhythms. The random is
controlled, by giving a selection of possibilities. The user defines how
often each choice is selected.

.. code:: python3

    from pyknon.genmidi import Midi
    from pyknon.music import Rest, Note, NoteSeq
    import numpy as np

**Instruments:** Available are at lest the 128 General-Midi (GM)
Instruments. Depending on the sound-fonts there is a bigger choice. A
list of the GM instruments can be found here.
https://en.wikipedia.org/wiki/General\_MIDI#Program\_change\_events
Remember to subtract 1, as the list starts with 1 and not 0.

.. code:: python3

    major = [0,2,4,5,7,9,11,12]
    minor = [0,2,3,5,7,8,10,12]
    ryt_1 = [1/4 + 1/8 ,1/8]
    ryt_2 = [0.125,0.125,0.125, 0.125,0.125,0.125, 0.25,0.25,0.25,] # Rythem from west side Story: America
    var   = np.array([1,2,-1])
    var2  = np.array([0,2,-1])
    var3  = np.array([0,-1,2])
    
    def fade(start,end,steps):
        fade = np.around( np.linspace(start,end,num=steps))
        fade = fade.astype(int)
        return fade

**tune\_H:** Rests are generated by setting the volume of the note to
zero.

.. code:: python3

    def tune_H():
        tune_name = 'tune_H' 
        
        iscale = np.arange(1,9)   # index of a scale
        imelody = np.array([])    # creating index melody
        for i in iscale:                            # adding the Ornament on each note
            imelody = np.append(imelody, var + i)
        imelody = np.append(imelody, [5,3,1])
        imelody = imelody.astype(int)
        major2 = [-1]+major +[14,16]
        melody = [major2[i] for i in imelody] # creating the tune out of the index-tune
        melody_len = len(melody)
        
        volume= np.array([0, 110], dtype=int)       # this are the allowed volumes of thenotes
        prob_volume = np.array([1,3])            # this are the probabilities how often each volume will occure
        prob_volume = prob_volume/np.sum(prob_volume) 
        volumes = np.r_[np.random.choice(volume, size=melody_len, p=prob_volume)]
        
        rythem = np.tile(ryt_2, 3)
        
        notes1 = NoteSeq( [Rest(0.5)] + [Note(no, octave=5, dur=du, volume=vo) for no,du,vo in zip(melody,rythem,volumes)] )
        instruments = [25]
        notes = [notes1]
        return notes, instruments,tune_name


.. raw:: html

    <br><audio controls="controls" src="https://raw.githubusercontent.com/schuhva/Music-Generation/master/doc/releases/2.01/tune_H.flac" type="audio/flac"></audio>
     tune_H     <br><br><br>
     

**tune\_I:** The note-duration is defined by controlled random

.. code:: python3

    def tune_I():
        tune_name = 'tune_I' 
        
        iscale = np.arange(1,9)   # index of a scale
        imelody = np.array([])    # creating index melody
        for i in iscale:                            # adding the Ornament on each note
            imelody = np.append(imelody, var2 + i)
        imelody = np.append(imelody, [5,3,1])
        imelody = imelody.astype(int)
        major2 = [-1]+major +[14,16]
        melody = [major2[i] for i in imelody] # creating the tune out of the index-tune
        melody_len = len(melody)
        
        volume= np.array([0, 110], dtype=int)       # this are the allowed volumes of thenotes
        prob_volume = np.array([1,5])            # this are the probabilities how often each volume will occure
        prob_volume = prob_volume/np.sum(prob_volume) 
        volumes = np.r_[np.random.choice(volume, size=melody_len, p=prob_volume)]
        
        
        duration= np.array([1/8, 1/4,1/2])              # this are the allowed durations of the notes
        prob_duration = np.array([4,2,1])            # this are the probabilities how often each will occure
        prob_duration = prob_duration/np.sum(prob_duration) 
        rythem = np.r_[np.random.choice(duration, size=melody_len, p=prob_duration)]
        
        
        notes1 = NoteSeq( [Note(no+12, octave=5, dur=du, volume=vo) for no,du,vo in zip(melody,rythem,volumes)] )
        instruments = [68]
        notes = [notes1]
        return notes, instruments,tune_name

.. raw:: html

    <br><audio controls="controls" src="https://raw.githubusercontent.com/schuhva/Music-Generation/master/doc/releases/2.01/tune_I.flac" type="audio/flac"></audio>
     tune_I     
     
     <br><img src="https://raw.githubusercontent.com/schuhva/Music-Generation/master/doc/releases/2.01/tune_I-1.png">
     tune_I   <br><br><br>

**tune\_J:** Creating two tracks with the same melody but different
Rests and Rhythm

.. code:: python3

    def ran_duration(duration, prob_duration, melody_len):    
        duration= np.asarray(duration)                  # this are the allowed durations of the notes
        prob_duration = np.asarray(prob_duration)       # this are the probabilities how often each will occure
        prob_duration = prob_duration/np.sum(prob_duration) 
        rythem = np.r_[np.random.choice(duration, size=melody_len, p=prob_duration)]
        return rythem
        
    def ran_volume(volume, prob_volume, melody_len):
        volume = np.asarray(volume, dtype=int)         # this are the allowed volumes of thenotes
        prob_volume = np.asarray(prob_volume)          # this are the probabilities how often each volume will occure
        prob_volume = prob_volume/np.sum(prob_volume) 
        volumes = np.r_[np.random.choice(volume, size=melody_len, p=prob_volume)]
        return volumes
        
    
    def tune_J():
        tune_name = 'tune_J' 
        
        iscale = np.arange(1,9)   # index of a scale
        imelody = np.array([])    # creating index melody
        for i in iscale:                            # adding the Ornament on each note
            imelody = np.append(imelody, var3 + i)
        imelody = np.append(imelody, [5,3,1])
        imelody = imelody.astype(int)
        major2 = [-1]+major +[14,16]
        melody = [major2[i] for i in imelody] # creating the tune out of the index-tune
        melody_len = len(melody)
        
        rythem1 = ran_duration([1/8, 1/4,1/2], [4,2,1], melody_len)
        rythem2 = ran_duration([1/8, 1/4,1/2], [4,2,1], melody_len)
        volumes1 = ran_volume([0,100], [1,4], melody_len )
        volumes2 = ran_volume([0,120], [1,4], melody_len )
    
        notes1 = NoteSeq( [Note(no+4,octave=5, dur=du, volume=vo) for no,du,vo in zip(melody,rythem1,volumes1)] )
        notes2 = NoteSeq( [Note(no-8,  octave=5, dur=du, volume=vo) for no,du,vo in zip(melody,rythem2,volumes2)] )
        instruments = [56, 58]
        notes = [notes1,notes2]
        return notes, instruments,tune_name

.. raw:: html

    <br><audio controls="controls" src="https://raw.githubusercontent.com/schuhva/Music-Generation/master/doc/releases/2.01/tune_J.flac" type="audio/flac"></audio>
     tune_J     
     
     <br><img src="https://raw.githubusercontent.com/schuhva/Music-Generation/master/doc/releases/2.01/tune_J-1.png">
     tune_J  <br><br><br>

.. code:: python3

    
    def gen_midi():
    #     squezze into a MIDI framework
        notes, instruments, tune_name = tune_I() #  <--- select a tune  <<--     <<<<<<<<<--- select a tune -----
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

