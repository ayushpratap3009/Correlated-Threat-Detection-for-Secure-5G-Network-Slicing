import random


class SliceTrafficGenerator:

    def __init__(self):

        self.slice_weights = {
            "embb": 0.60,
            "urllc": 0.25,
            "miot": 0.15
        }

    def choose_slice(self):

        r = random.random()

        if r < self.slice_weights["embb"]:
            return "embb"

        elif r < self.slice_weights["embb"] + self.slice_weights["urllc"]:
            return "urllc"

        else:
            return "miot"

    # ------------------------------------------------
    # Generate normal traffic with correct ML features
    # ------------------------------------------------
    def generate_normal_flow(self):

        slice_type = self.choose_slice()

        total_packets = random.randint(20, 200)
        total_bytes = random.randint(20000, 200000)
        duration = random.uniform(0.5, 5.0)

        packets_per_sec = total_packets / duration
        bytes_per_sec = total_bytes / duration

        avg_pkt = total_bytes / total_packets

        flow = {
            "slice_type": slice_type,
            "Total_Packets": total_packets,
            "Total_Bytes": total_bytes,
            "Flow_Duration": duration,
            "Packets_per_Second": packets_per_sec,
            "Bytes_per_Second": bytes_per_sec,
            "Average_Packet_Size": avg_pkt,
            "Min_Packet_Size": random.uniform(40, 200),
            "Max_Packet_Size": random.uniform(800, 1500),
            "Std_Packet_Size": random.uniform(10, 200),
            "IAT_Mean": random.uniform(0.001, 0.1),
            "IAT_Std": random.uniform(0.0001, 0.01)
        }

        return flow

    # ------------------------------------------------
    # Simulate attacks by amplifying features
    # ------------------------------------------------
    def amplify_attack(self, flow, attack_type):

        flow = flow.copy()

        if attack_type == "flood":

            flow["Total_Packets"] *= 5
            flow["Packets_per_Second"] *= 5
            flow["Bytes_per_Second"] *= 4

        elif attack_type == "dos":

            flow["Total_Packets"] *= 8
            flow["Packets_per_Second"] *= 8

        elif attack_type == "packet_spike":

            flow["Std_Packet_Size"] *= 3
            flow["IAT_Std"] *= 4

        return flow