import re
import whisper
from pydub import AudioSegment
import os
from dotenv import load_dotenv

load_dotenv()

# 配置 - 直接使用 FINAL_OUTPUT 音频文件生成字幕
final_audio_file = os.getenv("FINAL_OUTPUT")
output_srt = os.getenv("OUTPUT_TEXT_SRT")
whisper_model = os.getenv("WHISPER_MODEL")

print(f"正在为 '{final_audio_file}' 生成语音识别字幕...")

# 检查音频文件是否存在
if not os.path.exists(final_audio_file):
    print(f"错误: 音频文件 '{final_audio_file}' 不存在")
    print("请先运行 identify_and_export.py 生成音频合集")
    exit(1)

# 加载 Whisper 模型
print("正在加载 Whisper 模型...")
model = whisper.load_model(whisper_model)

# 直接对整个音频文件进行语音识别
print("正在进行语音识别...")
result = model.transcribe(final_audio_file, language="zh")

# 生成 SRT 字幕文件
def srt_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

with open(output_srt, "w", encoding="utf-8") as fout:
    for i, segment in enumerate(result["segments"], 1):
        start_time = segment["start"]
        end_time = segment["end"]
        text = segment["text"].strip()
        
        fout.write(f"{i}\n")
        fout.write(f"{srt_time(start_time)} --> {srt_time(end_time)}\n")
        fout.write(f"{text}\n\n")

print(f"已生成宋江语音识别字幕: {output_srt}")
print(f"共生成 {len(result['segments'])} 条字幕")
