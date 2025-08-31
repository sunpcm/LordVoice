#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from pydub import AudioSegment
from pydub.playback import play
import matplotlib.pyplot as plt
import numpy as np

def analyze_audio(audio_file):
    """分析音频文件的基本信息"""
    if not os.path.exists(audio_file):
        print(f"文件不存在: {audio_file}")
        return None

    try:
        audio = AudioSegment.from_file(audio_file)

        print(f"\n音频文件分析: {audio_file}")
        print("-" * 40)
        print(f"时长: {len(audio) / 1000:.2f} 秒")
        print(f"采样率: {audio.frame_rate} Hz")
        print(f"声道数: {audio.channels}")
        print(f"位深度: {audio.sample_width * 8} 位")
        print(f"文件大小: {os.path.getsize(audio_file) / 1024 / 1024:.2f} MB")

        # 音量分析
        loudness = audio.dBFS
        print(f"音量 (dBFS): {loudness:.2f}")

        return audio
    except Exception as e:
        print(f"分析音频时出错: {e}")
        return None

def trim_audio(input_file, start_time, end_time, output_file):
    """裁剪音频片段"""
    try:
        audio = AudioSegment.from_file(input_file)
        start_ms = start_time * 1000
        end_ms = end_time * 1000

        trimmed = audio[start_ms:end_ms]
        trimmed.export(output_file, format="wav")

        print(f"已裁剪音频片段: {start_time}s - {end_time}s")
        print(f"保存到: {output_file}")
        return True
    except Exception as e:
        print(f"裁剪音频时出错: {e}")
        return False

def validate_sample(sample_file):
    """验证宋江样本的质量"""
    audio = analyze_audio(sample_file)
    if not audio:
        return False

    print(f"\n样本质量评估:")
    print("-" * 40)

    # 检查时长
    duration = len(audio) / 1000
    if duration < 3:
        print("⚠️  样本时长过短，建议至少3秒")
    elif duration > 20:
        print("⚠️  样本时长过长，建议不超过20秒")
    else:
        print("✓ 样本时长合适")

    # 检查音量
    loudness = audio.dBFS
    if loudness < -30:
        print("⚠️  音量过低，可能影响识别效果")
    elif loudness > -10:
        print("⚠️  音量过高，可能有削波失真")
    else:
        print("✓ 音量合适")

    # 检查采样率
    if audio.frame_rate < 16000:
        print("⚠️  采样率偏低，建议至少16kHz")
    else:
        print("✓ 采样率合适")

    # 检查声道
    if audio.channels > 1:
        print("⚠️  建议转换为单声道")
    else:
        print("✓ 单声道格式")

    return True

def enhance_sample(input_file, output_file):
    """优化音频样本"""
    try:
        audio = AudioSegment.from_file(input_file)

        # 转换为单声道
        if audio.channels > 1:
            audio = audio.set_channels(1)
            print("✓ 转换为单声道")

        # 标准化采样率
        if audio.frame_rate != 16000:
            audio = audio.set_frame_rate(16000)
            print("✓ 设置采样率为16kHz")

        # 音量标准化
        target_dBFS = -20.0
        change_in_dBFS = target_dBFS - audio.dBFS
        audio = audio.apply_gain(change_in_dBFS)
        print(f"✓ 音量标准化到 {target_dBFS} dBFS")

        # 去除首尾静音
        audio = audio.strip_silence(silence_thresh=-40)
        print("✓ 去除首尾静音")

        audio.export(output_file, format="wav")
        print(f"✓ 优化后的样本保存到: {output_file}")

        return True
    except Exception as e:
        print(f"优化样本时出错: {e}")
        return False

def show_menu():
    """显示工具菜单"""
    print("\n" + "="*50)
    print("         音频样本工具 - LordVoice")
    print("="*50)
    print("1. 分析音频文件")
    print("2. 裁剪音频片段")
    print("3. 验证宋江样本质量")
    print("4. 优化宋江样本")
    print("5. 播放音频文件")
    print("0. 返回主程序")
    print("="*50)

def main():
    """主函数"""
    while True:
        show_menu()
        choice = input("\n请选择操作 (0-5): ").strip()

        if choice == '0':
            break
        elif choice == '1':
            filename = input("请输入音频文件名: ").strip()
            analyze_audio(filename)
        elif choice == '2':
            filename = input("请输入音频文件名: ").strip()
            try:
                start = float(input("开始时间 (秒): "))
                end = float(input("结束时间 (秒): "))
                output = input("输出文件名 (默认: trimmed.wav): ").strip() or "trimmed.wav"
                trim_audio(filename, start, end, output)
            except ValueError:
                print("时间格式错误")
        elif choice == '3':
            sample_file = input("样本文件名 (默认: songjiang_sample.wav): ").strip() or "songjiang_sample.wav"
            validate_sample(sample_file)
        elif choice == '4':
            input_file = input("输入文件名: ").strip()
            output_file = input("输出文件名 (默认: songjiang_sample_enhanced.wav): ").strip() or "songjiang_sample_enhanced.wav"
            enhance_sample(input_file, output_file)
        elif choice == '5':
            filename = input("请输入音频文件名: ").strip()
            try:
                audio = AudioSegment.from_file(filename)
                print("正在播放音频...")
                play(audio)
            except Exception as e:
                print(f"播放音频时出错: {e}")
        else:
            print("无效选择，请重试。")

if __name__ == "__main__":
    main()
