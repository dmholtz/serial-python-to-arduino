/*
	SerialClient.h - Library for fast serial communication between Arduino and
    PC. Implements a master - client protocol, which speeds up the transfer of
    numeric data or G-Codes

	(C) 2020 by David Holtz <https://github.com/dmholtz>
*/

#ifndef SerialClient_h
#define SerialClient_h

#define SETUP_INIT_BYTE 0xFF

#include "Arduino.h"

class SerialClient
{
  public:
	SerialClient();

    // setup, receive, send operations
    bool protocolSetup();
    //bool receive1ByteInts(byte & commands_ref, int8_t & params);
    bool receive2ByteInts(byte* commands_ref, int16_t* params);
    void send();

    // Queries
    uint8_t getIntRepresentation();
    uint8_t getBatchSize();
    uint8_t getMessageLength();

    boolean protocolDefined();

  private:
    // Initialize to invalid default values => protocolDefine() == false
    void awaitIncomingByte();

    uint8_t intRepresentation = 0;
    uint8_t messageLength = 0;
    uint8_t batchSize = 0;
	
};

#endif


