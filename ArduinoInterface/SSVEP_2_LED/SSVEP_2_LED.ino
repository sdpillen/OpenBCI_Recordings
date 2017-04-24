
int LED3 = 1;

// 500 = 1 Hz for testing
const unsigned long LED3_interval = 250; // Toggle every X milliseconds; Interval ON (and subsequently off) in ms.  For example setting to 500 will cause the light to blink at 1 Hz.

unsigned long LED3_time;
unsigned char LED3_on;

void setup () {
  pinMode (LED3, OUTPUT);
  LED3_time = millis ();
  LED3_on = 0;
}

void toggle_LED3 () {
   if (LED3_on == 0) {
      digitalWrite (LED3, LOW);
      LED3_on = 1;
   }
   else {
      digitalWrite (LED3, LOW);
      LED3_on = 0;
   }
  LED3_time = millis ();  
}

void loop ()
  {
    if ((millis () - LED3_time) >= LED3_interval) {
      toggle_LED3 ();
    }
}
