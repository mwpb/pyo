from pyo import *
import numpy as np
import matplotlib.pyplot as plt

SAMPLING_RATE = 44100
DURATION = 4

def line(f1, f2, t1, t2, x):
	f1, f2, t1, t2 = float(f1), float(f2), float(t1), float(t2)
	return f1+(((f2-f1)/(t2-t1)))*(x-t1)

def fun_a(x):
	if 0 <= x <= 0.3:
		return line(280, 990, 0, 0.3, x)
	elif 0.3 < x < 0.4:
		return 990
	elif 0.4 < x < 0.45:
		return line(990, 1055, 0.4, 0.45, x)
	elif 0.45 < x < 0.5:
		return line(1055, 970, 0.45, 0.5, x)
	if 0.5 < x < 7:
		return 970
	else:
		return 0

def fun_b(x):
	if 3.2 < x < 3.6:
		return 1170
	elif 3.6 < x < 3.7:
		return line(1170, 260, 3.6, 3.7, x)
	else: 
		return 0


test_track = [fun_a(x) for x in range(4)]

track_a = [fun_a(float(x)/SAMPLING_RATE) for x in range(SAMPLING_RATE*DURATION)]
track_b = [fun_b(float(x)/SAMPLING_RATE) for x in range(SAMPLING_RATE*DURATION)]
# for i in range(SAMPLING_RATE*DURATION//2):
# 	track_a[i] = 900
# for i in range(SAMPLING_RATE*DURATION//2, SAMPLING_RATE*DURATION):
# 	track_a[i] = 400

# plt.plot(track_a)
# plt.plot(track_b)
# plt.show()

s = Server().boot()
s.start()

a = Sine(mul=0.2).out()
b = Sine(mul=0.2).out()
beat_lower = Sine(mul=0.3).out()
beat_upper = Sine(mul=0.3).out()
beat_lower.setFreq(800)
beat_upper.setFreq(790)

flip = False
def inc_freq():
	global flip
	if flip:
		beat_lower.setFreq(800)
		beat_upper.setFreq(795)
	else:
		beat_lower.setFreq(0)
		beat_upper.setFreq(0)
	flip = not flip

m = Pattern(inc_freq, 1)
m.play()

for i in range(SAMPLING_RATE*DURATION):
	time.sleep(1/SAMPLING_RATE)
	a.setFreq(track_a[i])
	b.setFreq(track_b[i])
raw_input()
s.stop()