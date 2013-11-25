from mininet.node import Host

def transferFileUsingNc6(hostA,hostC,transferSize):
    if transferSize == "short":
        bytesT = (1500*64)-(18*64)
    elif transferSize == "medium":
        bytesT = (1500*128)-(18*128)
    elif transferSize == "long":
        bytesT = (1500*256)-(18*256)
    hostA.cmd("dd if=/dev/zero of=temp count="+bytesT+" bs=1")
	hostA.cmd("nc6 -X -l -p 7676 < temp &")
	hostC.cmd("nc6 -X 192.168.1.2 7676 > /dev/null")
    hostA.cmd("rm temp")