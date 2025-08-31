#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LordVoice 项目安装脚本
自动安装依赖并配置项目环境
"""

import subprocess
import sys
import os
import platform

def run_command(command, description):
    """运行命令并显示结果"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True,
                              capture_output=True, text=True)
        print(f"✓ {description}完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description}失败: {e.stderr}")
        return False

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("✗ 需要Python 3.8或更高版本")
        return False
    print(f"✓ Python版本: {version.major}.{version.minor}.{version.micro}")
    return True

def install_ffmpeg():
    """安装FFmpeg"""
    system = platform.system().lower()

    if system == "windows":
        print("\n请手动安装FFmpeg:")
        print("1. 访问 https://ffmpeg.org/download.html")
        print("2. 下载Windows版本")
        print("3. 解压并将bin目录添加到PATH环境变量")
        input("安装完成后按回车继续...")
    elif system == "darwin":  # macOS
        print("\n正在安装FFmpeg (macOS)...")
        return run_command("brew install ffmpeg", "安装FFmpeg")
    else:  # Linux
        print("\n正在安装FFmpeg (Linux)...")
        return run_command("sudo apt update && sudo apt install -y ffmpeg", "安装FFmpeg")

    return True

def install_python_packages():
    """安装Python包"""
    packages = [
        "torch>=1.9.0",
        "torchaudio>=0.9.0",
        "demucs>=4.0.0",
        "pyannote.audio",
        "speechbrain>=0.5.0",
        "pydub>=0.25.0",
        "numpy>=1.20.0",
        "matplotlib>=3.3.0",
        "huggingface_hub>=0.10.0"
    ]

    print(f"\n正在安装Python包...")
    for package in packages:
        if not run_command(f"pip install {package}", f"安装{package}"):
            return False
    return True

def setup_huggingface():
    """设置Hugging Face"""
    print("\n=== Hugging Face 配置 ===")
    print("1. 请访问 https://huggingface.co/")
    print("2. 注册或登录账户")
    print("3. 前往 Settings -> Access Tokens")
    print("4. 创建新的访问令牌")

    token = input("\n请输入您的Hugging Face访问令牌: ").strip()

    if token and token != "YOUR_HUGGING_FACE_TOKEN":
        # 更新diarize.py中的令牌
        try:
            with open("diarize.py", "r", encoding="utf-8") as f:
                content = f.read()

            content = content.replace("YOUR_HUGGING_FACE_TOKEN", token)

            with open("diarize.py", "w", encoding="utf-8") as f:
                f.write(content)

            print("✓ Hugging Face令牌已配置")
            return True
        except Exception as e:
            print(f"✗ 配置令牌时出错: {e}")
            return False
    else:
        print("⚠️  跳过令牌配置，请稍后手动配置")
        return True

def create_directories():
    """创建必要的目录"""
    dirs = ["separated", "songjiang_clips", "pretrained_models"]
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
    print("✓ 创建项目目录")

def main():
    """主安装流程"""
    print("欢迎使用 LordVoice 安装程序！")
    print("="*50)

    # 检查Python版本
    if not check_python_version():
        sys.exit(1)

    # 创建目录
    create_directories()

    # 安装FFmpeg
    print("\n=== 安装FFmpeg ===")
    install_ffmpeg()

    # 安装Python包
    print("\n=== 安装Python依赖 ===")
    if not install_python_packages():
        print("安装失败，请手动运行: pip install -r requirements.txt")
        sys.exit(1)

    # 配置Hugging Face
    setup_huggingface()

    print("\n" + "="*50)
    print("🎉 安装完成！")
    print("="*50)
    print("\n下一步:")
    print("1. 将《水浒传》视频文件放在项目目录中")
    print("2. 运行: python start.py")
    print("3. 按照向导完成声音提取")

    print("\n如果遇到问题，请查看 README.md 获取详细说明")

if __name__ == "__main__":
    main()
