#!/usr/bin/python3
import argparse
import sys, time, threading
import numpy as np
import uhd
import ofdm_frame as fr
import uhd_conf as ucf
from params import *

CLOCK_TIMEOUT = 1000  # 1000ms timeout for external clock locking
INIT_DELAY    = 0.05  # 50ms initial delay before transmit

def parse_args():
    """Parse the command line arguments"""
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-a", "--args", default="addr=192.168.1.4", type=str, help="single uhd device address args")
    parser.add_argument("-d", "--duration", default=5.0, type=float,
                        help="duration for the test in seconds")
    parser.add_argument("--rate", type=float, default=10000e3,help="IQ rate(sps)") 
    parser.add_argument("--gain", type=float, default=0,help="gain") 
    parser.add_argument("--tx", type=bool, default=False,help="enableTX")
    parser.add_argument("--rx", type=bool, default=False,help="enableRX")
    return parser.parse_args()


def tx_host(usrp, tx_streamer, timer_elapsed_event):
    """Benchmark the transmit chain"""
    print(" TX freq:%.3f GHz, IQ rate %.3f MSps, gain:%.1f, ant: %s, bandwidth:%.3f MHz,spb:%d",
                 usrp.get_tx_freq()/1e9,usrp.get_tx_rate() / 1e6,usrp.get_tx_gain(),usrp.get_tx_antenna(),usrp.get_tx_bandwidth()/1e6,tx_streamer.get_max_num_samps())

    # Make a transmit buffer
    # spb = tx_streamer.get_max_num_samps()
    spb=200
    buf_length=120
    filename="./data/bits.bin"
    sdata=None
    with open(filename,"rb") as f:
        sdata=np.fromfile(f,dtype="int8",count=buf_length)
    # f=fr.frame(sdata)
    # transmit_buffer=f.frame_to_uhd_buffer(spb)
    f=fr.ofdm_frame(sdata)
    transmit_buffer=f.frame_to_buffer()
    metadata = uhd.types.TXMetadata()
    metadata.time_spec = uhd.types.TimeSpec(usrp.get_time_now().get_real_secs() + INIT_DELAY)
    metadata.has_time_spec = False
    print('begin transmit')
    while not timer_elapsed_event.is_set():
        tx_streamer.send(transmit_buffer, metadata)
    # Send a mini EOB packet
    metadata.end_of_burst = True
    tx_streamer.send(np.zeros((1,0), dtype=np.complex64), metadata)


def rx_host(usrp,rx_streamer,timer_elapsed_event):
    print(" RX freq:%.3f GHz, IQ rate %.3f MSps, gain:%.1f, ant: %s, bandwidth:%.3f MHz,spb:%d",
                 usrp.get_rx_freq()/1e9,usrp.get_rx_rate() / 1e6,usrp.get_rx_gain(),usrp.get_rx_antenna(),usrp.get_rx_bandwidth()/1e6,rx_streamer.get_max_num_samps())
    spb = rx_streamer.get_max_num_samps()
    print(spb)
    recv_buffer = np.zeros(spb, dtype=np.complex64)
    
    metadata = uhd.types.RXMetadata()

    # Craft and send the Stream Command
    stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.start_cont)
    stream_cmd.stream_now = True
    stream_cmd.time_spec = uhd.types.TimeSpec(usrp.get_time_now().get_real_secs() + INIT_DELAY)
    rx_streamer.issue_stream_cmd(stream_cmd)

    
    print('begin receive')
    with open("./data/usrp_samples.bin","w") as f:
        # Receive until we get the signal to stop
        while not timer_elapsed_event.is_set():
            rx_streamer.recv(recv_buffer, metadata)
            recv_buffer.tofile(f)
    # After we get the signal to stop, issue a stop command
    rx_streamer.issue_stream_cmd(uhd.types.StreamCMD(uhd.types.StreamMode.stop_cont))

def main():
    """Run the benchmarking tool"""
    args = parse_args()
    usrp, st_args = ucf.uhd_builder(args.args, args.gain, args.rate)

    print("..........build......\n")
    threads=[]
    tx_quit_event = threading.Event()
    rx_quit_event = threading.Event()
    if args.tx:
        tx_streamer = usrp.get_tx_stream(st_args)
        tx_thread = threading.Thread(target=tx_host,
                                    args=(usrp, tx_streamer, tx_quit_event))
        threads.append(tx_thread)
        tx_thread.start()
        tx_thread.setName("tx_stream")
    if args.rx:
        rx_streamer = usrp.get_rx_stream(st_args)
        rx_thread = threading.Thread(target=rx_host,
                                    args=(usrp, rx_streamer, rx_quit_event))
        threads.append(rx_thread)
        rx_thread.start()
        rx_thread.setName("rx_stream")
    
   
    time.sleep(args.duration)
    # Interrupt and join the threads
    print("Sending signal to stop!")
    tx_quit_event.set()
    rx_quit_event.set()
    for thr in threads:
        thr.join()

    pass

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        raise e
    finally:
        # exit()
        pass
