import midicontroller
import module

m = midicontroller.get("midicontroller")

                # arturia minilab mkii pad addresses
hexoffset = 112 # begin at 0x70, or 112 in dec, so we need to add that
                # amount to any address we produce in script

padoffset = 36  #bespoke reads the lowest pad on the mkii as note 36
                
n_length = int(me.get("pulser~interval") + 1)
# n_length is how fast the sequencer tics.
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
   
# this number, c_length, is how many pads
# you would like the sequence to use, 
# between 2 and 16

c_length = 8

# (of course, anything over 8 requires using
# the pad switcher at the top left of 
# the controller to see)

# this list is the system exclusive message, in bytes, which will
# be sent to the keyboard. the first 8 instructions are more or
# less generic and not important for what we will be doing. the
# last two are pad address and color respectively.
sysmsg = [0x00, 0x20, 0x6B, 0x7F, 0x42, 0x02, 0x00, 0x10, 0x00, 0x00]

# this list is our "memory" to keep track of the status of each pad.
# the list will auto populate with zeroes equal to the number of pads
# you entered for c_length. # 0 = off ; 1 = on ; 2 = seq
padmem = [int(0)] * c_length

# these values designate the colors for
# when the pad is "on", "off", "seqon", and "seqoff".

oncolor  = 0x11
offcolor = 0x14
seqon    = 0x7F
seqoff   = 0x04

# 0x00 = off,    0x01 = red,  0x04 = green
# 0x05 = yellow, 0x10 = blue, 0x11 = magenta
#        0x14 = cyan, 0x7F = white

# for best results : in the Arturia MIDI Control Center:
# 1. set all your pads to TOGGLE, not GATE
# 2. set PAD OFF BACKLIGHT to OFF, and
# 3. set each pad color to be the same as the "seqoff" color.

############################################

def on_note(note, velocity):  
   if padoffset <= note < c_length + padoffset:
      if padmem[note - padoffset] == 2:   
         padmem[note - padoffset] = 0
         sysmsg[-2] = 0x70 + note - padoffset
         sysmsg[-1] = offcolor  
         m.send_sysex(bytes(sysmsg))
         return padmem
      else:
         sysmsg[-2] = 0x70 + note - padoffset
         sysmsg[-1] = seqoff  
         padmem[note - padoffset]  = 2
         m.send_sysex(bytes(sysmsg))
         me.output(padmem)
         return padmem
   else:
      return

def on_pulse():
   pad = 0
   for pad in range(c_length):
      if padmem[pad] == 0:
         paddec = pad + hexoffset
         padhex = int(hex(paddec), 16)
         sysmsg[-2] = padhex
         sysmsg[-1] = offcolor
         me.output(sysmsg)  
         m.send_sysex(bytes(sysmsg))   


   hit = bespoke.get_step(n_length) % c_length     
   lastpos = hit - 1
   if lastpos < 0:
      lastpos = c_length - 1  
           
   seqpos = hexoffset + hit
   hexseqpos = int(hex(seqpos), 16)
   oldhexpos = hexseqpos - 1
   if oldhexpos == 111:                     #when it reaches the last pad...
      oldhexpos = hexoffset + c_length - 1  #clear it and restart at pad0

   if padmem[hit] == 2:
      sysmsg[-2] = hexseqpos
      sysmsg[-1] = seqon
      m.send_sysex(bytes(sysmsg))
      me.output(sysmsg)
      
   else:   
      padmem[hit] = 1 
      sysmsg[-2] = hexseqpos   
      sysmsg[-1] = oncolor
      m.send_sysex(bytes(sysmsg))
      me.output(sysmsg)

   if padmem[lastpos] == 2:
      sysmsg[-2] = hexseqpos   
      sysmsg[-1] = oncolor      
      sysmsg[-2] = oldhexpos  
      sysmsg[-1] = seqoff
      m.send_sysex(bytes(sysmsg))
      me.output(sysmsg)
   else:
      sysmsg[-2] = oldhexpos
      padmem[lastpos] = 0
      sysmsg[-1] = offcolor
      m.send_sysex(bytes(sysmsg))
      me.output(sysmsg)
   
   me.output(lastpos)
   me.output(oldhexpos)
   me.output(hit)
   
   me.output(padmem)
   
   return padmem, hit