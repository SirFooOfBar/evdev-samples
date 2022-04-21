from evdev import ecodes, UInput, AbsInfo
from time import sleep
import rtmidi

spec = {
ecodes.EV_KEY:[
	ecodes.BTN_A, ecodes.BTN_B, ecodes.BTN_X, ecodes.BTN_Y,
	ecodes.BTN_TL, ecodes.BTN_TR, ecodes.BTN_SELECT, ecodes.BTN_START,
	ecodes.BTN_THUMBL, ecodes.BTN_THUMBR],
ecodes.EV_ABS:[
	(ecodes.ABS_X, AbsInfo(value=0, min=-32768, max=32767, fuzz=32, flat=0, resolution=0)),
	(ecodes.ABS_Y, AbsInfo(value=0, min=-32768, max=32767, fuzz=32, flat=0, resolution=0)),
	(ecodes.ABS_Z, AbsInfo(value=0, min=0, max=1023, fuzz=4, flat=0, resolution=0)),
	(ecodes.ABS_RX, AbsInfo(value=0, min=-32768, max=32767, fuzz=32, flat=0, resolution=0)),
	(ecodes.ABS_RY, AbsInfo(value=0, min=-32768, max=32767, fuzz=32, flat=0, resolution=0)),
	(ecodes.ABS_RZ, AbsInfo(value=0, min=0, max=1023, fuzz=4, flat=0, resolution=0)),
	(ecodes.ABS_HAT0X, AbsInfo(value=0, min=-1, max=1, fuzz=0, flat=0, resolution=0)),
	(ecodes.ABS_HAT0Y, AbsInfo(value=0, min=-1, max=1, fuzz=0, flat=0, resolution=0)),
	(ecodes.ABS_MISC, AbsInfo(value=0, min=0, max=1023, fuzz=4, flat=0, resolution=0)),
]}

controls={
	0: (ecodes.EV_KEY, ecodes.BTN_A, 1),
	2: (ecodes.EV_KEY, ecodes.BTN_B, 1),
	4: (ecodes.EV_KEY, ecodes.BTN_X, 1),

	5: (ecodes.EV_ABS, ecodes.ABS_HAT0X, -1),
	7: (ecodes.EV_ABS, ecodes.ABS_HAT0Y, 1),
	9: (ecodes.EV_ABS, ecodes.ABS_HAT0Y, -1),
	11: (ecodes.EV_ABS, ecodes.ABS_HAT0X, 1),
}

ui=UInput(spec, name='Weird Controller')
a=rtmidi.RtMidiIn()
a.openPort(1)

def handle(message):
	if message.isNoteOn():
		ui.write(*controls[message.getNoteNumber()%12])
	elif message.isNoteOff():
		ui.write(*[*controls[message.getNoteNumber()%12][:2],0])

a.setCallback(handle)

while True:
	ui.syn()
	sleep(.01)
