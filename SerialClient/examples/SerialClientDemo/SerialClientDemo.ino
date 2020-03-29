#include <SerialClient.h>

void setup() {
  // put your setup code here, to run once:
  SerialClient sc = {};
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);

  sc.protocolSetup();


  int batch = sc.getBatchSize();
  int messageLength = sc.getMessageLength();

  // Create pointers for variable-size arrays
  byte* operations = 0;
  int* data = 0;

  // If pointer is not 0, delete whatever it points to
  // Then, let the pointer point on a new array
  if (operations != 0)
  {
    delete [] operations;
  }
  operations = new byte[batch];
  if (data != 0)
  {
    delete [] data;
  }
  data = new int[batch * messageLength];

  // receiving the first batch
  sc.receive2ByteInts(operations, data);

  for (int i = 0; i < 50; i ++)
  {
    // If pointer is not 0, delete whatever it points to
    // Then, let the pointer point on a new array
    if (operations != 0)
    {
      delete [] operations;
    }
    operations = new byte[batch];
    if (data != 0)
    {
      delete [] data;
    }
    data = new int[batch * messageLength];

    // receiving the first batch
    sc.receive2ByteInts(operations, data);
  }

  //  for (int i = 0; i < data[119]; i ++)
  //  {
  //    digitalWrite(13, HIGH);
  //    delay(200);
  //    digitalWrite(13, LOW);
  //    delay(200);
  //  }


}

void loop() {
  // put your main code here, to run repeatedly:

}
