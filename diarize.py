import torch
from pyannote.audio import Pipeline
import os

# --- 配置 ---
# 1. 替换成你自己的 Hugging Face 访问令牌
HF_TOKEN = "YOUR_HUGGING_FACE_TOKEN"
# 2. 指定上一步分离出的人声音频文件
INPUT_AUDIO = "separated/htdemucs/vocals.wav"
# 3. 指定输出的说话人日志文件名
OUTPUT_LOG = "diarization_log.txt"

# 检查文件是否存在
if not os.path.exists(INPUT_AUDIO):
    print(f"错误: 输入文件 '{INPUT_AUDIO}' 未找到。")
    print("请先运行第一步和第二步。")
    exit()

print("正在加载说话人日志模型...")
# 使用你的令牌加载模型
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token=HF_TOKEN
)

# 如果有GPU，将模型移至GPU以加速
if torch.cuda.is_available():
    print("检测到GPU，将使用GPU进行处理。")
    pipeline.to(torch.device("cuda"))
else:
    print("未检测到GPU，将使用CPU进行处理（可能较慢）。")

print(f"正在处理音频文件: {INPUT_AUDIO}...")
# 运行说话人日志流程
diarization = pipeline(INPUT_AUDIO)

print("处理完成！正在将结果写入日志文件...")
# 将结果写入文本文件，方便查看
with open(OUTPUT_LOG, "w") as log_file:
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        # turn.start 和 turn.end 是说话的开始和结束时间（秒）
        log_line = f"开始: {turn.start:.2f}s | 结束: {turn.end:.2f}s | 说话人: {speaker}\n"
        print(log_line, end="")
        log_file.write(log_line)

print(f"\n说话人日志已保存到 '{OUTPUT_LOG}'。")
