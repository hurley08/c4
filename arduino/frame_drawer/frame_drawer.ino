#include "Arduino_LED_Matrix.h"
ArduinoLEDMatrix matrix;
void setup() {
  Serial.begin(9600);
  Serial.println("Penis");
  matrix.begin();
  // put your setup code here, to run once:
  uint8_t frame[8][12] = {
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }
};
frame[1][2] = 1;
matrix.renderBitmap(frame, 8, 12);

}
const int MAX_ROW = 20; // Adjust the maximum row and col based on your requirements
const int MAX_COL = 20;
byte frame[MAX_ROW][MAX_COL];


void accept_then_print(int row, int col, String message){

  memset(frame, 0, sizeof(frame));

  int messageIndex = 0;
  for (int i = 0; i < MAX_ROW; i++) {
    for (int j = 0; j < MAX_COL; j++) {
      if (messageIndex < message.length()) {
        frame[i][j] = message.charAt(messageIndex);
        messageIndex++;
      }
    }
  }

  frame[2][1] = 1;
  matrix.renderBitmap(frame,row,col);
}

void process_line(char* line, int& row, int& col, String& str) {
  char* token = strtok(const_cast<char*>(line), "-");
  if (token != NULL){
  row = atoi(token);
  }

  token = strtok(NULL, "-");
  if (token != NULL){
    row = atoi(token);
  }

  token = strtok(NULL, "-");
  if (token != NULL){
    col = atoi(token);
  }

 token = strtok(NULL, "-");
 while (token != NULL){
  str += token;
  token = strtok(NULL, "-");
  if (token != NULL){
    str += " ";
    }
 }
 Serial.println(row);
 Serial.println(col);
 Serial.println(str);
}

void clear_matrix(int row, int col){
  uint8_t frame[row][col] = {
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }
};
frame[1][2] = 1;
matrix.renderBitmap(frame, row, col);
}

void loop() {

   if (Serial.available() > 0) {
    // Read a line from the Serial input
    String inputLine = Serial.readStringUntil('\n');

    // Check if the command is the one you expect
    if (inputLine.charAt(0) == 'A') {
      Serial.println("Reading Line");
      int row, col;
      String str;

      // Create a non-const copy of the C-style string
      char inputLineCopy[inputLine.length() + 1];

      inputLine.toCharArray(inputLineCopy, sizeof(inputLineCopy));

      // Pass the non-const copy to the process_line function
      process_line(inputLineCopy, row, col, str);

      //clear_matrix(row, col);
        uint8_t frame[8][12] = {
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
  { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }
};
frame[1][2] = 1;
matrix.renderBitmap(frame, 8, 12);

      delay(2);
      accept_then_print(row, col, str);
      delay(2);
    }
  }
}
