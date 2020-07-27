import numpy as np
import matplotlib.pyplot as pl 
# from scipy import signal

def rrc(sps,rc,sl):
    if int(rc*4*sps*sl*125)%2==0:
        rc=rc-0.000001
        
    idx=np.linspace(-sl/2.0,sl/2.0,sps*sl+1,dtype=np.float32)
    f= ((np.cos((1+rc)*np.pi*idx)*4*rc/np.pi)+((np.sinc((1-rc)*idx))*(1-rc)))/((1-(4*rc*idx)**2)*np.sqrt(sps))
    return f

def pulse_shaping(modsymbols,sps,rc,sl):
    ns=np.zeros(sps*modsymbols.size,dtype=np.complex64)
    ns[::sps]=modsymbols[:]
    f=rrc(sps,rc,sl)
    
    sig=np.convolve(ns,f)
    
    return sig

def matched_filter(recvsamples,sps,rc,sl):
    f=rrc(sps,rc,sl)

    sig=np.convolve(recvsamples,f)
    return sig

