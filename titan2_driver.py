from evdev import UInput, AbsInfo, ecodes as e
import hid, ctypes

ACTIVATE=int.to_bytes(0xf0,64,'little')
DISACTIVATE=int.to_bytes(0xf1,64,'little')
CONTROLLER_DATA_HEADER=0x13

controls=[

	[
		(61,e.EV_KEY,e.BTN_B),
		(57,e.EV_KEY,e.BTN_Y),
		(29,e.EV_KEY,e.BTN_TL),
		(17,e.EV_KEY,e.BTN_TR),
		(33,e.EV_ABS,e.ABS_Z),
		(21,e.EV_ABS,e.ABS_RZ),
		(13,e.EV_KEY,e.BTN_START),
		(9,e.EV_KEY,e.BTN_SELECT),
		(5,e.EV_KEY,e.BTN_MODE),
		(37,e.EV_KEY,e.BTN_THUMBL),
		(25,e.EV_KEY,e.BTN_THUMBR),
		([41,45],e.EV_ABS,e.ABS_HAT0Y),
		([49,53],e.EV_ABS,e.ABS_HAT0X),
	],
	[
		(13,e.EV_KEY,e.BTN_PINKIE),
		(5,e.EV_KEY,e.BTN_A),
		(9,e.EV_KEY,e.BTN_X),
		(37,e.EV_ABS,e.ABS_X),
		(41,e.EV_ABS,e.ABS_Y),
		(29,e.EV_ABS,e.ABS_RX),
		(33,e.EV_ABS,e.ABS_RY),
	],
	[],
]

spec = {
	e.EV_KEY:[
		e.BTN_A, e.BTN_B, e.BTN_X, e.BTN_Y, #e.BTN_PINKIE,
		e.BTN_TL, e.BTN_TR, e.BTN_SELECT, e.BTN_START,
		e.BTN_THUMBL, e.BTN_THUMBR, e.BTN_MODE],
	e.EV_ABS:[
		(e.ABS_X, AbsInfo(value=0, min=-100, max=100, fuzz=0, flat=0, resolution=0)),
		(e.ABS_Y, AbsInfo(value=0, min=-100, max=100, fuzz=0, flat=0, resolution=0)),
		(e.ABS_Z, AbsInfo(value=0, min=-100, max=100, fuzz=0, flat=0, resolution=0)),
		(e.ABS_RX, AbsInfo(value=0, min=-100, max=100, fuzz=0, flat=0, resolution=0)),
		(e.ABS_RY, AbsInfo(value=0, min=-100, max=100, fuzz=0, flat=0, resolution=0)),
		(e.ABS_RZ, AbsInfo(value=0, min=-100, max=100, fuzz=0, flat=0, resolution=0)),
		(e.ABS_HAT0X, AbsInfo(value=0, min=-100, max=100, fuzz=0, flat=0, resolution=0)),
		(e.ABS_HAT0Y, AbsInfo(value=0, min=-100, max=100, fuzz=0, flat=0, resolution=0)),
]}

ui=UInput(spec, name='Titan-Two Monitoring Device')

try:
	t2=hid.Device(vid=0x2508,pid=0x0032)
	t2.write(ACTIVATE)

	while data:=[ctypes.c_int8(a).value for a in t2.read(64)]:
		if data[0] != CONTROLLER_DATA_HEADER:
			continue

		for i, inputType, code in controls[data[3]]:
			if type(i) is list:
				n,p=i
				ui.write(inputType,code,data[p]-data[n])
			elif inputType == e.EV_ABS:
				ui.write(inputType,code,data[i])
			else:
				ui.write(inputType,code,data[i]>1)
		ui.syn()

except KeyboardInterrupt:
	print("Keyboard inturrupt recieved, stopping...")

except OSError:
	print("Device was disconnected")
	t2=None

finally:
	if t2:
		t2.write(DISACTIVATE)
