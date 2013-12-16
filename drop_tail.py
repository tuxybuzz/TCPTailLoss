import sys
import nfqueue
from socket import AF_INET

count = 0
dropped = False
drop_count = 0


def callback(handle, new_handle=None):
    """
        This function causes Tail Drop
    """
    global count
    global dropped
    global drop_count
    count = count + 1
    if new_handle is not None:
        handle = new_handle
    if count > 50 and dropped is not True:
        drop_count = drop_count - 1
        if drop_count == 0:
            dropped = True
        handle.set_verdict(nfqueue.NF_DROP)
    handle.set_verdict(nfqueue.NF_ACCEPT)

if __name__ == "__main__":
    global payload_length
    global drop_count
    payload_length = sys.argv[0]
    drop_count = sys.argv[1]
    print("Started")
    q = nfqueue.queue()
    family = AF_INET
    q.set_callback(callback)
    q.fast_open(0, family)
    q.try_run()
