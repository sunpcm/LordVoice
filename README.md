# LordVoice 项目说明

本项目用于自动提取视频中的宋江声音片段，适用于《水浒传》相关音视频资料的处理。流程涵盖音频提取、人声分离、说话人分段、声纹识别与宋江音频导出。

---

## 环境准备

1. 建议使用 Python 3.8 及以上版本。
2. 推荐使用虚拟环境（如 venv、.venv、conda）。
3. 安装依赖：

```bash
pip install -r requirements.txt
```

4. 安装 ffmpeg（音视频处理工具）：
   - Ubuntu: `sudo apt install ffmpeg`
   - Mac: `brew install ffmpeg`
   - Windows: [下载并配置 ffmpeg](https://ffmpeg.org/download.html)

---

## 项目目录结构

```
LordVoice/
├── audio_extract.py           # 视频转音频脚本
├── diarize.py                 # 说话人分段脚本
├── identify_and_export.py     # 声纹识别与宋江音频导出脚本
├── requirements.txt           # 依赖列表
├── README.md                  # 项目说明
├── index.txt                  # 项目流程说明
├── separated/                 # 人声分离输出目录（demucs生成）
├── songjiang_clips/           # 宋江音频片段输出目录
├── pretrained_models/         # 声纹模型缓存目录
└── ...
```

---

## 使用流程

### 1. 提取音频
将原始视频（如 `demo.mp4`）放入项目根目录，运行：

```bash
python audio_extract.py
```

生成 `demo_audio.wav`。

### 2. 分离人声
使用 demucs 工具分离人声：

```bash
demucs --two-stems=vocals demo_audio.wav
```

输出文件位于 `separated/htdemucs/vocals.wav`。

### 3. 说话人分段
编辑 `diarize.py`，将 `HF_TOKEN` 替换为你的 Hugging Face Token。

```python
HF_TOKEN = "你的 Hugging Face Token"
```

运行：

```bash
python diarize.py
```

生成 `diarization_log.txt`。

### 4. 宋江声纹识别与导出
准备宋江的干净语音样本 `songjiang_sample.wav`，放在项目根目录。

运行：

```bash
python identify_and_export.py
```

自动识别宋江并导出所有片段，合成为 `songjiang_voice_compilation.mp3`。

---

## 常见问题

- Hugging Face Token 获取：注册 [Hugging Face](https://huggingface.co/)，在 Settings -> Access Tokens 创建。
- ffmpeg 未安装或未加入 PATH 时，音频提取会失败。
- 依赖安装失败时，建议升级 pip 并单独安装出错的包。
- 运行过程中如遇显存不足，可尝试在 CPU 上运行。

---

## 参考
- [pyannote.audio](https://github.com/pyannote/pyannote-audio)
- [demucs](https://github.com/facebookresearch/demucs)
- [speechbrain](https://github.com/speechbrain/speechbrain)

如有问题请提交 issue 或联系作者。

