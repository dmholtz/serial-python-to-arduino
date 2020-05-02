from serial_master import SerialCommunicator

class ApplicationTest:

    def __init__(self, int_rep, msg_length, batch_size):
        self.int_rep = int_rep
        self.msg_length = msg_length
        self.batch_size = batch_size

        # Hardware setup
        communicator = SerialCommunicator.autoconnect()
        communicator.client_setup(int_rep, msg_length, batch_size)

        # Send referencing command
        communicator.send(self.to_simple_command(1))
        # Send pos command
        communicator.send(self.to_command(2, 1500, 2300, 1400, 0, 800, 2000))
        communicator.send(self.to_command(2, 200, 200, 400, 0, 100, 0))
        # send end command
        communicator.send(self.to_simple_command(0))

    def to_simple_command(self, command):
        cmd = (command, list([0,0,0,0,0,0]))
        cmds = list()
        cmds.append(cmd)
        return cmds

    def to_command(self, command, p1, p2, p3, p4, p5, p6):
        cmd = (command, list([p1,p2,p3,p4,p5,p6,]))
        cmds = list()
        cmds.append(cmd)
        return cmds

test = ApplicationTest(2, 6, 1)