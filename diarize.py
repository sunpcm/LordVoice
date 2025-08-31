import torch
from pyannote.audio import Pipeline
import os
from dotenv import load_dotenv
load_dotenv()


# --- 配置 ---
HF_TOKEN = os.getenv("HF_TOKEN")
INPUT_AUDIO = os.getenv("INPUT_AUDIO")
OUTPUT_LOG = os.getenv("DIARIZATION_LOG")
MERGE_GAP = float(os.getenv("MERGE_GAP", "1.0"))
MERGE_INSERT_SILENCE = float(os.getenv("MERGE_INSERT_SILENCE", "1.0"))

if not os.path.exists(INPUT_AUDIO):
    print(f"错误: 输入文件 '{INPUT_AUDIO}' 未找到。\n请先运行音频提取和人声分离步骤。")
    exit(1)

print("正在加载说话人日志模型...")
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token=HF_TOKEN
)
if pipeline is None:
    print("模型加载失败，请检查 Hugging Face Token 和模型权限。")
    exit(1)

if torch.cuda.is_available():
    print("检测到GPU，将使用GPU进行处理。")
    pipeline.to(torch.device("cuda"))
else:
    print("未检测到GPU，将使用CPU进行处理（可能较慢）。")

print(f"正在处理音频文件: {INPUT_AUDIO} ...")
diarization = pipeline(INPUT_AUDIO)

print("处理完成！正在将结果写入日志文件...")

# 合并同一说话人片段，合并后片段之间保持至少 MERGE_GAP 秒间隔

merged_segments = []
last = None
for turn, _, speaker in diarization.itertracks(yield_label=True):
    if last is None:
        last = [turn.start, turn.end, speaker]
    else:
        if speaker == last[2] and turn.start - last[1] < MERGE_GAP:
            last[1] = turn.end
        else:
            merged_segments.append(tuple(last))
            last = [turn.start, turn.end, speaker]
if last:
    merged_segments.append(tuple(last))

with open(OUTPUT_LOG, "w", encoding="utf-8") as log_file:
    for i, seg in enumerate(merged_segments):
        duration = seg[1] - seg[0]
        log_line = f"开始: {seg[0]:.2f}s | 结束: {seg[1]:.2f}s | 时长: {duration:.2f}s | 说话人: {seg[2]}\n"
        print(log_line, end="")
        log_file.write(log_line)
        # 如果不是最后一个片段，插入静音间隔信息
        if i < len(merged_segments) - 1:
            silence_start = seg[1]
            silence_end = seg[1] + MERGE_INSERT_SILENCE
            silence_line = f"开始: {silence_start:.2f}s | 结束: {silence_end:.2f}s | 说话人: SILENCE\n"
            print(silence_line, end="")
            log_file.write(silence_line)

print(f"\n说话人日志已保存到 '{OUTPUT_LOG}'。")

