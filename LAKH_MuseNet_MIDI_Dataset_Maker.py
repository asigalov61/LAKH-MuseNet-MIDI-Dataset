#!/usr/bin/env python
# coding: utf-8

# # LAKH MuseNet MIDI Dataset Maker (ver 1.0)
# 
# ***
# 
# ## Powered by tegridy-tools: https://github.com/asigalov61/tegridy-tools
# 
# ***
# 
# ### Project Los Angeles
# 
# ### Tegridy Code 2022
# 
# ***

# # (Setup Environment)

# In[ ]:


#@title Install all dependencies (run only once per session)

get_ipython().system('git clone https://github.com/Tegridy-Code/tegridy-tools')
get_ipython().system('pip install tqdm')


# In[ ]:


print('Loading needed modules. Please wait...')

import os
from datetime import datetime
import secrets
import copy
import tqdm
from tqdm import tqdm
import re

# Create IO dirs...

print('Creating IO dirs...')

if not os.path.exists('Output'):
    os.mkdir('Output')

if not os.path.exists('In'):
    os.mkdir('In')
if not os.path.exists('Out'):
    os.mkdir('Out')
    
print('Done!')

os.chdir('./tegridy-tools/tegridy-tools')

print('Loading TMIDIX module...')
import TMIDIX

os.chdir('./')


# ***
# 
# # (Donwload and untar LAKH MIDI Dataset)

# In[ ]:


# LAKH MIDI Dataset (https://colinraffel.com/projects/lmd/)

get_ipython().system('wget http://hog.ee.columbia.edu/craffel/lmd/lmd_full.tar.gz')


# In[ ]:


# Untar LAKH dataset...

get_ipython().system('tar -xvf lmd_full.tar.gz')


# ***
# 
# # (Convert MIDIs)
# 
# ***

# In[ ]:


#@title Process MIDIs

sorted_or_random_file_loading_order = True


print('TMIDIX MIDI Processor')
print('Starting up...')
###########

files_count = 0

gfiles = []

melody_chords_f = []

###########

print('Loading MIDI files...')
print('This may take a while on a large dataset in particular.')

dataset_addr = "./lmd_full/"
# os.chdir(dataset_addr)
filez = list()
for (dirpath, dirnames, filenames) in os.walk(dataset_addr):
    filez += [os.path.join(dirpath, file) for file in filenames]
print('=' * 70)

if filez == []:
  print('Could not find any MIDI files. Please check Dataset dir...')
  print('=' * 70)

if sorted_or_random_file_loading_order:
  print('Sorting files...')
  filez.sort()
  print('Done!')
  print('=' * 70)
    
stats = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

v = 1
print('Processing MIDI files. Please wait...')
for f in tqdm(filez):
  try:
    fn = os.path.basename(f)
    fn1 = fn.split('.')[0]

    files_count += 1
    
    
    
    if not os.path.exists('./Output/'+fn):
    
    

        #print('Loading MIDI file...')
        score = TMIDIX.midi2score(open(f, 'rb').read())

        events_matrix = []

        itrack = 1

        patches = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        patch_map = [[0, 1, 2, 3, 4, 5, 6, 7], # Piano 
                     [24, 25, 26, 27, 28, 29, 30], # Guitar
                     [32, 33, 34, 35, 36, 37, 38, 39], # Bass
                     [40, 41], # Violin
                     [42, 43], # Cello
                     [46], # Harp
                     [56, 57, 58, 59, 60], # Trumpet
                     [71, 72], # Clarinet
                     [73, 74, 75], # Flute
                     [-1], # Fake Drums
                     [52, 53] # Choir
                    ]

        while itrack < len(score):
            for event in score[itrack]:         
                if event[0] == 'note' or event[0] == 'patch_change':
                    events_matrix.append(event)
            itrack += 1

        events_matrix1 = []
        for event in events_matrix:
                if event[0] == 'patch_change':
                    patches[event[2]] = event[3]

                if event[0] == 'note':
                    event.extend([patches[event[3]]])
                    once = False
                    for p in patch_map:
                        if event[6] in p and event[3] != 9: # Except the drums
                            event[3] = patch_map.index(p)
                            once = True
                    if not once and event[3] != 9: # Except the drums
                        event[3] = 11 # All other instruments/patches channel
                    if event[3] < 11: # We won't write all other instruments for now...
                        events_matrix1.append(event)
                        stats[event[3]] += 1

        events_matrix1.sort()

        detailed_stats = TMIDIX.Tegridy_SONG_to_MIDI_Converter(events_matrix1, 
                                                               number_of_ticks_per_quarter=score[0], 
                                                               output_file_name='./Output/'+fn1,
                                                              output_signature='Project Los Angeles',
                                                              track_name='Tegridy Code 2022',
                                                              list_of_MIDI_patches=[0, 24, 32, 40, 42, 46, 56, 71, 73, 0, 52, 0, 0, 0, 0, 0]
                                                              )    

        gfiles.append(f)

  except KeyboardInterrupt:
    print('Saving current progress and quitting...')
    break  
  
  except:
    print('Bad MIDI:', f)
    continue


# ***
# 
# # (Bonus) 
# 
# ## Intro and Middle Sampler
# 
# ## This is useful for the creation of the classification datasets
# 
# ***

# In[ ]:


#@title Process MIDIs

sorted_or_random_file_loading_order = True


print('TMIDIX MIDI Processor')
print('Starting up...')
###########

files_count = 0

gfiles = []

melody_chords_f = []

###########

print('Loading MIDI files...')
print('This may take a while on a large dataset in particular.')

dataset_addr = "./lmd_full/"
# os.chdir(dataset_addr)
filez = list()
for (dirpath, dirnames, filenames) in os.walk(dataset_addr):
    filez += [os.path.join(dirpath, file) for file in filenames]
print('=' * 70)

if filez == []:
  print('Could not find any MIDI files. Please check Dataset dir...')
  print('=' * 70)

if sorted_or_random_file_loading_order:
  print('Sorting files...')
  filez.sort()
  print('Done!')
  print('=' * 70)

v = 1
print('Processing MIDI files. Please wait...')
for f in tqdm(filez):
  try:
    fn = os.path.basename(f)
    fn1 = fn.split('.')[0]

    files_count += 1
      
    #print('Loading MIDI file...')
    score1 = TMIDIX.midi2ms_score(open(f, 'rb').read())
    score = score1[2]
    score.sort()
    song1 = score[:300]
    
    song2 = []
    time = 0
    pe = song1[0]
    for s in song1:
        if s[0] == 'note' and s[3] < 11:
            ss = copy.deepcopy(s)
            ss[1] = time
            song2.append(ss)
            time += abs(s[1]-pe[1])
            pe = s
    
    detailed_stats = TMIDIX.Tegridy_SONG_to_MIDI_Converter(song2, 
                                                           number_of_ticks_per_quarter=500, 
                                                           output_file_name='./In/'+' '.join(re.findall(r'[a-zA-Z]+',  fn1)).lower(),
                                                          output_signature='Project Los Angeles',
                                                          track_name='Tegridy Code 2022',
                                                          list_of_MIDI_patches=[0, 24, 32, 40, 42, 46, 56, 71, 73, 0, 52, 0, 0, 0, 0, 0]
                                                          )    
    
    song1 = score[int(len(score[2]) / 2):int(len(score[2]) / 2)+300]
    
    song3 = []
    time = 0
    pe = song1[0]
    for s in song1:
        if s[0] == 'note' and s[3] < 11:
            ss = copy.deepcopy(s)
            ss[1] = time
            song3.append(ss)
            time += abs(s[1]-pe[1])
            pe = s
     
    
    
    detailed_stats = TMIDIX.Tegridy_SONG_to_MIDI_Converter(song3, 
                                                           number_of_ticks_per_quarter=500, 
                                                           output_file_name='./Out/'+' '.join(re.findall(r'[a-zA-Z]+',  fn1)).lower(),
                                                          output_signature='Project Los Angeles',
                                                          track_name='Tegridy Code 2022',
                                                          list_of_MIDI_patches=[0, 24, 32, 40, 42, 46, 56, 71, 73, 0, 52, 0, 0, 0, 0, 0]
                                                          )    
    
    melody_chords_f.append([' '.join(re.findall(r'[a-zA-Z]+',  fn1)).lower(), song2, song3])
    
    gfiles.append(f)
    
    
    
    
  except KeyboardInterrupt:
    print('Saving current progress and quitting...')
    break  
  
  except:
    print('Bad MIDI:', f)
    continue


# ***
# 
# # Congrats! You did it! :)
# 
# ***
