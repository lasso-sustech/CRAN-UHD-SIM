"""
mod_demod
=========

provides:
    1. modulation scheme for 2,4,16 QAM
    2. demodulation scheme for 2,4,16 QAM
usage:
    modulate(input:array,modorder:integer)->array
    demodulate(input:array,modorder:integer) ->array

"""
import numpy as np

mod_lut={
    # BPSK
    2: np.array([-1+0j,1+0j]),
    # 4-QAM
    4: np.array([-1-1j,-1+1j,1+1j,1-1j]) / np.sqrt(2),
    # 16-QAM
    16: np.array([-3-3j,-1-3j,3-3j,1-3j,-3-1j,-1-1j,3-1j,1-1j,-3+3j,-1+3j,3+3j,1+3j,-3+1j,-1+1j,3+1j,1+1j]) / np.sqrt(10),
    #64 QAM
    64: np.array([  (-7-7j), (-5-7j), (-1-7j), (-3-7j), (7-7j), (5-7j), (1-7j), (3-7j), \
                    (-7-5j), (-5-5j), (-1-5j), (-3-5j), (7-5j), (5-5j), (1-5j), (3-5j), \
                    (-7-1j), (-5-1j), (-1-1j), (-3-1j), (7-1j), (5-1j), (1-1j), (3-1j), \
                    (-7-3j), (-5-3j), (-1-3j), (-3-3j), (7-3j), (5-3j), (1-3j), (3-3j), \
                    (-7+7j), (-5+7j), (-1+7j), (-3+7j), (7+7j), (5+7j), (1+7j), (3+7j), \
                    (-7+5j), (-5+5j), (-1+5j), (-3+5j), (7+5j), (5+5j), (1+5j), (3+5j), \
                    (-7+1j), (-5+1j), (-1+1j), (-3+1j), (7+1j), (5+1j), (1+1j), (3+1j), \
                    (-7+3j), (-5+3j), (-1+3j), (-3+3j), (7+3j), (5+3j), (1+3j), (3+3j)]) / np.sqrt(42),
    #256QAM
    256: np.array([ (-15-15j), (-13-15j), (-9-15j), (-11-15j), (-1-15j), (-3-15j), (-7-15j), (-5-15j),  \
                    (15-15j), (13-15j), (9-15j), (11-15j), (1-15j), (3-15j), (7-15j), (5-15j), \
                    (-15-13j), (-13-13j), (-9-13j), (-11-13j), (-1-13j), (-3-13j), (-7-13j), (-5-13j), \
                    (15-13j), (13-13j), (9-13j), (11-13j), (1-13j), (3-13j), (7-13j), (5-13j), \
                    (-15-9j), (-13-9j), (-9-9j), (-11-9j), (-1-9j), (-3-9j), (-7-9j), (-5-9j), \
                    (15-9j), (13-9j), (9-9j), (11-9j), (1-9j), (3-9j), (7-9j), (5-9j), \
                    (-15-11j), (-13-11j), (-9-11j), (-11-11j), (-1-11j), (-3-11j), (-7-11j), (-5-11j), \
                    (15-11j), (13-11j), (9-11j), (11-11j), (1-11j), (3-11j), (7-11j), (5-11j), \
                    (-15-1j), (-13-1j), (-9-1j), (-11-1j), (-1-1j), (-3-1j), (-7-1j), (-5-1j), \
                    (15-1j), (13-1j), (9-1j), (11-1j), (1-1j), (3-1j), (7-1j), (5-1j),\
                    (-15-3j), (-13-3j), (-9-3j), (-11-3j), (-1-3j), (-3-3j), (-7-3j), (-5-3j), \
                    (15-3j), (13-3j), (9-3j), (11-3j), (1-3j), (3-3j), (7-3j), (5-3j), \
                    (-15-7j), (-13-7j), (-9-7j), (-11-7j), (-1-7j), (-3-7j), (-7-7j), (-5-7j), \
                    (15-7j), (13-7j), (9-7j), (11-7j), (1-7j), (3-7j), (7-7j), (5-7j), \
                    (-15-5j), (-13-5j), (-9-5j), (-11-5j), (-1-5j), (-3-5j), (-7-5j), (-5-5j), \
                    (15-5j), (13-5j), (9-5j), (11-5j), (1-5j), (3-5j), (7-5j), (5-5j), \
                    (-15+15j), (-13+15j), (-9+15j), (-11+15j), (-1+15j), (-3+15j), (-7+15j), (-5+15j), \
                    (15+15j), (13+15j), (9+15j), (11+15j), (1+15j), (3+15j), (7+15j), (5+15j), \
                    (-15+13j), (-13+13j), (-9+13j), (-11+13j), (-1+13j), (-3+13j), (-7+13j), (-5+13j), \
                    (15+13j), (13+13j), (9+13j), (11+13j), (1+13j), (3+13j), (7+13j), (5+13j), \
                    (-15+9j), (-13+9j), (-9+9j), (-11+9j), (-1+9j), (-3+9j), (-7+9j), (-5+9j), \
                    (15+9j), (13+9j), (9+9j), (11+9j), (1+9j), (3+9j), (7+9j), (5+9j), \
                    (-15+11j), (-13+11j), (-9+11j), (-11+11j), (-1+11j), (-3+11j), (-7+11j), (-5+11j), \
                    (15+11j), (13+11j), (9+11j), (11+11j), (1+11j), (3+11j), (7+11j), (5+11j), \
                    (-15+1j), (-13+1j), (-9+1j), (-11+1j), (-1+1j), (-3+1j), (-7+1j), (-5+1j), \
                    (15+1j), (13+1j), (9+1j), (11+1j), (1+1j), (3+1j), (7+1j), (5+1j), \
                    (-15+3j), (-13+3j), (-9+3j), (-11+3j), (-1+3j), (-3+3j), (-7+3j), (-5+3j), \
                    (15+3j), (13+3j), (9+3j), (11+3j), (1+3j), (3+3j), (7+3j), (5+3j), \
                    (-15+7j), (-13+7j), (-9+7j), (-11+7j), (-1+7j), (-3+7j), (-7+7j), (-5+7j), \
                    (15+7j), (13+7j), (9+7j), (11+7j), (1+7j), (3+7j), (7+7j), (5+7j), \
                    (-15+5j), (-13+5j), (-9+5j), (-11+5j), (-1+5j), (-3+5j), (-7+5j), (-5+5j), \
                    (15+5j), (13+5j), (9+5j), (11+5j), (1+5j), (3+5j), (7+5j), (5+5j)]) / np.sqrt(170)
}


def modulate(sdata:np.array,order:int)-> np.array:
    """[summary]

    Args:
        sdata (np.array): [source data array]
        order ([type], optional): [modulation order]. Defaults to 4:int. now support 2,4,16

    Returns:
        np.array: [return IQ samples]
    """
    assert order in [2,4,16,64,256], "modulation does not support order:{}\n".format(order)
    assert sdata.size %(np.log2(order)) ==0, "length of source data is not multiple integer times of specified modulation order:{} with symbol length{}\n".format(order,np.log2(order))


    mod_ord_lut=mod_lut[order] # modulation and demodulation look up table
    decdata=0 #decimal source data ,e,g for 16QAM, [0,1,2,...15] <--[0000,0001,...1111]

    #implement 2,4,16 QAM modulation
    log_ord=int(np.log2(order))
    for i in np.arange(0,log_ord):
        decdata+=sdata[i::log_ord]*np.power(2,log_ord-1-i)  ##transfer binary integer sequence to decimal sequence

    return np.vectorize(lambda x: mod_ord_lut[x])(decdata)    ## lambda function: index look up table to acquire symbol. vectorize method to manipulate 


def demodulate(iqdata:np.array,order:int)-> np.array:
    """demodulate IQ samples to bit string

    Args:
        iqdata (np.array): IQ baseband samples
        order (int): demodulation order

    Returns:
        np.array: [return bit string]
    """

    ## 1. nearest neighbor demodulation
    ## 2. map IQ to bitstring

    assert order in [2,4,16,64,256], "demodulation does not support order:{}\n".format(order)
    
    log2_ord=int(np.log2(order))
    demod_ord_lut=mod_lut[order] # demodulation order look up table entry
    entry_indexes=np.vectorize(lambda x: np.argmin(np.abs(x-demod_ord_lut)))(iqdata) #nearest neighbor demodulation (entry index array)
    nnds=np.vectorize(lambda x: demod_ord_lut[x])(entry_indexes)
    decoded_mes=np.array([ np.array([(x & (1 << i)) >>i for i in np.arange(log2_ord-1,-1,-1)]) for x in entry_indexes]) ## to binary string
    decoded_mes=decoded_mes.reshape(1,-1)[0]

    return nnds,decoded_mes ## TODO to binary array
