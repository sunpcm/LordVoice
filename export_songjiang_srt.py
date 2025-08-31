import re

def seconds_to_srt_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

# 识别结果
songjiang_speaker = "SPEAKER_04"  # 可根据实际识别结果修改
input_log = "diarization_log.txt"
output_srt = "songjiang_voice_compilation.srt"

pattern = re.compile(r"开始: ([\d.]+)s \| 结束: ([\d.]+)s \| 说话人: (.+)")

with open(input_log, "r", encoding="utf-8") as fin, open(output_srt, "w", encoding="utf-8") as fout:
    idx = 1
    for line in fin:
        m = pattern.match(line.strip())
        if m:
            start, end, speaker = m.groups()
            if speaker == songjiang_speaker:
                fout.write(f"{idx}\n")
                fout.write(f"{seconds_to_srt_time(float(start))} --> {seconds_to_srt_time(float(end))}\n")
                fout.write(f"{speaker}\n\n")
                idx += 1
print(f"已生成宋江片段字幕: {output_srt}")
