from pydub import AudioSegment

audio = AudioSegment.from_wav("demo_audio.wav")
first_20s = audio[:20 * 1000]  # 前20秒
first_20s.export("demo_audio_20s.wav", format="wav")
print("已保存为 demo_audio_20s.wav")