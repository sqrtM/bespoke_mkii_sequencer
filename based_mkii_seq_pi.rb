set :bpm, 144
 

mem0 = []
padmem = []

set :active_mem, []
set :index, 0

set :pad0, false
set :pad1, false
set :pad2, false
set :pad3, false
set :pad4, false
set :pad5, false
set :pad6, false
set :pad7, false
/ set :pad8, false
set :pad9, false
set :pad10, false
set :pad11, false
set :pad12, false
set :pad13, false
set :pad14, false
set :pad15, false /



use_osc_logging false
use_cue_logging false

/midi clock/
live_loop :clock do
  use_real_time
  midi_clock_beat
  sleep 1.0
end


/iterates through the array recieved
via OSC and picks out all the indexes
of "2" then adds them to raw memory/
live_loop :ingroup do
  padmem = sync "/osc*/go"
  padmem[0].to_enum(:scan, /(2)/i).map do |m,|
    if (!mem0.include?($`.size))
      mem0.push($`.size)
    end
  end
end

/iterates through the array and discards
any indexes from the raw memory when they 
become anything other than "2"/
live_loop :outgroup0 do
  padmem = sync "/osc*/go"
  padmem[0].to_enum(:scan, /(0)/i).map do |m,|
  if (mem0.include?($`.size))
    mem0.delete($`.size)
    end
  end
end

live_loop :outgroup1 do
  padmem = sync "/osc*/go"
  padmem[0].to_enum(:scan, /(1)/i).map do |m,|
  if (mem0.include?($`.size))
    mem0.delete($`.size)
    end
  end
end


/takes the raw memory and makes it neater
and easier to work with. memory addresses
are assigned a memory bank as well as a 
number from 0 - c_length representing the pad/
live_loop :transformer do
  padmem = sync "/osc*/go"
  use_real_time
  mem1 = mem0.collect{ |e| (e / 3) - 1 }
  mem1.delete_if { |a| a < 0 }
  set :active_mem, mem1
  set :index, padmem[0][0].to_i
  cue :toggles
end

/each loop here checks/
live_loop :padtog0 do
  sync "toggles"
  active_mem = get :active_mem
  if active_mem.include?(0)
    set :pad0, true
    sleep 0.25
  else
    set :pad0, false
    sleep 0.25
  end
end

live_loop :padtog1 do
  sync "toggles"
  active_mem = get :active_mem
  if active_mem.include?(1)
    set :pad1, true
    sleep 0.25
  else
    set :pad1, false
    sleep 0.25
  end
end

live_loop :padtog2 do
  sync "toggles"
  active_mem = get :active_mem
  if active_mem.include?(2)
    set :pad2, true
    sleep 0.25
  else
    set :pad2, false
    sleep 0.25
  end
end

 live_loop :padtog3 do
  sync "toggles"
  active_mem = get :active_mem
  if active_mem.include?(3)
    set :pad3, true
    sleep 0.25
  else
    set :pad3, false
    sleep 0.25
  end
end

live_loop :padtog4 do
  sync "toggles"
  active_mem = get :active_mem
  if active_mem.include?(4)
    set :pad4, true
    sleep 0.25
  else
    set :pad4, false
    sleep 0.25
  end
end

live_loop :padtog5 do
  sync "toggles"
  active_mem = get :active_mem
  if active_mem.include?(5)
    set :pad5, true
    sleep 0.25
  else
    set :pad5, false
    sleep 0.25
  end
end

live_loop :padtog6 do
  sync "toggles"
  active_mem = get :active_mem
  if active_mem.include?(6)
    set :pad6, true
    sleep 0.25
  else
    set :pad6, false
    sleep 0.25
  end
end

live_loop :padtog7 do
  sync "toggles"
  active_mem = get :active_mem
  if active_mem.include?(7)
    set :pad7, true
    sleep 0.25
  else
    set :pad7, false
    sleep 0.25
  end
end
/
live_loop :padtog8 do
  sync "toggles"
  active_mem = get :active_mem
  if active_mem.include?(8)
    set :pad8, true
    sleep 0.25
  else
    set :pad8, false
    sleep 0.25
  end
end

live_loop :padtog9 do
  sync "toggles"
  active_mem = get :active_mem
  if active_mem.include?(9)
    set :pad9, true
    sleep 0.25
  else
    set :pad9, false
    sleep 0.25
  end
end

live_loop :padtog10 do
  sync "toggles"
  active_mem = get :active_mem
  if active_mem.include?(10)
    set :pad10, true
    sleep 0.25
  else
    set :pad10, false
    sleep 0.25
  end
end

live_loop :padtog11 do
  sync "toggles"
  active_mem = get :active_mem
  if active_mem.include?(11)
    set :pad11, true
    sleep 0.25
  else
    set :pad11, false
    sleep 0.25
  end
end

live_loop :padtog12 do
  sync "toggles"
  active_mem = get :active_mem
  if active_mem.include?(12)
    set :pad12, true
    sleep 0.25
  else
    set :pad12, false
    sleep 0.25
  end
end

live_loop :padtog13 do
  sync "toggles"
  active_mem = get :active_mem
  if active_mem.include?(13)
    set :pad13, true
    sleep 0.25
  else
    set :pad13, false
    sleep 0.25
  end
end

live_loop :padtog14 do
  sync "toggles"
  active_mem = get :active_mem
  if active_mem.include?(14)
    set :pad14, true
    sleep 0.25
  else
    set :pad14, false
    sleep 0.25
  end
end

live_loop :padtog15 do
  sync "toggles"
  active_mem = get :active_mem
  if active_mem.include?(15)
    set :pad15, true
    sleep 0.25
  else
    set :pad15, false
    sleep 0.25
  end
end
/