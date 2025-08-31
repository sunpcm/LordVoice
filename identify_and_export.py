import os
import torch
import torchaudio
from speechbrain.inference import SpeakerRecognition
from pydub import AudioSegment
from dotenv import load_dotenv
load_dotenv()

# --- 配置 ---
DIARIZATION_LOG = os.getenv("DIARIZATION_LOG")
ORIGINAL_VOCALS = os.getenv("INPUT_AUDIO")
SONGJIANG_SAMPLE = os.getenv("SONGJIANG_SAMPLE")
OUTPUT_DIR = os.getenv("OUTPUT_DIR")
FINAL_OUTPUT = os.getenv("FINAL_OUTPUT")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print("正在加载声纹识别模型...")
verification = SpeakerRecognition.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir=os.getenv("PRETRAINED_MODEL_DIR")
)

def get_embedding(audio_file):
    signal, fs = torchaudio.load(audio_file)
    # 跳过过短片段（小于1秒）
    if signal.shape[1] < fs:  # fs为采样率，1秒音频帧数
        print(f"警告: {audio_file} 片段过短，已跳过。")
        return None
    emb = verification.encode_batch(signal)
    return emb.squeeze(0)

def cosine_similarity(emb1, emb2):
    # 返回均值作为标量
    return torch.nn.functional.cosine_similarity(emb1, emb2).mean().item()

print(f"正在为样本 '{SONGJIANG_SAMPLE}' 创建声纹...")
songjiang_embedding = get_embedding(SONGJIANG_SAMPLE)

print("正在分析日志文件并为每个说话人创建声纹...")
audio = AudioSegment.from_wav(ORIGINAL_VOCALS)
speaker_embeddings = {}
with open(DIARIZATION_LOG, 'r', encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split(" | ")
        start_ms = float(parts[0].split(": ")[1][:-1]) * 1000
        end_ms = float(parts[1].split(": ")[1][:-1]) * 1000
        speaker = parts[2].split(": ")[1]
        segment = audio[start_ms:end_ms]
        # 跳过过短片段
        if len(segment) < 1000:  # pydub单位为毫秒，1000ms=1秒
            print(f"警告: {speaker} 片段 {start_ms/1000:.2f}-{end_ms/1000:.2f}s 过短，已跳过。")
            continue
        segment.export("temp_segment.wav", format="wav")
        embedding = get_embedding("temp_segment.wav")
        if embedding is None:
            continue
        if speaker not in speaker_embeddings:
            speaker_embeddings[speaker] = []
        speaker_embeddings[speaker].append(embedding)

avg_embeddings = {
    spk: torch.mean(torch.stack(embs), dim=0)
    for spk, embs in speaker_embeddings.items()
}

print("正在匹配最相似的说话人...")
best_match_speaker = None
highest_similarity = -1
for speaker, emb in avg_embeddings.items():
    similarity = cosine_similarity(songjiang_embedding, emb)
    print(f"与 {speaker} 的相似度: {similarity:.4f}")
    if similarity > highest_similarity:
        highest_similarity = similarity
        best_match_speaker = speaker

if best_match_speaker:
    print(f"\n识别完成！'{best_match_speaker}' 最有可能是宋江。")
else:
    print("未能找到匹配的说话人。")
    exit(1)

print("正在导出并合并所有宋江的音频片段...")
songjiang_compilation = AudioSegment.empty()
with open(DIARIZATION_LOG, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if best_match_speaker in line:
            parts = line.strip().split(" | ")
            start_ms = float(parts[0].split(": ")[1][:-1]) * 1000
            end_ms = float(parts[1].split(": ")[1][:-1]) * 1000
            clip = audio[start_ms:end_ms]
            songjiang_compilation += clip

songjiang_compilation.export(FINAL_OUTPUT, format="mp3")
print(f"任务完成！所有宋江的声音已合成为 '{FINAL_OUTPUT}'。")
if os.path.exists("temp_segment.wav"):
    os.remove("temp_segment.wav")

