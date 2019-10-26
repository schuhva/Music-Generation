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
    
def ran_duration(duration, prob_duration, melody_len, end_dur):    
    duration= np.asarray(duration)                  # this are the allowed durations of the notes
    prob_duration = np.asarray(prob_duration)       # this are the probabilities how often each will occure
    prob_duration = prob_duration/np.sum(prob_duration)
    cumsum, melody_len, rythem = 0, melody_len/4 , np.asarray([])  #melody_len/4 as note values are quarter
    while cumsum < melody_len:
        note_len = np.random.choice(duration, p=prob_duration)
        cumsum = cumsum + note_len
        rythem = np.append(rythem,note_len)
    if end_dur != 0:  
        rythem = np.append(rythem,end_dur)
    return rythem , len(rythem)

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

#   pattern_gen takes the chord pattern (scales): it reapeats the pattern as long the melody is, and generates the beat number where the chords change. 
# it also adds the end pattern
def pattern_gen(scales,end_scale, melody_len):
    bpb = 4  # beats per bar
    
#--Add note to chord
    scales = note_to_chord(scales)
    end_scale = note_to_chord(end_scale)
    
#--scales  
    factor = int(np.trunc(melody_len/(np.sum(scales[:,0]) * bpb)) + 1) # factor rounded up: how many times is the pattern used
    change_times = np.cumsum(np.tile(scales[:,0],factor)) * bpb        # create change time list with factor
    change_times = np.concatenate((np.asarray([0]),change_times))[:-1] # add 0 at beginig remove last element
    
    for i in range(len(scales)):          # send scales to scale_create
        scales[i,1] = scale_create(scales[i,1])
    pattern = np.tile(scales,(factor,1))   # tile the scales as long the melody is
    pattern[:,0] = change_times            #insert change_times into scales
    
#--end_scales 
    end_times = melody_len - np.cumsum(( end_scale[:,0]*bpb )[::-1])[::-1]   # reversed cumsum subtracted of melody_len
    end_scale[:,0] = end_times              #insert end_times into en_scale
    for i in range(len(end_scale)):         # send end_scale to scale_create
        end_scale[i,1] = scale_create(end_scale[i,1])

#--merge
    pattern = np.delete(pattern, np.argwhere(pattern[:,0] >= end_scale[0,0]) ,0) # remove unneeded scales
    pattern = np.concatenate((pattern,end_scale),axis=0)
    pattern = np.delete(pattern, np.argwhere(pattern[:,0] >= melody_len) ,0)     # remove if end is 0 bars
    return pattern
    
#   transforming the note name into a midi number. Add the scale with this nuber to the correct chord.
def note_to_chord(input_s):
    
    tone_dic = {           'C' : 0 , 'C#' : 1 , 
                'Db' : 1 , 'D' : 2 , 'D#' : 3 ,
                'Eb' : 3 , 'E' : 4 , 'E#' : 5 ,
                'Fb' : 4 , 'F' : 5 , 'F#' : 6 ,
                'Gb' : 6 , 'G' : 7 , 'G#' : 8 ,
                'Ab' : 8 , 'A' : 9 , 'A#' :10 ,
                'Bb' : 10, 'B' :11 , 'B#' :12 ,
                'Cb' : 11                      }
    
    input_s =np.asarray(input_s)
    le = len(input_s)
    out_s = [[0,1]]*le
    
    for sps in range(le):
        note = input_s[sps,1]
        nr = tone_dic[note]
        out_s[sps]= [input_s[sps,0]  ,   input_s[sps,2] + nr]
        
    out_s = np.asarray(out_s)
    return out_s

   
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



# [[[[[[[[[[[[[[[[[[[   -- Functions for Meteo Music --    ]]]]]]]]]]]]]]]]]]]


def meteo_melody(meteo, pattern, start_note, notenr, rythem,mpb):
    melody = np.zeros(notenr, dtype=int)
    cum_rythem = np.cumsum(rythem) *4             
    cum_rythem = np.concatenate(([0],cum_rythem)) # add 0 at beginig 
    
    scale_change = pattern[:,0]
    scale_nr =0
    scale = pattern[scale_nr,1]
    melody[0] = scale[i_last_note(start_note,scale)]
    
    for npn in range(1, notenr):  #npn: note per note (index)      
        
        scale_nr = np.ravel(np.argwhere(scale_change <= cum_rythem[npn-1])) [-1]     
        scale = pattern[scale_nr,1]
        
        # find interval
        met_resolution = 10
        inter = np.asarray([cum_rythem[npn-1], cum_rythem[npn]])  # get beat_nr's 
        inter = np.round((inter*mpb)/met_resolution).astype(int)  # calulate index of the data array
        intvl = meteo[inter[1]] - meteo[inter[0]]                 # take the diffrence of the data
        intvl = np.round(intvl).astype(int)                       # round to an int
        
        inote_befor = i_last_note(melody[npn-1],scale)    # get i in the scale of the last note
        inote = inote_befor + intvl                       # calculate i in scale of note    
        melody[npn] = scale[inote]                        # set in to melody
         
    plt.plot(cum_rythem[1:],melody) ; plt.xlabel= ('beat nr.'); plt.ylabel=('midi note nr')
    return melody
    
    # Creates a regular drumm track by definig a rythmic, note and volume pattern
def drum(rythems,notes,volumes,melody_len):
    ryth_rep = int((melody_len/(np.sum(rythems)*4))+1)      # calculate repeat factor
    rythem = np.tile(rythems,ryth_rep)                      # tile  
    rythem = np.delete(rythem, np.argwhere(np.cumsum(rythem)*4 >= melody_len))  # delete not used notes
    note_nr = len(rythem)
    
    melody_rep = int(note_nr/len(notes)+1)      # calculate repeat factor
    melody = np.tile(notes,melody_rep)          # tile  
    melody = melody[:note_nr]                   # delete not used notes
    
    volume_rep = int(note_nr/len(volumes)+1)    # calculate repeat factor
    volume = np.tile(volumes,volume_rep)        # tile  
    volume = volume[:note_nr]                   # delete not used notes
    return melody, rythem, volume


    #Generates out of meteo data a Volume track
def met_vol(meteo, add, max_vol, rythem, mpb):
    met_resolution = 10 
    cum_ryth = np.concatenate((np.asarray([0]),np.cumsum(rythem)))[:-1]   # add 0 at beginig remove last element
    i_data = (cum_ryth *4* (mpb /met_resolution)).astype(int)               # calculate index of the data
    volumes = meteo[i_data].astype(int)                 # fill in meteo data
    volumes = volumes + add                             # add 
    volumes = np.minimum(volumes, max_vol)              # set values bigger than 127 to 127 or max_vol
    return volumes

     # Mutes and unmutes voices dependet of the meteo input data. on_range defines when a voice plays
def on_off(meteo, on_range, volumes, rythem, mpb):
    met_resolution = 10 
    cum_ryth = np.concatenate((np.asarray([0]),np.cumsum(rythem)))[:-1]   # add 0 at beginig remove last element
    i_data = (cum_ryth*4 * (mpb /met_resolution)).astype(int)               # calculate index of the data
    for npn in range(len(i_data)):                  
        value = meteo[ i_data[npn] ]                  # get value of the meteo data
        if on_range[0] < value < on_range[1]: pass    # do nothing when in on_range
        else:  volumes[npn] = 0                       # set volume to zero when out of range
    return volumes

# [[[[[[[[[[[[[[[[[[[   -- Functions for Meteo Transformation --    ]]]]]]]]]]]]]]]]]]]


#   takes the rolling mean and interpolates the meteo data for each colunm
def met_transform(dM,factors,means,start):
    col_nr = dM.shape[1]-2
    start = int(start*6)
    cut_border = np.trunc((np.amax(means))/2).astype(int)   # calculate nr of nan at the border because of the rolling mean
    cut_begin = np.amax([cut_border,start])
    trans = np.zeros((col_nr, (dM.shape[0]  -cut_border -cut_begin))) 
    if col_nr != len(factors) or col_nr != len(means): print('dM,factor,mean not same length')
    
    for nr,factor, mean in zip(range(col_nr),factors,means):                                          
        Yw  = np.array(dM[dM.columns[nr +2]].rolling(window=mean,center=True).mean()) # nr+2 the first two colums are location and date.
        Yw = Yw * factor
        trans[nr] = Yw[cut_begin: -cut_border]  # remove nan at begining and end. because of rolling mean   
    return trans

    # Prints the end and starting point of the actual tune; Calculates melody_len and Start
def print_dur(bar,bpb,mpb,s_day,s_hour,tune_name):
    start = (s_day*24)+ s_hour  # start in hours 
    melody_len = bar * bpb
    
    S_h = start%24
    S_d = start//24
    dur_h = melody_len *mpb/60
    E_h = (start+dur_h)%24
    E_d = (start+dur_h)//24
    print(tune_name+': Start:',S_d,'day',S_h,'h   End:', E_d,'day',E_h,'h')
    return melody_len, start
    

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
