import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

# 从环境变量读取配置
VIDEO_FILE = os.getenv("VIDEO_FILE", "demo.mp4")  # 可修改为你的文件名
AUDIO_FILE = os.getenv("INPUT_AUDIO", "demo_audio.wav")

if not os.path.exists(VIDEO_FILE):
    print(f"错误: 未找到视频文件 '{VIDEO_FILE}'")
    print(f"请确保视频文件存在，或在 .env 中设置正确的 VIDEO_FILE 路径")
    exit(1)

print(f"正在从 {VIDEO_FILE} 提取音频到 {AUDIO_FILE} ...")

# 使用 ffmpeg 提取音频
cmd = [
    "ffmpeg", "-i", VIDEO_FILE, 
    "-vn",  # 不包含视频
    "-acodec", "pcm_s16le",  # 音频编码格式
    "-ar", "16000",  # 采样率 16kHz
    "-ac", "1",  # 单声道
    "-y",  # 覆盖输出文件
    AUDIO_FILE
]

try:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    print(f"音频提取成功: {AUDIO_FILE}")
except subprocess.CalledProcessError as e:
    print(f"音频提取失败: {e}")
    print("请确保已安装 ffmpeg 并在 PATH 中")
    exit(1)
except FileNotFoundError:
    print("错误: 未找到 ffmpeg")
    print("请安装 ffmpeg: ")
    print("  Ubuntu/Debian: sudo apt install ffmpeg")
    print("  macOS: brew install ffmpeg")
    print("  Windows: 下载并配置 PATH")
    exit(1)
