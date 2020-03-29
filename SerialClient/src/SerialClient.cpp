/*
	SerialClient.cpp - Library for fast serial communication between Arduino and
    PC. Implements a master - client protocol, which speeds up the transfer of
    numeric data or G-Codes

	(C) 2020 by David Holtz <https://github.com/dmholtz>
*/

#include "Arduino.h"
#include "SerialClient.h"

/**
 * 
 **/
SerialClient::SerialClient()
{
    Serial.begin(115200);
}

/**Awaits four incoming bytes to define the protocol.
 * 1. byte: must be SETUP_INIT_BYTE
 * 2. byte: integer representation: 1, 2 or 4
 * 3. byte: message length: positive integer > 0
 * 4. byte: batch size: positive integer > 0
 * 
 * @returns false if any of these rules is infringed
 * @returns true if all conditions are fulfilled
 * 
 **/
bool SerialClient::protocolSetup()
{
    // Await the setup initialization byte
    while (Serial.available() < 1)
    {
    }
    if (Serial.read() != SETUP_INIT_BYTE)
    {
        return false;
    }
    // Await Integer representation byte
    while (Serial.available() < 1)
    {
    }
    int intRep = Serial.read();
    if (intRep == 2 || intRep == 1 || intRep == 4)
    {
        intRepresentation = intRep;
    }
    else
    {
        return false;
    }
    // Await message length byte
    while (Serial.available() < 1)
    {
    }
    int msgLen = Serial.read();
    if (msgLen >= 1)
    {
        messageLength = msgLen;
    }
    else
    {
        return false;
    }
    // Await batch size byte
    while (Serial.available() < 1)
    {
    }
    int batch = Serial.read();
    if (batch >= 1)
    {
        batchSize = batch;
    }
    else
    {
        return false;
    }
    Serial.println();
    return true;
}

bool SerialClient::receive2ByteInts(byte* commands_ref, int16_t* params)
{
    awaitIncomingByte();
    if (Serial.peek() == SETUP_INIT_BYTE)
    {
        protocolSetup();
        return false;
    }
    else
    {
        for (int i = 0; i < batchSize; i++)
        {
            awaitIncomingByte();
            commands_ref[i] = Serial.read();
            for (int j = 0; j < messageLength; j++)
            {
                int param = 0;
                for (int count = 0; count < intRepresentation; count++)
                {
                    awaitIncomingByte();
                    param += (byte)Serial.read();
                    if (count < intRepresentation - 1)
                    {
                        param = param << 8;
                    }
                }
                params[i * messageLength + j] = param;
            }
        }
        Serial.println();
    }
    return true;
}

void SerialClient::awaitIncomingByte()
{
    while (Serial.available() < 1)
    {
    }
}

uint8_t SerialClient::getBatchSize()
{
    return batchSize;
}

uint8_t SerialClient::getMessageLength()
{
    return messageLength;
}

uint8_t SerialClient::getIntRepresentation()
{
    return intRepresentation;
}
