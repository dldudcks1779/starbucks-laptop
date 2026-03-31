# 아두이노가 연결된 시리얼 포트
PORT = "COM5"

# 시리얼 통신 속도 (bps)
BAUD_RATE = 115200

# 배터리 잔량 임계값 (%)
BATTERY_SOC_THRESHOLD = 20

# 배터리 체크 주기 (초)
BATTERY_CHECK_INTERVAL_SECONDS = 5.0

# 배터리 상태별 표시 색상 (R, G, B, A)
BATTERY_SOC_COLORS = {
    'NORMAL':       (  0,   0,   0, 255),
    'LOW':          (232,  17,  35, 255),
    'DISCONNECTED': (160, 160, 160, 255),
}