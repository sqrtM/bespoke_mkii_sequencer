import midicontroller
import drumsequencer
import module
import grid
import oscoutput

o = oscoutput.get("oscoutput")
m = midicontroller.get("midicontroller")

me.connect_osc_input(6969)

                # arturia minilab mkii pad addresses
hexoffset = 112 # begin at 0x70, or 112 in dec, so we need to add that
                # amount to any address we produce in script

noteoffset = 36  
# bespoke reads the lowest pad on the mkii as note 36 by default
# if you have changed your settings for your minilab mkii, this 
# may not be the case, and if you are having problems getting the
# sequencer to run as intended, this is the most likely problem.

n_length = int(me.get("pulser~interval") + 1)
# n_length (note length) is how fast the sequencer tics.
# - set automatically by the pulser interval.

# haven't been able to get 64nt and above 
# or 2n and below to work with this set up yet
# (i'm sure it's possible, as my design here is very... hokey.)
# all other note lengths should work fine, though!

if n_length == 8:
    n_length += 8
if n_length == 7:
    n_length += 5
if n_length == 6:
    n_length += 2
if n_length == 5:
    n_length += 1
   
# this number, c_length (cycle length), is how many pads
# you would like the sequencer to use, between 2 and 16

c_length = 8

# any pads not used will automatically
# become membank switchers

membanks = 16 - c_length
# this variable will be used by the script to figure out
# how many pads are not being used, and turn them into
# bank switchers

padmem = [[int(0)] * c_length for _ in range(membanks)]
# this is our 2D "memory" array which keeps track of the status of each pad.
# the list will auto populate with zeroes equal to the number of pads
# we entered into c_length. the numbers will be initiallized as 0, signifying "off",
# but become 1 when an "off" pad is on the current subdivision, and 2 when a pad
# is toggled as an active sequencer.

active_mem = 0
# active_mem is the 1D memory line you are currently looking at
# this is switched with the bank switchers, if c_length is less than 15.



# these values designate the colors for
# when the pad is "on", "off", "seqon", 
# "seqoff", and the bank switches.

colorNone   = 0x00
colorRed    = 0x01
colorGreen  = 0x04
colorYellow = 0x05
colorBlue   = 0x10
colorPurple = 0x11
colorCyan   = 0x14
colorWhite  = 0x7F

oncolor   = colorPurple
offcolor  = colorCyan
seqon     = colorWhite
seqoff    = colorGreen
bankcolor = colorBlue
# for best results : in the Arturia MIDI Control Center:
# 1. set all your pads to TOGGLE, not GATE
# 2. set PAD OFF BACKLIGHT to OFF, and
# 3. set each pad color to be the same as the "seqoff" color.

sysmsg = [0x00, 0x20, 0x6B, 0x7F, 0x42, 0x02, 0x00, 0x10, 0x00, 0x00]
# this list is the system exclusive message which will
# be sent to the keyboard. the first 8 instructions are more or
# less generic and not important for what we will be doing. the
# last two are pad address and color respectively.

def refresh():
    for x in range(16 - c_length):
        if x <= membanks:
            sysmsg[-2] = 16 - membanks + hexoffset + x
            sysmsg[-1] = 0x00  
            m.send_sysex(bytes(sysmsg))
        else:
            break        
    sysmsg[-2] = hexoffset + c_length
    sysmsg[-1] = bankcolor
    m.send_sysex(bytes(sysmsg))

refresh()
# this initializes the lights for the bank switches
# so they actually reflect the correct initial bank

############################################

def on_note(note, velocity): 
    global active_mem
    o.send_string("/go", str(active_mem) + ", " + str(padmem[active_mem]))
    if note >= c_length + noteoffset:
        for x in range(16 - c_length):
            if x <= membanks:
                sysmsg[-2] = 16 - membanks + hexoffset + x
                sysmsg[-1] = colorNone  
                m.send_sysex(bytes(sysmsg))
            else:
               break
        active_mem = note - noteoffset - c_length
        sysmsg[-2] = hexoffset + note - noteoffset
        sysmsg[-1] = bankcolor  
        m.send_sysex(bytes(sysmsg))
        me.output(sysmsg)
        return active_mem
    elif noteoffset <= note < c_length + noteoffset:
        if padmem[active_mem][note - noteoffset] == 2:   
               padmem[active_mem][note - noteoffset] = 0
               sysmsg[-2] = 0x70 + note - noteoffset
               sysmsg[-1] = offcolor  
               m.send_sysex(bytes(sysmsg))
               return padmem[active_mem]
        else:
            sysmsg[-2] = 0x70 + note - noteoffset
            sysmsg[-1] = seqoff 
            padmem[active_mem][note - noteoffset]  = 2
            m.send_sysex(bytes(sysmsg))
            return padmem[active_mem]
    else:
        return

def on_pulse():
    global active_mem
    o.send_string("/go", str(active_mem) + ", " + str(padmem[active_mem]))
    m = midicontroller.get("midicontroller")
    g = grid.get("grid")
    g.set_grid(c_length, membanks)
    for x in range(membanks):
       g.set_label(x, str(x))

    hit = bespoke.get_step(n_length) % c_length
    lastpos = hit - 1
    if lastpos < 0:
        lastpos = c_length - 1  
      
    seqpos = hexoffset + hit
    hexseqpos = int(hex(seqpos), 16)
    oldhexpos = hexseqpos - 1
    if oldhexpos == 111:                      #when it reaches the last pad...
        oldhexpos = hexoffset + c_length - 1  #clear it and restart at pad0

    for pad in range(c_length):
        if padmem[active_mem][pad] == 0:
            paddec = pad + hexoffset
            padhex = int(hex(paddec), 16)
            sysmsg[-2] = padhex
            sysmsg[-1] = offcolor
            m.send_sysex(bytes(sysmsg))   
        if padmem[active_mem][pad] == 1 & padmem[active_mem][hit] != 1:
            paddec = pad + hexoffset
            padhex = int(hex(paddec), 16)
            padmem[active_mem][pad] == 0
            sysmsg[-2] = padhex
            sysmsg[-1] = offcolor
            m.send_sysex(bytes(sysmsg))   
        if padmem[active_mem][pad] == 2:
            paddec = pad + hexoffset
            padhex = int(hex(paddec), 16)
            sysmsg[-2] = padhex
            sysmsg[-1] = seqoff
            m.send_sysex(bytes(sysmsg))   
    
    
    # reads the status of the pads and
    # sends the color to the controller
    for pos in range(len(padmem)):
        if padmem[active_mem][hit] == 2:
            sysmsg[-2] = hexseqpos
            sysmsg[-1] = seqon
            m.send_sysex(bytes(sysmsg))
           
        else:
            padmem[active_mem][hit] = 1 
            sysmsg[-2] = hexseqpos   
            sysmsg[-1] = oncolor
            m.send_sysex(bytes(sysmsg))
     
        if padmem[active_mem][lastpos] == 2:
            sysmsg[-2] = hexseqpos           # genuinely no idea why this works
            sysmsg[-1] = oncolor             # i mean, shouldn't these first two
            sysmsg[-2] = oldhexpos           # sysmsg things do nothing ? but the
            sysmsg[-1] = seqoff              # script doesn't work w/o them....
            m.send_sysex(bytes(sysmsg))
        else:
            padmem[active_mem][lastpos] = 0
            sysmsg[-2] = oldhexpos
            sysmsg[-1] = offcolor
            m.send_sysex(bytes(sysmsg))
    
    
    
    # sends the status of the pads to the grid module
    # so other modules can read the memorybanks natively   

    g.highlight_cell(hit, active_mem, -0.1, 0.15, 1)
    
    for j in range(membanks):
       if 2 in padmem[j]:
          col = [i for i, x in enumerate(padmem[j]) if x == 2]
          for k in range(len(col)):
              g.set(col[k], j, 1)
    
    for m in range(membanks):
        off = [i for i, x in enumerate(padmem[m]) if x != 2]
        for n in range(len(off)):
            g.set(off[n], m, 0) 
    return padmem
    
