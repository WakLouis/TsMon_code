import datetime
import json

import dpkt
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import pytz


class QueueElement:
    def __init__(self, Type, data):
        self.Type = Type
        self.QueueID = int.from_bytes(data[0:4], 'big')
        self.EnterTime_S = int.from_bytes(data[4:8], 'big')
        self.EnterTime_NS = int.from_bytes(data[8:12], 'big')
        self.PeakCnt = int.from_bytes(data[12:16], 'big')
        self.PeakTime = int.from_bytes(data[16:20], 'big')
        self.ExitTime_S = int.from_bytes(data[20:24], 'big')
        self.ExitTime_NS = int.from_bytes(data[24:28], 'big')
        self.MaxEnqueRate = int.from_bytes(data[28:32], 'big')
        self.MaxLatency = int.from_bytes(data[32:36], 'big')

        self.RxPktCnt = int.from_bytes(data[48:52], 'big')
        self.RxByteCnt = int.from_bytes(data[52:56], 'big')
        self.DropPktCnt = int.from_bytes(data[56:60], 'big')
        self.DropByteCnt = int.from_bytes(data[60:64], 'big')

    def transform_to_Beijing_time(self, timestamp_s, timestamp_ns):
        turn_over = ((((timestamp_s - 1) * 10 ** 9) - timestamp_ns) & 0xffffffff) != 0
        N = ((((timestamp_s - 1) * 10 ** 9) - timestamp_ns) >> 32) + turn_over
        time = ((N << 32) + timestamp_ns) / 10 ** 9
        dt = datetime.utcfromtimestamp(time)
        beijing_tz = pytz.timezone('Asia/Shanghai')
        return dt.replace(tzinfo=beijing_tz)

    def get_dict(self):
        return {"QueueID": self.QueueID,
                "EnterTime (Beijing)": self.transform_to_Beijing_time(self.EnterTime_S,
                                                                      self.EnterTime_NS * 16),
                "EnterTime (s)": self.EnterTime_S,
                "EnterTime (ns)": self.EnterTime_NS * 16,
                "PeakCnt (Byte)": self.PeakCnt * 32,
                "PeakTime (ns)": self.PeakTime * 16,
                "ExitTime (Beijing)": self.transform_to_Beijing_time(self.ExitTime_S,
                                                                     self.ExitTime_NS * 16),
                "ExitTime (s)": self.ExitTime_S,
                "ExitTime (ns)": self.ExitTime_NS * 16,
                "ReachPeakInterval (ns)": ((self.PeakTime - self.EnterTime_NS) % 2 ** 32) *
                                          16,
                "MicroBurstInterval (ns)": ((self.ExitTime_NS - self.EnterTime_NS) % 2 ** 32)
                                           * 16,
                "RxPktCnt": self.RxPktCnt,
                "RxByteCnt": self.RxByteCnt,
                "DropPktCnt": self.DropPktCnt,
                "DropByteCnt": self.DropByteCnt,
                "MaxEnqueRate (Mbps)": (self.MaxEnqueRate & 0xffff) * 8,
                "MaxLatency (ns)": self.MaxLatency * 256}


def extract_pcap(from_filename, save_csv=False):
    ele_list = []
    with open(from_filename, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        # 遍历每个数据包
        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            if not isinstance(eth.data, dpkt.ip.IP):
                continue
            ip = eth.data
            if not isinstance(ip.data, dpkt.udp.UDP):
                continue
            udp = ip.data
            udp_payload = udp.pack()
            Type = int.from_bytes(udp_payload[10:11], 'big')
            meta_payload = buf[50:]
            mb_start = 0
            while mb_start < len(meta_payload) - 4:
                qe = QueueElement(Type, meta_payload[mb_start:mb_start + 64])
                ele_list.append(qe.get_dict())
                mb_start += 64

    if save_csv:
        df = pd.DataFrame(ele_list)
        file_name = from_filename.replace('source', 'result', 1).replace('.pcap', '.csv')
        df.to_csv(file_name, index=False)
if __name__ == '__main__':
    # extract_pcap("dataset_1GE.pcap", True)
    extract_pcap("case2_2GE.pcap", True)