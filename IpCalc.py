#/usr/bin/python3
class IpCalc:
    def __init__(self, ipAddr="192.168.1.1", mask="255.255.255.0"):
        self.ip = ipAddr
        self.mask = mask

    def broadcast(self):
        result = self.mask.split('.')
        ip_res = self.ip.split('.')
        for i in range(len(result)):
             if int(result[i]) < 255:
                 if int(result[i]) != 0:
                     bits="{0:08b}".format(int(result[i]))
                     ip_bits="{0:08b}".format(int(ip_res[i]))
                     bits = list(bits)
                     ip_bits = list(ip_bits)
                     for j in range(len(bits)):
                        if int(bits[j]) == 0:
                              ip_bits[j] = '1'            
                     ip_res[i] = str(int(''.join(ip_bits),2))
                 else:
                     ip_res[i] = '255'
        return ip_res

    def maxAddr(self):
        out_data = self.broadcast()
        out_data = out_data[::-1]
        for i in range(len(out_data)):
            if int(out_data[i]) == 255:
                out_data[i] = (255-1)
                break
        return out_data[::-1]

    def network(self):
        result = self.mask.split('.')
        ip_res = self.ip.split('.')
        for i in range(len(result)):
            if int(result[i]) < 255:
                 if int(result[i]) != 0:
                     bits="{0:08b}".format(int(result[i]))
                     ip_bits="{0:08b}".format(int(ip_res[i]))
                     bits = list(bits)
                     ip_bits = list(ip_bits)
                     for j in range(len(bits)):
                        if int(bits[j]) == 0:
                              ip_bits[j] = '0'            
                     ip_res[i] = str(int(''.join(ip_bits),2))
                 else:
                     ip_res[i] = '0'       
        return ip_res

    def minAddr(self):
        out_data = self.network()
        out_data = out_data[::-1]
        for i in range(len(out_data)):
            if int(out_data[i]) == 0:
                out_data[i] = str(int(out_data[i]) + 1)
                break
        return out_data[::-1]
    
    def wildcard(self):
        list_octet = self.mask.split('.')
        data = []
        res = ""
        for octet in list_octet:
            list_bits = "{:08b}".format(int(octet))
            result = list(list_bits)
            for i in range(len(result)):
                if int(result[i]) == 0:
                    result[i] = '1'
                elif int(result[i]) == 1:
                    result[i] = '0'
            data.append(result)
        for bits in data:
            res += str(int("".join(bits),2))
            res += '.'
        return res[:-1]