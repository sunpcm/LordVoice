import re
import whisper
from pydub import AudioSegment
import os
from dotenv import load_dotenv
load_dotenv()

# 配置
songjiang_speaker = os.getenv("SONGJIANG_SPEAKER")
input_log = os.getenv("DIARIZATION_LOG")
audio_file = os.getenv("ORIGINAL_VOCALS")
output_srt = os.getenv("OUTPUT_TEXT_SRT")

pattern = re.compile(r"开始: ([\d.]+)s \| 结束: ([\d.]+)s \| 说话人: (.+)")

# 加载音频和模型
audio = AudioSegment.from_wav(audio_file)
model = whisper.load_model(os.getenv("WHISPER_MODEL"))

with open(input_log, "r", encoding="utf-8") as fin, open(output_srt, "w", encoding="utf-8") as fout:
    idx = 1
    for line in fin:
        m = pattern.match(line.strip())
        if m:
            start, end, speaker = m.groups()
            if speaker == songjiang_speaker:
                start_ms = int(float(start) * 1000)
                end_ms = int(float(end) * 1000)
                segment = audio[start_ms:end_ms]
                segment.export("temp_songjiang.wav", format="wav")
                result = model.transcribe("temp_songjiang.wav", language="zh")
                text = result["text"].strip()
                def srt_time(seconds):
                    h = int(seconds // 3600)
                    m = int((seconds % 3600) // 60)
                    s = int(seconds % 60)
                    ms = int((seconds - int(seconds)) * 1000)
                    return f"{h:02}:{m:02}:{s:02},{ms:03}"
                fout.write(f"{idx}\n")
                fout.write(f"{srt_time(float(start))} --> {srt_time(float(end))}\n")
                fout.write(f"{text}\n\n")
                idx += 1
import os
os.remove("temp_songjiang.wav")
print(f"已生成宋江语音识别字幕: {output_srt}")
