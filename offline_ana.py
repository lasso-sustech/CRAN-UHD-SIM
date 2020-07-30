import numpy as np
import matplotlib.pyplot as pl
from numpy.fft import fft,ifft,fftshift 

num_tones=64 ## FFT size: 64 subcarriers
num_data_tones=60
cp_len=16
indexes_null_tones=np.array([-32,-31,0,31])+32   #null_tones +index offset
indexes_data_tones=np.append(np.arange(-30,0),np.arange(1,31))+32  #data_tones +index offset
zadoff=np.exp(1j*np.pi*np.power(np.arange(0,num_data_tones),2)/num_data_tones) # zad off sequence

#------------------------------------------ Load ----------------------------------------------#
fname="recvf.txt"
b=np.fromfile(fname,dtype=np.complex64,count=2000)

#----------------------------------------- Find Offset ----------------------------------------#
sym_off=np.argmax([np.mean(np.power(np.absolute(b[i::4]),2)) for i in range(0,4)])
print("sym_off:",sym_off)
sync_symbols=b[sym_off::4]

#------------------------------------------- Frame Synchronization ---------------------------------------------#
print("sync_size",sync_symbols.size) #NOTE: only 13*6 symbols engaged
# frame sync 
bl=13*3
sc=np.empty(bl*4)
for i in range(0,bl*4):
    p=np.conjugate(sync_symbols[i:i+bl])
    n=sync_symbols[i+bl:i+bl*2]
    sc[i]=np.absolute(np.dot(p,n))
frame_off=np.argmax(sc)
print("frame_off:",frame_off)
frame_symbols=sync_symbols[frame_off:]
## coarse freq est
x=frame_symbols[:bl+26]
y=frame_symbols[13:bl+39]

und=np.dot(x.conjugate(),y) / np.dot(x.conjugate(),x) #freq_offset estimation
f = -np.angle(und)*12500000.0/(4*13*np.pi*2)
print("coarse_f:"+str(f)+'\n')
frame_symbols *= np.exp(2j*np.pi*f/12500000*4*np.arange(0,len(frame_symbols)))

#------------------------------------------- Frame Synchronization ---------------------------------------------#
## ofdm fine freq est 

cp_ofdm_symbols = frame_symbols[bl*2:]
# ox=np.conjugate(cp_ofdm_symbols[cp_len:cp_len+num_tones])
# oy=cp_ofdm_symbols[2*cp_len+num_tones:2*cp_len+2*num_tones]
# print(ox.size,oy.size)
# fine_angle=np.dot(ox.conjugate(),oy)/(np.dot(ox.conjugate(),ox))
# fine_f=-np.angle(fine_angle)*12500000.0/(4*num_tones*np.pi*2)
# print("fine_f:"+str(fine_f)+'\n')
# cp_ofdm_symbols=cp_ofdm_symbols*np.exp(2j*np.pi*fine_f/12500000*4*np.arange(0,len(cp_ofdm_symbols)))
## serial to parallel
i=cp_ofdm_symbols.size//80
cp_ofdm_symbols=cp_ofdm_symbols[:i*80]
s2p_cp_ofdm_symbols=cp_ofdm_symbols.reshape(i,80)
s2p_ofdm_symbols=s2p_cp_ofdm_symbols[:,16:]
## channel estimation
recv_pilot=fftshift(fft(s2p_ofdm_symbols[2]))[indexes_data_tones]
chest=recv_pilot/zadoff

pl.plot(np.absolute(chest))
# recv_pilot=fftshift(fft(s2p_ofdm_symbols[2]))[indexes_data_tones]
# fest=recv_pilot/zadoff
recv_sym=fftshift(fft(s2p_ofdm_symbols[3]))[indexes_data_tones]
recv_sym_eqa=recv_sym/chest
# pl.plot(recv_sym_eqa.real,recv_sym_eqa.imag,linestyle='None',marker='.')

# #symbols timing
# recv_symbols=b[::4][18:]
# i=recv_symbols.size//80
# recv_symbols=recv_symbols[:i*80]

# s2p_recv_symbols=recv_symbols.reshape(i,80)
# s2p_ofdm_symbols=s2p_recv_symbols[:,16:]

# #frame synchronization

# print(fft(s2p_ofdm_symbols[1]).size)
# recv_pilot=fftshift(fft(s2p_ofdm_symbols[2]))[indexes_data_tones]
# fest=recv_pilot/zadoff
# recv_sym=fftshift(fft(s2p_ofdm_symbols[3]))[indexes_data_tones]
# recv_sym_eqa=recv_sym/fest


pl.show()





# symbols=buf[1::4]
# print([np.mean(np.power(np.absolute(buf[i::4]),2)) for i in range(0,4)])



# # bar=np.array([1.0,1,1,1,1,-1,-1,1,1,-1,1,-1,1,1.0,1,1,1,1,-1,-1,1,1,-1,1,-1,1])

# # re=np.correlate(symbols,bar)
# bl=13*3
# i=28
# print(i)
# b=symbols[i:i+bl*2]
# symbols=symbols[i:]
# x=b[:bl+26]
# y=b[13:bl+39]
# print(symbols.size)


# und=np.dot(x.conjugate(),y)/(np.dot(x.conjugate(),x))
# f=-np.angle(und)*12500000.0/(4*13*np.pi*2)

# print(f)
# symbols=symbols*np.exp(2j*np.pi*f/12500000*4*np.arange(0,len(symbols)))

# ang=-np.mean(np.angle(symbols[26:26+5]))
# symbols=symbols*np.exp(1j*ang)


# #channel
# # t=np.array([1.0+0j,1,1,1,1,-1,-1,1,1,-1,1,-1,1])
# # chl=4
# # y=symbols[4+bl:13+bl]
# # x=np.empty((t.size-4,4),dtype=np.complex64)

# # for i in range(0,chl):
# #     for j in range(0,t.size-chl):
# #         x[j,i]=t[chl-1-i+j]
# # xh=np.conjugate(x).T
# # hn=np.matmul(np.matmul(np.linalg.inv( np.matmul(xh,x)),xh),y)

# # print(hn)

# # l=4
# # th=np.zeros((2*l-1,l),dtype=np.complex64)
# # dn=np.zeros(2*l-1,dtype=np.complex64)
# # dn[0]=1
# # for i in range(0,l):
# #     for j in range(i,i+l):
# #         th[j,i]=hn[j-i]

# # thh=np.conjugate(th).T
# # on=np.linalg.inv( np.matmul(thh,th))

# # f=np.matmul(np.matmul(on,thh),dn)
# # print(np.convolve(hn,f))

# # symbols=np.convolve(symbols,f)
# #,b.imag,linestyle='None',marker='*'
# pl.plot(symbols[bl*2:120].real,symbols[bl*2:120].imag,linestyle='None',marker='.')
# # pl.plot(symbols[:bl*2].real,symbols[:bl*2].imag,linestyle='None',marker='.')
# pl.ylim([-2,2])
# pl.xlim([-2,2])
# pl.title("sps:256")
# pl.show()

# # sc=np.empty(bl*4)
# # for i in range(0,bl*4):
# #     p=np.conjugate(symbols[i:i+bl])
# #     n=symbols[i+bl:i+bl*2]
# #     sc[i]=np.absolute(np.dot(p,n))

# # pl.plot(sc)
# # pl.plot(symbols[:bl*4])
# # pl.show()