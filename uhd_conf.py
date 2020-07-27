#!/usr/bin/env python3
import uhd, logging
from params import *

UHD_OTW  = "sc16"
UHD_CPU  = "fc32"

def uhd_builder(args=UHD_DEFAULT_ARGS, gain=UHD_DEFAULT_GAIN, rate=UHD_DEFAULT_RATE):
    usrp=uhd.usrp.MultiUSRP(args)
    logging.info("usrp created")
    usrp.set_clock_source("internal")
    usrp.set_time_source("none")
    logging.info("Setting device timestamp to 0...")
    usrp.set_time_now(uhd.types.TimeSpec(0.0))

    usrp.set_tx_rate(rate)
    usrp.set_tx_gain(0)
    usrp.set_tx_antenna("TX/RX")
    usrp.set_tx_bandwidth(40e6)
    usrp.set_tx_freq(uhd.libpyuhd.types.tune_request(0), 0)

    usrp.set_rx_rate(rate)
    usrp.set_rx_gain(0)
    usrp.set_rx_antenna("RX2")
    usrp.set_rx_bandwidth(40e6)
    usrp.set_rx_freq(uhd.libpyuhd.types.tune_request(0), 0)
    
    st_args = uhd.usrp.StreamArgs(UHD_CPU, UHD_OTW)
    st_args.channels=[0]
    return (usrp, st_args)
