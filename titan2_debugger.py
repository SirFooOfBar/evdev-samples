import hid, os, ctypes, time

ACTIVATE=int.to_bytes(0xf0,64,'little')
DISACTIVATE=int.to_bytes(0xf1,64,'little')
CONTROLLER_DATA_HEADER=0x13

try:
	t2=hid.device()
	t2.open(vendor_id=0x2508, product_id=0x0032)	#lsusb
	t2.write(ACTIVATE)
	out=''

	while data:=[ctypes.c_int8(byte).value for byte in t2.read(64)]:
		if data[0] != CONTROLLER_DATA_HEADER:
			continue

		if data[3]==0:
			if time.time_ns()%5==0:
				os.system("clear")
				print(out)
			out=''

		for i in range(0,64):
			out+="%2d: %4d" % (i,data[i])+'|' if i%8!=7 else '\n'
		out+='\n'

except Exception as e:
	print("An exception has occured: "+str(e))

finally:
	t2.write(DISACTIVATE)
