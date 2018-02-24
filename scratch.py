"""
Writing to the sequence file that will create the musical sequence (the song)
@param  gain        The gain (volume) of the instrument - this will be equivilent to the value of the variable that week
@param  instrument  The current instrument being added
@param  ms          The current location in the sequence (song)
@param  duration    The number of ms that makes up a data point (week) in the sequence (song)
"""
def addBeatsToSequence(gain, instrument, ms, duration):
    global sequence
    global hindex
    # Will this instrument be offset?
    # Tempo Offset of 0 will play the instrument on the fitst beat
    # Tempo Offset of 0.5 will play the instrument on the offbeat
    # Tempo Offset of 1 will play the instrument on the second beat
    # Get the amount of ms the instrument will be offset so that it can be added to the place in the song
    offset_ms = int(instrument['Tempo Offset'] * BEAT_MS)
    ms += offset_ms
    h = halton(hindex, 3)
    variance = int(h * VARIANCE_MS * 2 - VARIANCE_MS)
    rate_variance = float(h * VARIANCE_RATE * 2 - VARIANCE_RATE) # This is currently always 0
    print(rate_variance)
    sequence.append({
        'instrument_index': instrument['index'],
        'instrument': instrument,
        'position': 0,
        'gain': round(gain, 2),
        'rate': 1.0 + rate_variance,
        'elapsed_ms': max([ms + variance, 0])
    })
    hindex += 1
    # increment where we are in the song
    ms += duration

# Add beats to sequence
# gain = the gain (volume) of the instrument - this will be equivilent to the value of the variable that week
# instrument = the current instrument we are adding
# ms = where we are in the song (in ms)
def addBeatsToSequence(gain, instrument, ms, duration):
    global sequence
    global hindex
    # Will this instrument be offset?
    # Tempo Offset of 0 will play the instrument on the fitst beat
    # Tempo Offset of 0.5 will play the instrument on the offbeat
    # Tempo Offset of 1 will play the instrument on the second beat
    # Get the amount of ms the instrument will be offset so that it can be added to the place in the song
    offset_ms = int(instrument['Tempo Offset'] * BEAT_MS)
    ms += offset_ms
    #previous_ms = int(ms)
    # BPMS of the instrument's initial tempo
    #from_beat_ms = instrument['From Beat MS']
    # BPMS of the instrument's target tempo
    #to_beat_ms = instrument['To Beat MS']
    # BPMS of the instrument's slowest tempo
    #min_ms = min(from_beat_ms, to_beat_ms)
    # if there is an offset
    #elapsed_duration = offset_ms
    # where are we in the song at this moment
    elapsed_ms = int(ms)
    # what beat in the sequence are we on - difference between where we are in the song and where we started the sequnce / bpms
    #elapsed_beat = int((elapsed_ms-previous_ms) / BEAT_MS)
    # beat duration in ms based on this current point in time
    #this_beat_ms = getBeatMs(instrument, elapsed_beat, MS_PER_DIVIDED_BEAT)
    #print(this_beat_ms)
    h = halton(hindex, 3)
    variance = int(h * VARIANCE_MS * 2 - VARIANCE_MS)
    rate_variance = float(h * VARIANCE_RATE * 2 - VARIANCE_RATE)
    sequence.append({
        'instrument_index': instrument['index'],
        'instrument': instrument,
        'position': 0,
        'gain': round(gain, 2),
        'rate': 1.0 + rate_variance,
        'elapsed_ms': max([elapsed_ms + variance, 0])
    })
    hindex += 1
    # increment the possible offset
    #elapsed_duration += this_beat_ms
    # increment where we are in the song
    ms += week_duration


#Round n to the nearest nearest
def roundToNearest(n, nearest):
    return 1.0 * round(1.0*n/nearest) * nearest

# Multiplier based on sine curve
def getMultiplier(percent_complete):
    radians = percent_complete * math.pi
    multiplier = math.sin(radians)
    if multiplier < 0:
        multiplier = 0.0
    elif multiplier > 1:
        multplier = 1.0
    return multiplier

# Get beat duration in ms based on current point in time
def getBeatMs(instrument, beat, round_to):
    from_beat_ms = instrument['From Beat MS']
    to_beat_ms = instrument['To Beat MS']
    beats_per_phase = instrument['Tempo Phase']
    percent_complete = float(beat % beats_per_phase) / beats_per_phase
    multiplier = getMultiplier(percent_complete)
    ms = multiplier * (to_beat_ms - from_beat_ms) + from_beat_ms
    ms = int(roundToNearest(ms, round_to))
    return ms

# Make sure there's no sudden drop in gain
# Variable Min and max represent the percentage of the variables
# Example: Variable Min = 60 and Variable Max = 100, this instrument can only be played when the variable is between 0.6 and 1.0
"""
def continueFromPrevious(instrument):
    return instrument['Variable Min'] > 0 or instrument['Variable Max'] < 100
"""

# Return if the instrument should be played in the given interval
def isValidInterval(instrument, elapsed_ms):
    return True
    #interval_ms = instrument['Interval MS']
    #interval = instrument['Interval']
    #interval_offset = instrument['Interval Offset']    
    #return int(math.floor(1.0*elapsed_ms/interval_ms)) % interval == interval_offset

# Retrieve gain based on current beat
""""
def getGain(instrument, beat):
	beats_per_phase = instrument['Gain Phase']
	percent_complete = float(beat % beats_per_phase) / beats_per_phase
	multiplier = getMultiplier(percent_complete)
	from_gain = instrument['From Gain']
	to_gain = instrument['To Gain']
	min_gain = min(from_gain, to_gain)
	gain = multiplier * (to_gain - from_gain) + from_gain
	gain = max(min_gain, round(gain, 2))
	return gain
"""

"""
# Add beats to sequence
# instrument = the current instrument we are adding
# duration = how long (in ms) this instrument will play
# ms = where we are in the song (in ms)
# beat_ms = ms in a beat - 500 (BEAT_MS)
# round_to = beat (measure) over divisions per beat (time signature) - 125 (ROUND_TO_NEAREST)
def addBeatsToSequence(val, instrument, duration, ms, beat_ms, round_to):
	global sequence
	global hindex
    # Will this instrument be offset?
    # Tempo Offset of 0 will play the instrument on the fitst beat
    # Tempo Offset of 0.5 will play the instrument on the offbeat
    # Tempo Offset of 1 will play the instrument on the second beat
	#print(round(val, 2))
	offset_ms = int(instrument['Tempo Offset'] * beat_ms)
	ms += offset_ms
	previous_ms = int(ms)
    # BPMS of the instrument's initial tempo
	from_beat_ms = instrument['From Beat MS']
    # BPMS of the instrument's target tempo
	to_beat_ms = instrument['To Beat MS']
    # BPMS of the instrument's slowest tempo
	min_ms = min(from_beat_ms, to_beat_ms)
    # how long the instrument will play - corresponds to queue_duration
	remaining_duration = int(duration)
    # if there is an offset
	elapsed_duration = offset_ms
    # wat
	#continue_from_prev = continueFromPrevious(instrument)
    # while how long we have to play > BPMS of the instrument's slowest tempo
	while remaining_duration >= min_ms:
        # where are we in the song at this moment
		elapsed_ms = int(ms)
        # what beat in the sequence are we on - difference between where we are in the song and where we started the sequnce / bpms
		elapsed_beat = int((elapsed_ms-previous_ms) / beat_ms)
		# continue beat from previous
		#if continue_from_prev:
			#elapsed_beat = int(elapsed_ms / beat_ms)
        # beat duration in ms based on this current point in time
		this_beat_ms = getBeatMs(instrument, elapsed_beat, round_to)
		# add to sequence if in valid interval
		if isValidInterval(instrument, elapsed_ms):
			#print('oh hai')
			#print(round(val, 2))
			h = halton(hindex, 3)
			variance = int(h * VARIANCE_MS * 2 - VARIANCE_MS)
			rate_variance = float(h * VARIANCE_RATE * 2 - VARIANCE_RATE)
			sequence.append({
				'instrument_index': instrument['index'],
				'instrument': instrument,
				'position': 0,
				'gain': round(val, 2), #getGain(instrument, elapsed_beat),
				'rate': 1.0 + rate_variance,
				'elapsed_ms': max([elapsed_ms + variance, 0])
			})
			hindex += 1
        # decrement the amount of time left for this instrument to play
		remaining_duration -= this_beat_ms
        # increment the possible offset
		elapsed_duration += this_beat_ms
        # increment where we are in the song
		ms += this_beat_ms
        """


# Get number of instruments
#n_instruments = instruments.shape[0]
#sequence = []
#hindex = 0

"""
This is where we build the sequence file
    Make a set duration for how long we will spend on each data point (in this case, each data point represents a week)
    Loop through each instrument in the given instrument csv
    For each instrument, loop through the variable values
        An instrument is played for the variable if the value of the variable is greater than the allowed variable for the instrument
            If an instrument is played, add that beat to the sequence file
        Incrument where we are in the song (ms defines where we are in the song)
"""
# Amount of time, in MS, to spend on each data point
week_duration = 500

# Loop through each instrument
for index, instrument in enumerate(instruments.iterrows()):
    # ms is our current place in the song
    ms = 0
    # queue_duration is how long to play the instrument for current 'period' (accumulation of weeks)
    # queue_duration = 0

    instrument = instrument[1]
    instrument['index'] = index
    min_var = instrument['Min Var']
    #Loop through each week's value
    for week_val in test_var:
        play_instrument = (week_val*100) > min_var
        if play_instrument:
            addBeatsToSequence(week_val, instrument, ms)
        ms += week_duration
    """
    gains = []
    for week_val in test_var:
        #print(week_val)
        # Should this instrument be playing for this week?
        play_instrument = (week_val*100) > min_var
        # play_instrument = (week_val*n_instruments) > index
        if play_instrument:
            # add this week's duration to queue_duration, since instrument should play for this week
            queue_duration += week_duration
            gains.append(week_val)
        elif queue_duration > 0:
            # We've stopped playing the instrument, add the queued beats to sequence and increment where we are in the song
            addBeatsToSequence(gains, instrument, queue_duration, ms, BEAT_MS, ROUND_TO_NEAREST)
            # increment where we are in the song (ms)
            ms += queue_duration + week_duration
            queue_duration = 0
        else:
            # Not playing the instrument and weren't before this week, just skip this week by incrementing where we are in the song
            ms += week_duration
    if queue_duration > 0:
        # If we ended the song playing this instrument, make sure we add the residual queue time to the sequence
        addBeatsToSequence(gains, instrument, queue_duration, ms, BEAT_MS, ROUND_TO_NEAREST)
    """
