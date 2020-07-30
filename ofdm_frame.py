#!/usr/bin/env python3
"""
    ofdm_frame
    =====================

    frame structure:
        --------------------------------------------------------
        |   barker seq  | short training  | pilot  |  payload  |
        --------------------------------------------------------
    provides:
    1. construct ofdm symbol frame 
"""
import numpy as np 
from numpy.fft import fft,ifft,fftshift 
import matplotlib.pyplot as pl
from  mod_demod import modulate,demodulate
from signal_filter import *

num_tones=64 ## FFT size: 64 subcarriers
num_data_tones=60
cp_len=16
indexes_null_tones=np.array([-32,-31,0,31])+32   #null_tones +index offset
indexes_data_tones=np.append(np.arange(-30,0),np.arange(1,31))+32  #data_tones +index offset

st_symbols=np.array([1+1j,-1-1j,1+1j,-1-1j,-1+1j,1+1j,-1-1j,-1-1j,1+1j,1+1j,1+1j,1+1j])*np.sqrt(13/6) #short training symbols
st_symbols_upsampling=np.zeros(60,np.complex64)
for i in range(st_symbols.size//2):
    st_symbols_upsampling[6+i*4]=st_symbols[i]
for i in range(st_symbols.size//2,st_symbols.size):
    st_symbols_upsampling[9+i*4]=st_symbols[i]

zadoff=np.exp(1j*np.pi*np.power(np.arange(0,num_data_tones),2)/num_data_tones) # zad off sequence

class ofdm_frame:
    def __init__(self,bin_payload:np.array,order=4):
        self.barker_sq=np.tile(np.array([1.0+0j,1,1,1,1,-1,-1,1,1,-1,1,-1,1],dtype=np.complex64),6)
        self.train_seq=data_to_cp_ofdm(st_symbols_upsampling,2)
        self.pilot_seq=data_to_cp_ofdm(zadoff)
        self.payload = ofdm_modulate(modulate(bin_payload,order))

    def frame_to_buffer(self):
        padlen=16
        padding=np.full(padlen,0.1+0.1j,dtype=np.complex64) #NOTE: Inter-Frame Interval
        padzeros=np.zeros(120,dtype=np.complex64)
        ofdm_symbol=np.concatenate((self.train_seq,self.pilot_seq,self.payload))
        ofdm_symbol=ofdm_symbol/np.max(np.absolute(ofdm_symbol))
        frame_symbol=np.concatenate( [padding,self.barker_sq,ofdm_symbol,padding,padzeros] )
        buffer=pulse_shaping(frame_symbol,4,0.8,2)
        
        sym_energy=np.max(np.absolute(buffer))
        buffer=buffer/sym_energy
        buffer=buffer[:363*6]
        buffer=buffer*np.exp(-2j*np.pi*80000/12500000*np.arange(0,363*6,dtype=np.float32))
        print(buffer.size)
        buffer=buffer.reshape(1,-1)
        return buffer
    pass

def data_to_cp_ofdm(data,rpt_num=1):
    fft_data=np.zeros(64,dtype=np.complex64)
    fft_data[indexes_data_tones]=data 
    ofdm_symbol=ifft(fftshift(fft_data))
    cp_ofdm_data=np.append(ofdm_symbol[num_tones-cp_len:],ofdm_symbol)
    if rpt_num ==1:
        return cp_ofdm_data
    else:
        return np.tile(cp_ofdm_data,rpt_num)

def ofdm_modulate(symbols:np.array):
    assert symbols.size %60 ==0, "modulated symbols size is not multiple times of 64"
    
    s2p_symbols=np.reshape(symbols,(symbols.size//num_data_tones,num_data_tones))  # 2 dimentional array, one row vector represent 60 data carrier symbols
    
    s2p_cp_ofdm_symbols=np.zeros((symbols.size//num_data_tones,num_tones+cp_len),dtype=np.complex64)
    
    for i in np.arange(0,symbols.size//num_data_tones):
        s2p_cp_ofdm_symbols[i]=data_to_cp_ofdm(s2p_symbols[i])
    
    return s2p_cp_ofdm_symbols.reshape(1,-1)[0]  #parallel to serial

# f=ofdm_frame(np.random.choice([1,0],120))
# b=f.frame_to_buffer()



# b=matched_filter(b,4,0.9,2)
# #symbols timing
# sym_off=np.argmax([np.mean(np.power(np.absolute(b[i::4]),2)) for i in range(0,4)])
# sync_symbols=b[sym_off::4]
# # frame sync 
# bl=13*3
# sc=np.empty(bl*4)
# for i in range(0,bl*4):
#     p=np.conjugate(sync_symbols[i:i+bl])
#     n=sync_symbols[i+bl:i+bl*2]
#     sc[i]=np.absolute(np.dot(p,n))
# frame_off=np.argmax(sc)
# frame_symbols=sync_symbols[frame_off:]
# ## coarse freq est
# x=frame_symbols[:bl+26]
# y=frame_symbols[13:bl+39]

# und=np.dot(x.conjugate(),y)/(np.dot(x.conjugate(),x))
# f=-np.angle(und)*12500000.0/(4*13*np.pi*2)
# print("coarse_f:"+str(f)+'\n')

# frame_symbols=frame_symbols*np.exp(2j*np.pi*f/12500000*4*np.arange(0,len(frame_symbols)))

# ## ofdm fine freq est 

# cp_ofdm_symbols=frame_symbols[bl*2:]
# ox=np.conjugate(cp_ofdm_symbols[cp_len:cp_len+num_tones])
# oy=np.conjugate(cp_ofdm_symbols[2*cp_len+num_tones:2*cp_len+2*num_tones])
# fine_angle=np.dot(ox.conjugate(),oy)/(np.dot(ox.conjugate(),ox))
# fine_f=-np.angle(fine_angle)*12500000.0/(4*num_tones*np.pi*2)
# print("fine_f:"+str(f)+'\n')
# cp_ofdm_symbols=cp_ofdm_symbols*np.exp(2j*np.pi*fine_f/12500000*4*np.arange(0,len(cp_ofdm_symbols)))

# ## serial to parallel
# i=cp_ofdm_symbols.size//80
# cp_ofdm_symbols=cp_ofdm_symbols[:i*80]
# s2p_cp_ofdm_symbols=cp_ofdm_symbols.reshape(i,80)
# s2p_ofdm_symbols=s2p_cp_ofdm_symbols[:,16:]
# ## channel estimation
# recv_pilot=fftshift(fft(s2p_ofdm_symbols[2]))[indexes_data_tones]
# chest=recv_pilot/zadoff
# pl.plot(np.absolute(chest))
# # recv_pilot=fftshift(fft(s2p_ofdm_symbols[2]))[indexes_data_tones]
# # fest=recv_pilot/zadoff
# # recv_sym=fftshift(fft(s2p_ofdm_symbols[3]))[indexes_data_tones]
# # recv_sym_eqa=recv_sym/fest

# # #symbols timing
# # recv_symbols=b[::4][18:]
# # i=recv_symbols.size//80
# # recv_symbols=recv_symbols[:i*80]

# # s2p_recv_symbols=recv_symbols.reshape(i,80)
# # s2p_ofdm_symbols=s2p_recv_symbols[:,16:]

# # #frame synchronization

# # print(fft(s2p_ofdm_symbols[1]).size)
# # recv_pilot=fftshift(fft(s2p_ofdm_symbols[2]))[indexes_data_tones]
# # fest=recv_pilot/zadoff
# # recv_sym=fftshift(fft(s2p_ofdm_symbols[3]))[indexes_data_tones]
# # recv_sym_eqa=recv_sym/fest


# pl.show()