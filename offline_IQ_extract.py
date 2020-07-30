import numpy as np
import filter
import matplotlib.pyplot as pl

with open("usrp_samples.dat","rb") as f:
    np.fromfile(f,dtype=np.complex64,count=20000000)
    buf=np.fromfile(f,dtype=np.complex64,count=20000000)
    # pl.plot(np.absolute(buf))
    buffer=filter.matched_filter(buf,4,0.8,2)-np.complex(0,0)
    # b=(buffer)[2000:4800] #NOTE: extract part
    # print(b.dtype)
    b.tofile("recvf.txt")
    pl.plot(buf.real)
    pl.plot(buf.imag)
    # pl.plot(buf.imag)
    pl.show()