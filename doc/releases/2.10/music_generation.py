from pyknon.genmidi import Midi
from pyknon.music import Rest, Note, NoteSeq
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from datetime import date


# [[[[[[[[[[[[[[[[[[[   -- Functions for Music Generation --    ]]]]]]]]]]]]]]]]]]]

def scale_create(tones):
    tones = np.asarray(tones)   # tones which form chord or scale in the first octave (0-11)
    if any(tones > 11):             # tones over one octave?
        tones = np.mod(tones,12)    # set the thones in one octave
        tones = np.sort(tones)      # sort the tones new
        tones = np.unique(tones)    # remove duplicate tones
    octave = np.repeat( np.linspace(0,108, num=10), len(tones))
    scale = np.add( octave, np.tile(tones, 10)) # add element wise octave and note
    return scale.astype(int)
    
def fade(start,end,steps): 
    fade = np.around( np.linspace(start,end,num=steps))
    fade = fade.astype(int)
    return fade

def ran_volume(volume, prob_volume, melody_len):
    volume = np.asarray(volume, dtype=int)         # this are the allowed volumes of thenotes
    prob_volume = np.asarray(prob_volume)          # this are the probabilities how often each volume will occure
    prob_volume = prob_volume/np.sum(prob_volume) 
    volumes = np.r_[np.random.choice(volume, size=melody_len, p=prob_volume)]
    return volumes

#   liniar_range: Generates an range in which the instrument can play. 
def liniar_range(r_start, r_top, r_edge, r_end): # acceptance range of the instrument 
    h = 100 # hight of acceptance function
    a_range = np.zeros(121, dtype=int)  # only to midi =120 as 127 is not a complete octave
    np.put(a_range, range(r_start,r_top),  np.linspace(0,h, num=(r_top -r_start)) )
    np.put(a_range, range(r_top, r_edge),  np.linspace(h,h, num=(r_edge-r_top  )) )
    np.put(a_range, range(r_edge, r_end),  np.linspace(h,0, num=(r_end -r_edge )) )
    return a_range
    
#   i_last_note: finds de i value of the last not in the actual scale.
def i_last_note(note, scale):
    i_note = (np.abs(scale - note)).argmin()
    return i_note

#   intvl_next is a modification of intvl_melody. But it does only creats one interval and not an array/melody in one time.
def intvl_next(intvl, prob_intvl):  #singel interval
    intvl = np.asarray(intvl)            # Possible interval
    prob_intvl = np.asarray(prob_intvl)         # Probability of each interval
    prob_intvl = prob_intvl/np.sum(prob_intvl)
    interval = np.random.choice(intvl, size=1, p=prob_intvl)
    return interval[0]

#   acceptance: accepts and refuses proposed nots with Metropolis-Hasting Algorythem.
#     x is the value in the aceptance range of the current note, while x_new is it from the proposoal note
def acceptance(x, x_new):
    if x_new < 1:
        if x < 1: print('start_note not in range') ; x = start_note_not_in_range
    quot = x_new/x
    if quot >= 1: return True
    if np.random.uniform(0,1)< quot: return True
    else: return False
    
def acceptance_melody(intvl, prob_intvl, pattern, start_note, a_range, notenr, rythem):
    melody = np.zeros(notenr, dtype=int)
    cum_rythem = np.cumsum(rythem) *4
    cum_rythem = np.concatenate(([0],cum_rythem))[:-1] # add 0 at beginig remove last element
    scale_change = pattern[:,0]
    scale_nr =0
    scale = pattern[scale_nr,1]
    melody[0] = scale[i_last_note(start_note,scale)]
    
    for npn in range(1, notenr):  #npn: note per note (index)      
        scale_nr = np.ravel(np.argwhere(scale_change <= cum_rythem[npn-1])) [-1]     
        scale = pattern[scale_nr,1]

        accept = False    
        while not accept:       # aslong acept == False
            inote = i_last_note(melody[npn-1],scale)
            inote_next = inote + intvl_next(intvl, prob_intvl)         # add current not with Proposition
            accept_val = a_range[[melody[(npn-1)],scale[inote_next]]]  # get acceptance values
            accept = acceptance(accept_val[0],accept_val[1])
        melody[npn] = scale[inote_next]
    return melody

#   plot_range: plot all ranges together
def plot_range(ranges,labels,title):
    fig, ax = plt.subplots()
    plt.xlabel('Midi Note')
    plt.ylabel('Acceptance')
    plt.title(title)

    for a_range, lab in zip(ranges,labels):
        ax.plot(range(121), a_range,label= lab )
    ax.vlines(x=np.linspace(0,108, num=10), ymin=0, ymax=10, color='grey', label='Octaves',linewidth=1) # plot octaves
    plt.legend()
    plt.show()
    
    
    
    
# [[[[[[[[[[[[[[[[[[[   -- Functions for Meteo Transformation --    ]]]]]]]]]]]]]]]]]]]




# [[[[[[[[[[[[[[[[[[[   -- Functions for Sound generation --    ]]]]]]]]]]]]]]]]]]]

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
