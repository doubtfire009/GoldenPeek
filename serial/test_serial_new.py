import serial

class Ser(object):
    def __init__(self):
        # 打开端口
        self.port = serial.Serial(port='COM4', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=2)

    # 发送指令的完整流程
    def send_cmd(self, cmd):
        print(cmd)
        self.port.write(cmd)
        response = self.port.readall()
        print(response)
        response = self.convert_hex(response)
        return response

    # 转成16进制的函数
    def convert_hex(self, string):
        res = []
        result = []
        for item in string:
            res.append(item)
        for i in res:
            result.append(hex(i))
        return result

# cmd = [0x03]
# Ser.send_cmd()
if __name__ == '__main__':
    if __name__ == '__main__':
        stdroom = Ser()
        cmd = [0x01,0x06,0x00,0xc8, 0x00, 0x02,0xf5,0x89]
        r = stdroom.send_cmd(cmd)
        print(r)
