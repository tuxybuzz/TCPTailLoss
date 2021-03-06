import dpkt
import sys


def filterPackets(pcap):
    """Filters the packets of the transmission being observed"""
    filtered_pkts = []
    for ts, buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        ip = eth.data
        tcp = ip.data
        if type(tcp) == dpkt.tcp.TCP:
            if tcp.sport == 7676 or tcp.dport == 7676:
                filtered_pkts.append((ts, eth))
    return filtered_pkts


def getCompletionTime(filtered_pkts):
    """Returns the time taken to complete the Transmission"""
    return filtered_pkts[-1][0] - filtered_pkts[0][0]


def getRetransmissionTime(filtered_pkts):
    """Returns the time taken for retransmission of a packet from
        the time of the first lost data packet.
        This is achieved by keeping track of sequence numbers,
        first packet with a retransmission, and the first lost.
    """
    first_lost_seq = ''
    first_lost = 0
    first_retrans = 0
    seq_list = []
    retrans = False
    for ts, pkt in filtered_pkts:
        if pkt.data.len == 1500 and pkt.data.data.sport == 7676:
            for ts_e, pkt_e in seq_list:
                if pkt.data.data.seq == pkt_e.data.data.seq:
                    if retrans is False:
                        first_retrans = ts
                        first_lost = ts_e
                        first_lost_seq = pkt_e.data.data.seq
                        retrans = True
                    elif pkt_e.data.data.seq < first_lost_seq:
                        first_lost_seq = pkt_e.data.data.seq
                        first_lost = ts_e
            seq_list.append((ts, pkt))
    return first_retrans - first_lost


if __name__ == "__main__":
    pcap_file = sys.argv[1]
    f = open(pcap_file)
    pcap = dpkt.pcap.Reader(f)
    filtered_pkts = filterPackets(pcap)
    completion_time = getCompletionTime(filtered_pkts)
    retransmission_time = getRetransmissionTime(filtered_pkts)
    print(str(completion_time) + "\t" + str(retransmission_time))
