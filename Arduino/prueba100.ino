////////////////////////////////////////////////////////////////////////
/// @param[in] IRSensorPin Analog pin on which IR detector is connected
/// @param[in] delay (msec) delay between calls to this method. It is
///                  best to call it at least 5 times per beat, aka
///                  no slower than 150msec for 70bpm. An ideal value
///                  is 60ms or faster to handle up to 200 BPM.
///
/// @brief
/// True if heartbeat is detected on the sensor.
/// This code is trivial and just does a peak detection, instead of
/// trying to detect the heart's pulse waveform.
/// Note: I am fudging sensor data with the delay to make the integer
/// math after that uses constants, somewhat independant of the sleep
/// delay used in the main loop. Otherwise if maxValue decays too slow
/// or too fast, it causes glitches and false beat detection.
////////////////////////////////////////////////////////////////////////
//#define HBDEBUG(i) i
#define HBDEBUG(i)

bool heartbeatDetected(int IRSensorPin, int delay)
{
  static int maxValue = 0;
  static bool isPeak = false;
  int rawValue;
  bool result = false;
    
  rawValue = analogRead(IRSensorPin);
  // Separated because analogRead() may not return an int
  rawValue *= (1000/delay);
  HBDEBUG(Serial.print(isPeak); Serial.print("p, "));
  HBDEBUG(Serial.print(rawValue); Serial.print("r, "));
  HBDEBUG(Serial.print(maxValue); Serial.print("m, "));

  // If sensor shifts, then max is out of whack.
  // Just reset max to a new baseline.
  if (rawValue * 4L < maxValue) {
    maxValue = rawValue * 0.8;
    HBDEBUG(Serial.print("RESET, "));
  }
  
  // Detect new peak
  if (rawValue > maxValue - (1000/delay)) {
    // Only change peak if we find a higher one.
    if (rawValue > maxValue) {
      maxValue = rawValue;
    }
    // Only return true once per peak.
    if (isPeak == false) {
      result = true;
      HBDEBUG(Serial.print(result); Serial.print(",  *"));
    }
    isPeak = true;
  } else if (rawValue < maxValue - (3000/delay)) {
    isPeak = false;
    // Decay max value to adjust to sensor shifting
    // Note that it may take a few seconds to re-detect
    // the signal when sensor is pushed on meatier part
    // of the finger. Another way would be to track how
    // long since last beat, and if over 1sec, reset
    // maxValue, or to use derivatives to remove DC bias.
    maxValue-=(1000/delay);
 }
  HBDEBUG(Serial.print("\n"));
  return result;
}


////////////////////////////////////////////////////////////////////////
// Arduino main code
////////////////////////////////////////////////////////////////////////
int ledPin=8;
int analogPin=0;
//Include libraries
#include <OneWire.h>
#include <DallasTemperature.h>

// Data wire is plugged into pin 2 on the Arduino
#define ONE_WIRE_BUS 2
// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);
// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);
void setup()
{
  Serial.begin(9600); //Begin serial communication
   sensors.begin();
  // Built-in arduino board pin for the display LED
  pinMode(ledPin,OUTPUT);
  
  // Init serial console
  Serial.begin(9600);
  //Serial.println("Heartbeat detection sample code.");
}

const int delayMsec = 60; // 100msec per sample

// The main loop blips the LED and computes BPMs on serial port.
void loop()
{ 
  static int beatMsec = 0;
  int heartRateBPM = 0;
   if (heartbeatDetected(analogPin, delayMsec)) {
    heartRateBPM = 60000 / beatMsec;
    digitalWrite(ledPin,1);
    

    // Print msec/beat and instantaneous heart rate in BPM
    Serial.println(heartRateBPM);
    // Send the command to get temperatures
  
    beatMsec = 0;
    sensors.requestTemperatures();  
  //Serial.print("Temperature is: ");
  Serial.println(sensors.getTempCByIndex(0)); // Why "byIndex"? You can have more than one IC on the same bus. 0 refers to the first IC on the wire
  //This section prints firstly the HB and then the temperature, temperature will only be requested and printed while a HB is detected.
  //If you would like to print the temperature firstly just cut and paste the lines before the HB's lines
  } else {
    digitalWrite(ledPin,0);
    
  // Send the command to get temperatures
  
  }
  
  // Note: I assume the sleep delay is way longer than the
  // number of cycles used to run the code hence the error
  // is negligible for math.
  delay(delayMsec);
  beatMsec += delayMsec;
}
