// ===============================
// Q-TABLE (Paste your values here)
// ===============================

float Q[4][2] = {
  [[70.0151016  80.03927111]
 [69.99889728 47.21321076]
 [69.61854027 60.17672219]
 [70.12396428 41.07158188]]
};

#define RELAY_PIN  5   // Change if needed

// ===============================
// Choose Best Action
// ===============================
int choose_action(int state) {
  if (Q[state][0] > Q[state][1])
    return 0;   // BLOCK
  else
    return 1;   // ALLOW
}

// ===============================
// Simulated State (Temporary)
// ===============================
int get_current_state() {
  // For now we simulate state
  return random(0, 4);
}

void setup() {
  Serial.begin(115200);
  pinMode(RELAY_PIN, OUTPUT);
  randomSeed(analogRead(0));
}

void loop() {

  int state = get_current_state();
  int action = choose_action(state);

  Serial.print("State: ");
  Serial.print(state);

  if (action == 1) {
    Serial.println(" → ALLOW discharge");
    digitalWrite(RELAY_PIN, HIGH);
  }
  else {
    Serial.println(" → BLOCK discharge");
    digitalWrite(RELAY_PIN, LOW);
  }

  delay(2000);
}