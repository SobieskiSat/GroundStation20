#include <Radiolot.h>

static SX1278_config radio_config =
{
  434000000,  //frequency in Hz, resolution: 61.035Hz
  SX1278_POWER_17DBM,
  SX1278_SF_7,
  SX1278_CR_4_5,
  SX1278_BW_125KHZ,
  SX1278_CRC_DIS,
  100 // rxTimeout = val * 1.024ms (for SF=7, BW=125K) [rxTimeout = val * (2^(SF) / BW)]
};

SX1278 radio;
uint8_t sendBuffer[SX1278_MAX_PACKET];

uint8_t counter = 0;
bool led_state = true;

String fragment;
String packet;
bool packeto;
char incoming;
float angleo;
uint8_t servo;
uint8_t motors;
uint8_t toSend[2];
String reco;

float pressure;
float temperature;
float latitude;
float longitude;
float yaw;
float pitch;
float roll;

void setup()
{
  //SerialUSBbegin(115200);
  SPI.begin();
  pinMode(LED_BUILTIN, OUTPUT);

  delay(1000);

  radio.config = radio_config;
  radio.useDio0IRQ = false;
  
  SX1278_init(&radio);
  packeto = false;
  angleo = 0;
  servo = 0;
  motors = 0;
}

void loop()
{ 
  SX1278_receive(&radio);  // transmit packet
  decodePacket();
  SerialUSB.println("p" + String(pressure, 2) + "Pt" + String(temperature, 1) + "Tx" + String(latitude, 7) + "Xy" + String(longitude, 7) + "Ya" + String(yaw, 1) + "Ab" + String(pitch, 1) + "Bc" + String(roll, 1) + "Cr" + String(radio.rssi) + "R");
//  //SerialUSBprintln(radio.rssi);
  SerialUSB.println(radio.rssi);
  digitalWrite(LED_BUILTIN, led_state);
  led_state = !led_state;

  if (radio.rxDone) // if receive successful
  {  
    if (radio.rxBuffer[radio.rxLen - 1] == (uint8_t)5)
    {
      getPacket();

      fragment = cutFragment('s', 'S');
      if (fragment != "bad") servo = (uint8_t)fragment.toInt();
      //SerialUSBprintln("Servo: " + String(servo));
      fragment = cutFragment('m', 'M');
      if (fragment != "bad") motors = (uint8_t)fragment.toInt() * 2;
      //SerialUSBprintln("Motors: " + String(servo));
      fragment = cutFragment('a', 'A');
      if (fragment != "bad") angleo = fragment.toFloat();
      //SerialUSBprintln("Angle: " + String(servo));
      
      toSend[0] = motors + servo;
      toSend[1] = (uint8_t)(angleo * (255.0 / 360.0));
      delay(10);
      SX1278_transmit(&radio, toSend, 2);
      //SX1278_transmit(&radio, (uint8_t*)"Duplex!", 7);
    }
    
    radio.rxDone = false;
    
    ////SerialUSBprintln("[LoRa] Packet received, " + (String)bitrate + "b/s, " + (String)packrate + "P/s");
    ////SerialUSBprintln(String((int)radio.rxBuffer[radio.rxLen - 1]));
  }
}

void getPacket()
{
  while (SerialUSB.available() > 0)
  {
    incoming = SerialUSB.read();
    if (packeto)
    {
      packet += incoming;
    }
    
    if (incoming == '<')
    {
      packeto = true;
      packet = "";
      packet += incoming;
    }
    else if (incoming == '>') packeto = false;
  }
}


String cutFragment(char openChar, char closeChar)
{
  if (packet.indexOf('<') >= 0 && packet.indexOf('>') >= 0)
  {
    if (packet.indexOf(openChar) >= 0 && packet.indexOf(closeChar) >= 0)
    {
       return (packet.substring(packet.indexOf(openChar) + 1, packet.indexOf(closeChar)));
    }
  }
  return "bad";
}

static void decodePacket()
{
  pressure = (float)(radio.rxBuffer[0] + (radio.rxBuffer[1] << 8) + (radio.rxBuffer[2] << 16) + (radio.rxBuffer[3] << 24)) / 1000.0;
  temperature = (float)(radio.rxBuffer[4] + (radio.rxBuffer[5] << 8) + (radio.rxBuffer[6] << 16) + (radio.rxBuffer[7] << 24)) / 10.0;
  latitude = (float)(radio.rxBuffer[8] + (radio.rxBuffer[9] << 8) + (radio.rxBuffer[10] << 16) + (radio.rxBuffer[11] << 24)) / 10000000.0;
  longitude = (float)(radio.rxBuffer[12] + (radio.rxBuffer[13] << 8) + (radio.rxBuffer[14] << 16) + (radio.rxBuffer[15] << 24)) / 10000000.0; 
  yaw = (float)(radio.rxBuffer[16]) * (360.0 / 255.0);
  pitch = (float)(radio.rxBuffer[17]) * (360.0 / 255.0);
  roll = (float)(radio.rxBuffer[18]) * (360.0 / 255.0);
}
