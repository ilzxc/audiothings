import socket, struct, sys
import pyaudio
from meter import * 

### TODO : make a package to avoid the following:
sys.path.append('..')
from odotsetup import *

### udp socket stuff:
RINFO = ('127.0.0.1', 56765)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Sending udp packets to " + str(RINFO))
def send(message): sock.sendto(message.getBytes(), RINFO) ### assumes o.bundle

### pyAudio:
audio_format = pyaudio.paFloat32
channels = 1
rate = 44100
chunk = 1024
struct_format = str(chunk) + 'f' ### stream.read outputs a buffer as a string, cast using '<chunk>f'

audio = pyaudio.PyAudio()
stream = audio.open(format = audio_format, channels = channels, rate = rate, input = True, frames_per_buffer = chunk)
meter = Meter(rate)

### main loop:
try:
    while True:
        data = struct.unpack(struct_format, stream.read(chunk))
        b = o.bundle( messages = [o.message('/meter', meter.process(data))] )
        send(b)
except KeyboardInterrupt:
    stream.stop_stream()
    stream.close()
    audio.terminate()
    sock.close()
    print("\nCleanup successful")
