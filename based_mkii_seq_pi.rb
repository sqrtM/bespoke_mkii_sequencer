/for debugging and sync purposes/

live_loop :metronome, delay: 0.01 do
  sync :clock
  use_synth :beep
  play :a3
  sleep 2
end

live_loop :foo, sync: :metronome do   
  sync :clock  
  if get(:pad0) == true && get(:index) == 0
    sample :bd_tek 
    sleep 0.05
  else 
    sleep 0.5
  end
end
