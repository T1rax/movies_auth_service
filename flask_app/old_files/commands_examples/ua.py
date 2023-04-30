from device_detector import DeviceDetector

# phone
ua = "Mozilla/5.0 (Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36"

device = DeviceDetector(ua, skip_bot_detection=True).parse()

print(device.device_type())
print(device.engine())
# smartphone

# web
ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"

device = DeviceDetector(ua, skip_bot_detection=True, skip_device_detection=True).parse()

print(device.device_type())
print(device.engine())
# desktop


# tv
ua = "AppleTV/tvOS/9.1.1"

device = DeviceDetector(ua, skip_bot_detection=True).parse()

print(device.device_type())
print(device.engine())
# tv
