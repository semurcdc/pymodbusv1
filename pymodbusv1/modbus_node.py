import rclpy
from rclpy.node import Node
from pymodbus.client import ModbusTcpClient

class ModbusNode(Node):
    def __init__(self):
        super().__init__('modbus_node')
        self.client = ModbusTcpClient("192.168.1.3")

    def read_registers(self, address, count):
        result = self.client.read_holding_registers(address, count)
        if result.isError():
            self.get_logger().error('Failed to read registers:')
            self.get_logger().error(result)
            return None
        return result.registers

def main(args=None):
    rclpy.init(args=args)
    node = ModbusNode()
    while rclpy.ok():
        registers = node.read_registers(0, 10)
        if registers is not None:
            node.get_logger().info('Read registers:')
            node.get_logger().info(str(registers))
        rclpy.spin_once(node, timeout_sec=0.5)

    node.client.close()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
