import threading
import time
import serial
import pystray
import config
from PIL import Image, ImageDraw

# 전역 변수 초기화
icon: pystray.Icon | None = None # 아이콘 객체

# 배터리 잔량 이미지 생성
def create_battery_soc_image(soc: int | None) -> Image.Image:
    image = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    if soc is None:
        color_key = 'DISCONNECTED'
    elif soc <= config.BATTERY_SOC_THRESHOLD:
        color_key = 'LOW'
    else:
        color_key = 'NORMAL'
    color = config.BATTERY_SOC_COLORS[color_key]
    x1, y1, x2, y2 = 0, 96, 472, 416
    border_width, border_radius = 35, 50
    nub_height = 100
    nub_y1 = (y1 + y2 - nub_height) // 2
    draw.rounded_rectangle([x2, nub_y1, x2 + 40, nub_y1 + nub_height], radius=10, fill=color)
    draw.rounded_rectangle([x1, y1, x2, y2], radius=border_radius, outline=color, width=border_width)
    if soc:     
        margin = border_width + 40
        fill_width = int(((x2 - x1) - margin * 2) * (soc / 100))
        draw.rounded_rectangle(
            [x1 + margin, y1 + margin, x1 + margin + fill_width, y2 - margin],
            radius=max(0, border_radius - 20),
            fill=color,
        )
    return image

# 배터리 잔량 파싱
def parse_battery_soc(line: str) -> int | None:
    try:
        soc = int(line)
        return soc if 1 <= soc <= 100 else None
    except ValueError:
        return None

# 아이콘 업데이트
def update_icon(soc: int | None) -> None:
    icon.icon = create_battery_soc_image(soc)
    icon.title = f"배터리 상태: {soc}% 남음" if soc is not None else "배터리 상태: 연결 끊김"
    print(icon.title)

# 배터리 잔량 모니터링
def battery_soc_monitor() -> None:
    serial_port: serial.Serial | None = None
    while True:
        try:
            if serial_port is None or not serial_port.is_open:
                serial_port = serial.Serial(config.PORT, config.BAUD_RATE, timeout=1)
                print(f"시리얼 포트 연결: {config.PORT}")
                time.sleep(1)
            while line := serial_port.readline().decode("utf-8", errors="ignore").strip():
                soc = parse_battery_soc(line)
                if soc is not None:
                    update_icon(soc)
                    break
        except serial.SerialException as exception:
            print(exception)
            update_icon(None)
            if serial_port and serial_port.is_open:
                serial_port.close()
            serial_port = None
            time.sleep(1)
            continue
        time.sleep(config.BATTERY_CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    icon = pystray.Icon(
        "battery_soc_icon",
        create_battery_soc_image(None),
        title="배터리 상태: 알 수 없음"
    )
    threading.Thread(target=battery_soc_monitor, daemon=True).start()
    icon.run()