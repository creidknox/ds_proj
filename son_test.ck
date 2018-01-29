2000 => int padding;
2 => int instrument_buffers;
me.sourceDir() => string base_dir;

// normalize base directory
if (base_dir.charAt(base_dir.length()-1) != '/')
{
    "/" +=> base_dir;
}

// instrument object
class Instrument {
    string filename;
    SndBuf buf[8];  // http://chuck.cs.princeton.edu/doc/program/ugen_full.html
    int plays;
}

// data files
base_dir + "data/chk_instruments.csv" => string instruments_file;
base_dir + "data/chk_sequence.csv" => string sequence_file;

// read data files
FileIO instruments_fio;
FileIO sequence_fio;
instruments_fio.open( instruments_file, FileIO.READ );
sequence_fio.open( sequence_file, FileIO.READ );

// check if files are valid
if( !instruments_fio.good() || !sequence_fio.good() )
{
    cherr <= "can't open instrument and/or sequence files for reading..."
          <= IO.newline();
    me.exit();
}

// create instruments array
Instrument instruments[128];

// read instruments file
while( instruments_fio.more() )
{
    //<<< "Instruments" >>>;
    // read instrument index and filename
    Std.atoi(instruments_fio.readLine()) => int instrument_index;
    instruments_fio.readLine() => string filename;
    filename.find("\r") => int return_match;
    if (return_match >= 0)
    {
        filename.erase(return_match, 1);
    }
    base_dir + filename => instruments[instrument_index].filename;
    0 => instruments[instrument_index].plays;
    // create buffers from filename
    for( 0 => int i; i < instrument_buffers; i++ )
    {
        instruments[instrument_index].filename => instruments[instrument_index].buf[i].read; // load the file for reading
        // set position to end, so it won't play immediately upon open
        instruments[instrument_index].buf[i].samples() => instruments[instrument_index].buf[i].pos; // get number of samples and set position to the total
        instruments[instrument_index].buf[i] => dac;  // da converter
    }

}

// Add padding
padding::ms => now;

// read sequence from file
while( sequence_fio.more() ) {
    //<<< "Sequence" >>>;
    // Read the lines from the sequence file and assign to thes vars
    Std.atoi(sequence_fio.readLine()) => int instrument_index; // 9, 3
    Std.atoi(sequence_fio.readLine()) => int position; // 0, 0
    Std.atof(sequence_fio.readLine()) => float gain; // 0.05, 0.1
    Std.atof(sequence_fio.readLine()) => float rate; // seems like this is always 1.0
    Std.atoi(sequence_fio.readLine()) => int milliseconds; // 0, 3
    <<< gain >>>;
    // wait duration
    if (milliseconds > 0)
    {
        /*
            This seems to be where it actually plays
            Advancing time by the number of ms specified
                Time can only be advanced by specifically manipulating `now`
                `now` is the current logical time
                Advancing time allows other shreds (processes) to run and allows audio to be computed in a controlled manner
                A time chucked to now will have ChucK wait until the appointed time
        */
        milliseconds::ms => now;
    }

    // choose buffer index
    instruments[instrument_index].plays % instrument_buffers => int buffer_index;  // 0 % 2 = 0 (first iteration)
    instruments[instrument_index].plays++;  // increment plays for instrument

    // play the instrument
    position => instruments[instrument_index].buf[buffer_index].pos;  // set the position to the value of position
    gain => instruments[instrument_index].buf[buffer_index].gain;  // set the gain of this iteration of the instrument
    rate => instruments[instrument_index].buf[buffer_index].rate;  // set/get playback rate ( relative to file's natural speed ) - this appears to always be one in this example
}

// Add padding
padding::ms => now;

<<< "Done." >>>;
