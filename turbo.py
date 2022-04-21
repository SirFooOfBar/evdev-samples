from evdev import UInput, InputDevice, ecodes

dev = InputDevice('/dev/input/event24')
dev.grab()

spec=dev.capabilities()
spec={ key:value for (key,value) in spec.items() if key in (ecodes.EV_ABS, ecodes.EV_KEY) }

ui=UInput(spec, name='Turbo Controller')

a=True
while True:
	for b in dev.active_keys():
		ui.write(ecodes.EV_KEY, b, 1 if a else 0)
	a=not a
