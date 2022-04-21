from evdev import InputDevice, UInput, ecodes
from time import sleep

dev = InputDevice('/dev/input/event24')

spec=dev.capabilities()
spec={ key:value for (key,value) in spec.items() if key in (ecodes.EV_ABS, ecodes.EV_KEY) }

ui=UInput(spec, name='Macro Controller')

def press(typ,btn,val):
	ui.write(typ,btn,val)
	ui.syn()
	sleep(0.07)

for event in dev.read_loop():
	if event.type==ecodes.EV_KEY and event.code==ecodes.BTN_X and event.value==1:
		press(ecodes.EV_ABS,ecodes.ABS_HAT0X,-1)
		press(ecodes.EV_ABS,ecodes.ABS_HAT0Y,1)
		press(ecodes.EV_ABS,ecodes.ABS_HAT0X,0)
		press(ecodes.EV_ABS,ecodes.ABS_HAT0X,1)
		press(ecodes.EV_ABS,ecodes.ABS_HAT0Y,0)
		press(ecodes.EV_ABS,ecodes.ABS_HAT0X,1)
		press(event.type,event.code,event.value)
		press(ecodes.EV_ABS,ecodes.ABS_HAT0X,0)
		press(event.type,event.code,0)

	else:
		ui.write(event.type,event.code,event.value)
