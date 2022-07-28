import midicontroller
import module

# module.create("midicontroller", 500, 100)
m = midicontroller.get("midicontroller")

# module.create("pulser", 100, 400)
# me.set("pulser~interval", 3)
# module.get("pulser").set_target(module.get("script"))

                # arturia minilab mkii pad addresses
hexoffset = 112 # begin at 0x70, or 112 in dec, so we need to add that
                # amount to any address we produce in script
                
n_length = int(me.get("pulser~interval") + 1)
# n_length is how fast the sequencer bangs.
# set automatically by the pulser.

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

# of course, anything over 8 requires using
# the pad switcher at the top left of 
# the controller to see


##########


# these values designate the colors for
# when the pad is "on" or "off".

oncolor =  0x01
offcolor = 0x7F

# 0x00 = off,    0x01 = red,  0x04 = green
# 0x05 = yellow, 0x10 = blue, 0x11 = magenta
#        0x14 = cyan, 0x7F = white

      
def clear():
   pad = 0
   for x in range(16):
      padtar = pad + hexoffset
      padhex = hex(padtar)
      m.send_sysex(bytes([0x00, 0x20, 0x6B, 0x7F, 0x42, 0x02, 0x00, 0x10, int(padhex, 16), offcolor]))
      pad = pad + 1

def on_pulse():
   subdiv = bespoke.get_step(n_length) % c_length
   me.output(subdiv)
   
   clear() #clears the pads on each beat to the "off" color.
           #looks a bit cleaner, especially when your pad colors 
           #are set to "toggle" but doesn't effect any functionality
           
   seqpos = hexoffset + subdiv
   hexseqpos = int(hex(seqpos), 16)
   oldhexpos = hexseqpos - 1
   if oldhexpos == 111:                     #when it reaches the last pad...
      oldhexpos = hexoffset + c_length - 1  #clear it and restart at pad0
   me.output(oldhexpos)
   me.output(n_length + hexoffset)
      
   m.send_sysex(bytes([0x00, 0x20, 0x6B, 0x7F, 0x42, 0x02, 0x00, 0x10, hexseqpos, oncolor ]))
   m.send_sysex(bytes([0x00, 0x20, 0x6B, 0x7F, 0x42, 0x02, 0x00, 0x10, oldhexpos, offcolor]))
   
on_pulse()