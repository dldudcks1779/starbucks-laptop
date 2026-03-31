// 배터리 잔량 측정 라이브러리
// - MAX17043: I2C 통신을 통해 배터리 잔량 정보 제공
#include "DFRobot_MAX17043.h"

// 배터리 모니터링 객체 생성
DFRobot_MAX17043 battery;

void setup() {
  // 시리얼 통신 초기화 (Baud Rate: 115200)
  Serial.begin(115200);

  // I2C 통신을 통한 센서 초기화 및 연결 확인
  while(battery.begin() != 0){
    delay(1000);
  }
}

void loop() {
  // 배터리 잔량(SoC: State of Charge) 측정 및 출력
  int percentage = battery.readPercentage();
  Serial.println(percentage);

  // 1초 대기
  delay(1000);
}