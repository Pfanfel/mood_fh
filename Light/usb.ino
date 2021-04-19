// USB - USB.ino
//
// Description:
// Executes commands retrieved from serial (USB) port.
//
// Created by John Woolsey on 12/17/2019.
// Copyright (c) 2019 Woolsey Workshop.  All rights reserved.
/*void setup() {
   Serial.begin(9600);  // start serial communication at 9600 baud
}
void loop() {
   // Read and execute commands from serial port
   if (Serial.available()) {  // check for incoming serial data
      String command = Serial.readString();  // read command from serial port
      if (command == "led_on") {  // turn on LED
         printf("Hallo\n");
         digitalWrite(LED_BUILTIN, HIGH);
      } else if (command == "led_off") {  // turn off LED
         digitalWrite(LED_BUILTIN, LOW);
      } else if (command == "read_a0") {  // read and send A0 analog value
         Serial.println(analogRead(A0));
      }
   }
}*/
//String data="Hello From Arduino!";

void setup() {
// put your setup code here, to run once:
Serial.begin(9600);

}

void loop() {
// put your main
//code here, to run repeatedly:
int r = 1;
//Serial.print(r);//data that is being Sent
int temp = Serial.read() - '0';
printf("%d", temp);
//if (temp == 5) {
  //Serial.println(Serial.read());
//}
delay(200);
}
