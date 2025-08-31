import torch
from pyannote.audio import Pipeline
import os
from dotenv import load_dotenv
load_dotenv()

# --- 配置 ---
HF_TOKEN = os.getenv("HF_TOKEN")
INPUT_AUDIO = os.getenv("INPUT_AUDIO")
OUTPUT_LOG = os.getenv("OUTPUT_LOG")

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
with open(OUTPUT_LOG, "w", encoding="utf-8") as log_file:
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        log_line = f"开始: {turn.start:.2f}s | 结束: {turn.end:.2f}s | 说话人: {speaker}\n"
        print(log_line, end="")
        log_file.write(log_line)

print(f"\n说话人日志已保存到 '{OUTPUT_LOG}'。")

