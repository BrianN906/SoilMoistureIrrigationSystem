const int RED_PIN = 9;
const int GREEN_PIN = 10;
const int WHITE_PIN = 8;
const int BUTTON_PIN = 7;
const int SENSOR_PIN = A0;
const int RELAY_PIN = 12;

const int DRY_VALUE = 514;   // raw reading in completely dry soil
const int WET_VALUE = 230;   // raw reading in completely wet soil

const long PUMP_TIME = 2000;  // seconds in milliseconds
const long WAIT_TIME = 10000; //seconds in milliseconds

void setup() {
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(WHITE_PIN, OUTPUT);
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Serial.begin(9600);
  digitalWrite(RELAY_PIN, HIGH);
  setLEDs(LOW, LOW, HIGH);  // green on startup
}

void loop() {
  // button
  if (digitalRead(BUTTON_PIN) == LOW) {
    delay(50);
    if (digitalRead(BUTTON_PIN) == LOW) {
      setLEDs(HIGH, LOW, LOW);  // white 
      digitalWrite(RELAY_PIN, LOW);
      delay(PUMP_TIME);
      digitalWrite(RELAY_PIN, HIGH);
      delay(WAIT_TIME);             // wait for water to absorb
      sendReading("MANUAL");
      setLEDs(LOW, LOW, HIGH);  // green 
      while (digitalRead(BUTTON_PIN) == LOW);
      delay(500);
    }
  }

  // listen for commands from Python
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "READ") {
      sendReading("READ");

    } else if (cmd == "PUMP") {
      setLEDs(LOW, HIGH, LOW);  // red 
      digitalWrite(RELAY_PIN, LOW);
      delay(PUMP_TIME);
      digitalWrite(RELAY_PIN, HIGH);
      delay(10000);             // wait
      sendReading("PUMP");
      setLEDs(LOW, LOW, HIGH);  // green
    }
  }
}

void sendReading(String type) {
  int raw = analogRead(SENSOR_PIN);
  int moisture = map(raw, DRY_VALUE, WET_VALUE, 0, 100);
  moisture = constrain(moisture, 0, 100);
  Serial.print(type);
  Serial.print(",");
  Serial.print(raw);
  Serial.print(",");
  Serial.println(moisture);
}

void setLEDs(int w, int r, int g) {
  digitalWrite(WHITE_PIN, w);
  digitalWrite(RED_PIN, r);
  digitalWrite(GREEN_PIN, g);
}
