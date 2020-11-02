from neurons_engine import neurons_request, neurons_blocking_read, neurons_async_read, neurons_is_block_online
import time, math
from common import num_range_scale, node_table, MIDI_NOTE_NUM0, NOTE_FREQUENCE_RATIO

PLAY_MAX_TIME = 86400

# music_name_table = {"hello": "!001", "hi": "!002", "bye": "!003", "yeah": "!004", "wow": "!005", "laugh": "!006", "hum": "!007", "sad": "!008", "sigh": "!009", "annoyed": "!010"}
def stop_sounds(index = 1):
    if not isinstance(index, (int, float)):
        return

    neurons_request("m_speaker", "stop", (), index)
    time.sleep(0.1)

def set_volume(val, index = 1):
    if not isinstance(index, (int, float)):
        return

    if not isinstance(val, (int, float)):
        return
    val = num_range_scale(val, 0, 100)

    neurons_request("m_speaker", "set_volume", val, index)
    time.sleep(0.05)

def change_volume(val, index = 1):
    if not isinstance(index, (int, float)):
        return

    if not isinstance(val, (int, float)):
        return
    val = num_range_scale(val, -100, 100)
    neurons_request("m_speaker", "change_volume", val, index)
    time.sleep(0.05)

def get_volume(index = 1):
    if not isinstance(index, (int, float)):
        return 0

    value = neurons_blocking_read("m_speaker", "get_volume", (), index)
    if value == None:
        return 0
    else:
        return value[0]

def play_note(note, beat = None, index = 1):
    if not isinstance(index, (int, float)):
        return

    if isinstance(note, (int, float)):
        note = num_range_scale(note, 48, 72) 

        freq = MIDI_NOTE_NUM0 * math.pow(NOTE_FREQUENCE_RATIO, note)

    elif isinstance(note, str):
        if note in node_table:
            freq = node_table[note]
        else:
            return
    
    neurons_request("m_speaker", "stop", (), index)

    if beat == None:
        neurons_request("m_speaker", "play_frequency", freq, index)

    elif isinstance(beat, (int, float)):
        beat = num_range_scale(beat, 0)
        if beat <= 0:
            return

        neurons_request("m_speaker", "play_frequency", freq, index)
        time.sleep(beat)
        neurons_request("m_speaker", "stop", (), index)

def play_tone(freq, t = None, index = 1):
    if not isinstance(index, (int, float)):
        return

    if not isinstance(freq, (int, float)):
        return

    freq = num_range_scale(freq, 0, 5001)

    if freq > 5000 or freq < 20:
        freq = 0        

    if t == None:
        neurons_request("m_speaker", "play_frequency", freq, index)

    elif isinstance(t, (int, float)):
        t = num_range_scale(t, 0, PLAY_MAX_TIME)
        if t <= 0:
            return

        neurons_request("m_speaker", "play_frequency", freq, index)
        time.sleep(t)
        neurons_request("m_speaker", "stop", (), index)
    
def play_melody(music, index = 1):
    if not isinstance(index, (int, float)):
        return
    if not isinstance(music, str):
        return
		
	# only process music name which the length is 4, such as "!101"
    if len(music) != 4:
        return
		
	# this delay is for the bug of mbuild speaker module
	# without it, mutilple continuous calling of this function will
	# cause a unusual behavior
    time.sleep(0.1)
	
    neurons_request("m_speaker", "play_melody", music, index)

def play_melody_until_done(music, index = 1):
    if not isinstance(index, (int, float)):
        return
    if not isinstance(music, str):
        return
		
	# only process music name which the length is 4, such as "!101"
    if len(music) != 4:
        return
        
    neurons_request("m_speaker", "play_melody", music, index)

    if not neurons_is_block_online("m_speaker", index):
        return
    time.sleep(0.1)
    while neurons_blocking_read("m_speaker", "get_status", (), index) != [0]:
        if not neurons_is_block_online("m_speaker", index):
            return        
        time.sleep(0.1)

def is_playing(index = 1):
    if not isinstance(index, (int, float)):
        return False

    value = neurons_blocking_read("m_speaker", "get_status", (), index)
    if value == None:
        return False
    else:
        return bool(value[0])