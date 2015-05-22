class Meter(object):
    def __init__(self, samplerate=44100):
        ### state
        self.w1 = 450.0  / samplerate       # attack filter coeff
        self.w2 = 1300.0 / samplerate       # attack filter coeff
        self.w3 = 1.0 - 5.4 / samplerate    # release filter coeff
        self.g  = 0.5108                    # gain factor
        self.z1 = 0                         # filter state
        self.z2 = 0                         # filter state
        self.m  = 0                         # max value since last read

    ### lambda helpers (internal use)
    clamp = lambda self, n, minn, maxn: max(min(maxn, n), minn)
    applyfilt = lambda self, t, z, w: (t - z) * w if t > z else 0

    ### The main process block:
    ### input  : an array of sampled signal values
    def process(self, block):
        z1 = self.clamp(self.z1, 0, 20)
        z2 = self.clamp(self.z2, 0, 20)
        m = 0

        for i in range(0, len(block), 4):
            z1 *= self.w3
            z2 *= self.w3
            for j in range(i, i + 4):
                t = abs(block[j])
                z1 += self.applyfilt(t, z1, self.w1)
                z2 += self.applyfilt(t, z2, self.w2)
            t = z1 + z2;
            if t > m: m = t

        self.z1 = z1 + 1e-10
        self.z2 = z1 + 1e-10
        self.m = m
        return self.g * self.m