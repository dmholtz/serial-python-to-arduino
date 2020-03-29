# serial-python-to-arduino
Accelerates serial communication between PC with python setup and an Arduino board. Useful to quickly transfer numeric data or G-Code.

# Idea


# Protocol

## Client setup
Client setup is an initialization routine, which lets the master define the communication protocol for his client. This setup consists of four bytes:
* Client-setup-Init-Byte: 0xFF
* Integer-representation-byte: 0x01 / 0x02 / 0x04
* Byte-count-Byte: 0x04 - ...
* Batch-size-byte: 0x01 - ...

### Client setup-Init-Byte
If 0xFF is the first byte to be sent in a batch, a client setup routine is triggerd.

### Integer-representation-Byte
Defines, how many bytes are used to define an integer. Examples:
* 0x01: one byte integer (-128, 127) (Arduino byte, Java byte)
* 0x02: two byte integer (-32768, 32767) (Arduino int, Java short)
* 0x04: four byte integer (-2^31-1, 2^31) (Arduino long, Java int)

### Bytes per command - byte
Defines, how many bytes are sent per batch. Every batch has to be of the following structure:
* command byte (1 byte)
* data bytes (n * Integer-representation-Byte): where n is the number of Integer values that are sent (message length)
Consequently, the Byte-count-Byte is the sum of all bytes: byte-count-byte = 1 + n * integer-representation-byte

### Batch-size-Byte
Defines how many (commands + data) tuples are combined into one batch. Sending batches of data signifantly increases the performance. Keep in mind that the Arduino has a limited buffer and batch sizes must not exceed the dynamic storage.

## Data transfer


