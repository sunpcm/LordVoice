import os
from dotenv import load_dotenv
load_dotenv()
from pydub import AudioSegment

INPUT_AUDIO = os.getenv("INPUT_AUDIO")
LORD_SAMPLE = os.getenv("LORD_SAMPLE")

print(f"正在从 {INPUT_AUDIO} 提取前20秒作为样本到 {LORD_SAMPLE} ...")

audio = AudioSegment.from_wav(INPUT_AUDIO)
first_20s = audio[:20 * 1000]  # 前20秒
first_20s.export(LORD_SAMPLE, format="wav")
print(f"已保存为 {LORD_SAMPLE}")