import pyaudio
import numpy as np
import matplotlib.pyplot as plt

SAMPLING_RATE = 44100
DURATION = 15
TOTAL_SAMPLES = SAMPLING_RATE*DURATION

def line(start_freq, end_freq, start_time, end_time):
	epsilon = 0.05
	xs = np.linspace(start_freq, end_freq, TOTAL_SAMPLES)
	vs = np.concatenate([
		np.linspace(0, 0, abs(int(SAMPLING_RATE*(start_time-epsilon)))),
		np.linspace(0, 2, abs(int(SAMPLING_RATE*epsilon))),
		np.linspace(2, 2, abs(int(SAMPLING_RATE*(end_time-start_time)))),
		np.linspace(2, 0, abs(int(SAMPLING_RATE*epsilon))),
		np.linspace(0, 0, abs(int(SAMPLING_RATE*(DURATION-end_time))))
		])
	m = min(len(xs), len(vs))
	return xs[:m], vs[:m]

p = pyaudio.PyAudio()

volume = 0.2   # range [0.0, 1.0]
       # sampling rate, Hz, must be integer

t1 = np.concatenate([
	np.linspace(320, 1050, int(SAMPLING_RATE*0.5)),
	np.linspace(0, 0, int(SAMPLING_RATE*4.5)),
	# np.linspace(0, 0, int(SAMPLING_RATE*3.3))
	])
v1 = np.concatenate([
	np.linspace(0, 2, int(SAMPLING_RATE*0.1)),
	np.linspace(2, 2, int(SAMPLING_RATE*0.3)),
	np.linspace(2, 0, int(SAMPLING_RATE*0.1)),
	np.linspace(2, 2, int(SAMPLING_RATE*1)),
	np.linspace(0, 0, int(SAMPLING_RATE*3.3))
	])
t2 = np.concatenate([
	np.linspace(0, 0, int(SAMPLING_RATE*1)),
	np.linspace(975, 970, int(SAMPLING_RATE*4))
	])
v2 = np.concatenate([
	np.linspace(2, 2, int(SAMPLING_RATE*1)),
	np.linspace(2, 2, int(SAMPLING_RATE*4))
	])
print(len(t2), len(v2))
# t2 = line(1050, 1050, 1.4, 2)
# t3 = line(975, 975, 2, 4)


# # generate samples, note conversion to float32 array
# l = np.linspace(270, 970, int(fs*duration))

# # samples = (np.sin(2*np.pi*l/fs)).astype(np.float32)

# # for paFloat32 sample values must be in range [-1.0, 1.0]


# # play. May repeat with different volume values (if done interactively) 
# b2 =  np.arange(fs*5)
# s2 = np.sin(2*np.pi*b2*970/fs).astype(np.float32)


# freq_graph = np.concatenate([t1, t2+t3])
# freq_graph = t1+t2+t3

tracks = [ # Implement attack duration sustain etc..
	line(285, 990, 8, 8.1), line(990, 990, 8.1, 8.2),
	line(990, 1050, 8.2, 8.3), line(1050, 1050, 8.3, 9.3),
	line(970, 970, 8.7, 14.8),
	line(1165, 1165, 10.1, 10.7), line(1165, 250, 10.7, 10.8),
	]

for i in range(4):
	for freq in [100, 200, 300]:
		for start in range(DURATION):
			tracks.append(line(freq, freq, start+0.2*i, start+0.2*i+0.01))

# plt.figure(0)
# for track, volume in tracks:
# 	plt.plot(track)
# plt.figure(1)
# for track, volume in tracks:
# 	plt.plot(volume)
# plt.show()

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=SAMPLING_RATE,
                output=True)

min_duration = float('inf')
for track, v in tracks:
	if len(track) < min_duration:
		min_duration = len(track)
	if len(v) < min_duration:
		min_duration = len(v)
base = np.arange(min_duration)
print(min_duration/SAMPLING_RATE)
# print(len(base))
# tracks = [(t1[:min_duration], v1[:min_duration])]#, (t2[:min_duration], v2[:min_duration])]

samples = 0.0*base
for track, v in tracks:
	# print(len(track), len(v))
	samples += (v/10)*(np.sin(2*np.pi*track*base/SAMPLING_RATE))
# plt.plot(samples)
# plt.show()

samples = samples.astype(np.float32).tobytes()

stream.write(samples)
stream.stop_stream()
stream.close()
p.terminate()