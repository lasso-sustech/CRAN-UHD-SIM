import numpy as np
import matplotlib.pyplot as pl 
# from scipy import signal

PI=np.pi

def rrc(sps, rc, sl):
    if int(rc*4*sps*sl*125)%2==0:
        rc=rc-0.000001
        
    idx=np.linspace(-sl/2.0,sl/2.0,sps*sl+1,dtype=np.float32)
    _a = np.cos( (1+rc)*PI*idx ) * 4 * rc/PI
    _b = np.sinc( (1-rc)*idx ) * (1-rc)
    _c = ( 1 - (4*rc*idx)**2 ) * np.sqrt(sps)
    f= (_a + _b) / _c
    return f

def pulse_shaping(modsymbols,sps,rc,sl):
    ns = np.zeros(sps*modsymbols.size, dtype=np.complex64)
    ns[::sps] = modsymbols[:]
    f   = rrc(sps, rc, sl)
    sig = np.convolve(ns, f)
    return sig

def matched_filter(recvsamples,sps,rc,sl):
    f   = rrc(sps,rc,sl)
    sig = np.convolve(recvsamples,f)
    return sig
