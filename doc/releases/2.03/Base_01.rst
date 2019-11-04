
2.03 Melody by Intervals
========================

In the previous example the melody was completely random and did not
sound like a melody for us. In composed music, the melody often only
makes small steps of seconds or thirds. So in this Version the melody is
created by intervals. Note duration and rests are set by controlled
random.

.. code:: python3

    from pyknon.genmidi import Midi
    from pyknon.music import Rest, Note, NoteSeq
    import numpy as np

**Instruments:** Available are at lest the 128 General-Midi (GM)
Instruments. Depending on the sound-fonts there is a bigger choice. A
list of the GM instruments can be found here.
https://jazz-soft.net/demo/GeneralMidi.html

.. code:: python3

    major = np.array([-12, -10, -8, -7, -5, -3, -1, 0, 2, 4, 5, 7, 9, 11, 12, 14, 16])
    minor = np.array([-12, -10, -9, -7, -5, -4, -2, 0, 2, 3, 5, 7, 8, 10, 12, 14, 15])  
    var   = np.array([1,2,-1])
    var2  = np.array([0,2,-1])
    var3  = np.array([0,-1,2])
    
    def fade(start,end,steps):
        fade = np.around( np.linspace(start,end,num=steps))
        fade = fade.astype(int)
        return fade
    
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

**tune\_L:** In this example we are not going to create the melody
directly. Instead we control **the interval of the next note** of the
melody. Starting with a second and a third up and downwards and the
Perfect unison. The note durations are quarters for the moment.

The size of each interval is created by controlled random. Every
interval has an individual probability.

.. code:: python3

    def tune_L():
        tune_name = 'tune_L'  
        np.random.seed(5)
        melody_len = 32
        scale = major
        i_tone_zero = np.argwhere(scale==0)[0]
        
        interval = np.asarray([-2,-1, 0, 1, 2])            # Possible interval
        prob_interval = np.asarray([2, 4, 1, 4, 2])         # Probability of each interval
        prob_interval = prob_interval/np.sum(prob_interval)
        intervals = np.r_[np.random.choice(interval, size=melody_len, p=prob_interval)] 
        
        imelody1 = i_tone_zero + np.cumsum(intervals)
        melody1 = scale[imelody1]
    
        rythem1 = ran_duration([1/8, 1/4,1/2], [0,2,0], melody_len)
        volumes1 = ran_volume([0,100], [0,4], melody_len )
    
        notes1 = NoteSeq( [Note(no+4,octave=5, dur=du, volume=vo) for no,du,vo in zip(melody1,rythem1,volumes1)] )
        instruments = [69]
        notes = [notes1]
        return notes, instruments,tune_name

.. raw:: html

    <br><audio controls="controls" src="https://raw.githubusercontent.com/schuhva/Music-Generation/master/doc/releases/2.03/tune_L.flac" type="audio/flac"></audio>
     tune_L     
     
     <br><img src="https://raw.githubusercontent.com/schuhva/Music-Generation/master/doc/releases/2.03/tune_L-1.png">
     tune_L  <br><br><br>

**tune\_M:** Same as tune\_L but with two voices and creating the
**int\_vlt function**

.. code:: python3

    def intvl_melody(intvl, prob_intvl, melody_len):  #Interval Melody  
        intvl = np.asarray(intvl)            # Possible interval
        prob_intvl = np.asarray(prob_intvl)         # Probability of each interval
        prob_intvl = prob_intvl/np.sum(prob_intvl)
        intervals = np.r_[np.random.choice(intvl, size=melody_len, p=prob_intvl)] 
        imelody = np.cumsum(intervals)
        return imelody
         
    
    def tune_M():
        tune_name = 'tune_M'  
        np.random.seed(10)
        melody_len = 40
        scale = major
        i_tone_zero = np.argwhere(scale==0)[0]
        
        melody1 = scale[ i_tone_zero + intvl_melody([-2,-1, 0, 1, 2],[2, 4, 1, 4, 2], melody_len)]
        rythem1 = ran_duration([1/8, 1/4,1/2], [1,2,1], melody_len)
        volumes1 = ran_volume([0,120], [0,4], melody_len )
        
        melody2 = scale[ i_tone_zero + intvl_melody([-2,-1, 0, 1, 2],[2, 4, 1, 4, 2], melody_len)]
        rythem2 = ran_duration([1/8, 1/4,1/2], [1,2,1], melody_len)
        volumes2 = ran_volume([0,100], [0,4], melody_len )
    
        notes1 = NoteSeq( [Note(no,octave=6, dur=du, volume=vo) for no,du,vo in zip(melody1,rythem1,volumes1)] )
        notes2 = NoteSeq( [Note(no,octave=5, dur=du, volume=vo) for no,du,vo in zip(melody2,rythem2,volumes2)] )
        instruments = [110,70]
        notes = [notes1,notes2]
        return notes, instruments,tune_name

.. raw:: html

    <br><audio controls="controls" src="https://raw.githubusercontent.com/schuhva/Music-Generation/master/doc/releases/2.03/tune_M.flac" type="audio/flac"></audio>
     tune_M     
     
     <br><img src="https://raw.githubusercontent.com/schuhva/Music-Generation/master/doc/releases/2.03/tune_M-1.png">
     tune_M  <br><br><br>

.. code:: python3

    
    def gen_midi():
    #     squezze into a MIDI framework
        notes, instruments, tune_name = tune_M() #  <--- select a tune  <<--     <<<<<<<<<--- select a tune -----
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

External players offered a better sound quality in comparison with
python libraries. We use **VLC** and **Musescore**

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
