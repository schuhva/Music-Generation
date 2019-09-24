
2.05 Stay in Instument Range
============================

In the Previous exampel the melody could get **off track** and get
further away from the **good sounding instument range.** It was also
possile that it left the scale and created an error.

.. code:: python3

    from pyknon.genmidi import Midi
    from pyknon.music import Rest, Note, NoteSeq
    import numpy as np
    import matplotlib.pyplot as plt

**Instruments:** Available are at lest the 128 General-Midi (GM)
Instruments. Depending on the sound-fonts there is a bigger choise. A
list of the GM instruments can be found here.
https://jazz-soft.net/demo/GeneralMidi.html



.. code:: python3

    from IPython.display import Image
    Image("Midi_range.jpg")




.. image:: output_4_0.jpeg



.. code:: python3

    major = np.array([ 0, 2, 4, 5, 7, 9, 11])
    minor = np.array([ 0, 2, 3, 5, 7, 8, 10])  
    C7 = np.array([ 0, 4, 7, 10]) 
    var   = np.array([1,2,-1])
    var2  = np.array([0,2,-1])
    var3  = np.array([0,-1,2])
    
    def scale_create(tones):   # Creats a scale over the hole midi Range from C-2 to C-7 (midi notes: 0-120)
        tones = np.asarray(tones)   # tones which form chord or scale in the first octave (0-11)
        octave = np.repeat( np.linspace(0,108, num=10), len(tones))
        scale = np.add( octave, np.tile(tones, 10)) # add element wise octave and note
        return scale.astype(int)
        
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
    
    def intvl_melody(intvl, prob_intvl, melody_len):  #Interval Melody  
        intvl = np.asarray(intvl)            # Possible interval
        prob_intvl = np.asarray(prob_intvl)         # Probability of each interval
        prob_intvl = prob_intvl/np.sum(prob_intvl)
        intervals = np.r_[np.random.choice(intvl, size=melody_len, p=prob_intvl)] 
        imelody = np.cumsum(intervals)
        return imelody

**liniar\_range:** Generates an range in which the instrument can play.

.. code:: python3

    def liniar_range(r_start, r_top, r_edge, r_end): # acceptance range of the instrument 
        h = 100 # hight of acceptance function
        a_range = np.zeros(121, dtype=int)  # only to midi =120 as 127 is not a complete octave
        np.put(a_range, range(r_start,r_top),  np.linspace(0,h, num=(r_top -r_start)) )
        np.put(a_range, range(r_top, r_edge),  np.linspace(h,h, num=(r_edge-r_top  )) )
        np.put(a_range, range(r_edge, r_end),  np.linspace(h,0, num=(r_end -r_edge )) )
    
        fig, ax = plt.subplots()
        ax.plot(range(121), a_range)
        plt.show()
        return
        
    liniar_range(36,48,72,84)
    




.. image:: output_7_0.png


**i\_last\_note:** finds de i value of the last not in the actual scale.

.. code:: python3

    def i_last_note(melody, scale):
        try: 
            i_note = np.argwhere(scale== melody[-1])[0]
        except:
            print('not same scale')
            
        
        return i_note

.. code:: python3

    def intvl_next(intvl, prob_intvl):  #singel interval
        intvl = np.asarray(intvl)            # Possible interval
        prob_intvl = np.asarray(prob_intvl)         # Probability of each interval
        prob_intvl = prob_intvl/np.sum(prob_intvl)
        interval = np.r_[np.random.choice(intvl, size=1, p=prob_intvl)]
        return interval
    
    intvl_next([-2,-1, 0, 1, 2],[2, 4, 1, 4, 2])


.. parsed-literal::

    [-1]


**tune\_P:** Changing the scale creating methode.

.. code:: python3

    def tune_P():
        tune_name = 'tune_P'  
        np.random.seed(23)
        melody_len = 40
        scale = scale_create(C7)
        i_tone_zero = np.argwhere(scale==60)[0]
        
        melody1 = scale[4+ i_tone_zero + intvl_melody([-2,-1, 0, 1, 2],[2, 4, 1, 4, 2], melody_len)]
        rythem1 = ran_duration([1/8, 1/4,1/2], [1,2,1], melody_len)
        volumes1 = ran_volume([0,120], [1,5], melody_len )
        
        melody2 = scale[ i_tone_zero + intvl_melody([-2,-1, 0, 1, 2],[4, 2, 1, 2, 4], melody_len)]
        rythem2 = ran_duration([1/8, 1/4,1/2], [1,2,1], melody_len)
        volumes2 = ran_volume([0,100], [1,6], melody_len )
    
        melody3 = scale[-6+ i_tone_zero + intvl_melody([-1, 0, 1],[2, 1, 2], melody_len)]
        rythem3 = ran_duration([1/8, 1/4,1/2], [1,2,1], melody_len)
        volumes3 = ran_volume([0,100], [0,4], melody_len )
    
        notes1 = NoteSeq( [Note(no,octave=0, dur=du, volume=vo) for no,du,vo in zip(melody1,rythem1,volumes1)] )
        notes2 = NoteSeq( [Note(no,octave=0, dur=du, volume=vo) for no,du,vo in zip(melody2,rythem2,volumes2)] )
        notes3 = NoteSeq( [Note(no,octave=0, dur=du, volume=vo) for no,du,vo in zip(melody3,rythem3,volumes3)] )
        
        instruments = [60,3,32]
        notes = [notes1,notes2,notes3]
        return notes, instruments,tune_name

.. raw:: html

    <br><audio controls="controls" src="https://raw.githubusercontent.com/schuhva/Music-Generation/master/doc/releases/2.04/tune_O.flac" type="audio/flac"></audio>
     tune_     
     
     <br><img src="https://raw.githubusercontent.com/schuhva/Music-Generation/master/doc/releases/2.03/tune_M-1.png">
     tune_M  <br><br><br>

.. code:: python3

    
    def gen_midi():
    #     squezze into a MIDI framework
        notes, instruments, tune_name = tune_O() #  <--- select a tune  <<--     <<<<<<<<<--- select a tune -----
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
python liaberys. We use **VLC** and **Musescore**. The **soundfont** for
the VLC player is defined over the command line. For Musescore through
the Gui in the preferences.

.. code:: python3

    import subprocess
    default_soundfont = '/usr/share/sounds/sf3/MuseScore_General.sf3'
    
    def midi_play(midi_in, soundfont= default_soundfont):
        subprocess.call(['cvlc', midi_in , 'vlc://quit', '--soundfont', '/home/viturin/-vitis/Documents/MuseScore2/Soundfonts/Compifont_13082016.sf2'])   # cvlc = vlc without gui
        
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
        subprocess.call(['mscore', '-o', name_out, '-T', '2', midi_in]) # -o = export as , -T 2 = cut page with 2 pixel

.. code:: python3

    ######---  Main  ---######
    midi_file_name = gen_midi()
    
    midi_play(midi_file_name)
    midi_audio(midi_file_name)
    midi_png(midi_file_name)
