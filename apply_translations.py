#!/usr/bin/env python3
"""
ZeroClaw 全面翻译脚本

此脚本只翻译字符串字面量，不影响代码标识符。
"""

import os
import re

SOURCE_DIR = os.environ.get('LOCAL_SOURCE', '/tmp/zeroclaw-bootstrap-3Q90vt')

# 完整翻译映射表 - 按文件分组
# 格式: (文件路径, 原始字符串, 翻译后字符串)
TRANSLATIONS = {
    # main.rs - CLI 命令和帮助
    "main.rs": [
        ('The fastest, smallest AI assistant.', '最小最快的人工智能助手。'),
        ('Initialize your workspace and configuration', '初始化工作区和配置'),
        ('Run the full interactive wizard', '运行完整的交互式向导'),
        ('Overwrite existing config without confirmation', '覆盖现有配置无需确认'),
        ('Reconfigure channels only', '仅重新配置频道'),
        ('API key', 'API 密钥'),
        ('Provider name', '提供商名称'),
        ('Model ID override', '模型 ID 覆盖'),
        ('Memory backend', '记忆后端'),
        ('Start the AI agent loop', '启动 AI agent 循环'),
        ('Start the gateway server', '启动网关服务器'),
        ('Start long-running autonomous runtime', '启动长时间运行的自主运行时'),
        ('Manage OS service lifecycle', '管理操作系统服务生命周期'),
        ('Run diagnostics', '运行诊断'),
        ('Show system status', '显示系统状态'),
        ('Self-update ZeroClaw', '更新 ZeroClaw'),
        ('Engage, inspect, and resume emergency-stop states', '启动、检查和恢复紧急停止状态'),
        ('Manage security maintenance tasks', '管理安全维护任务'),
        ('Configure and manage scheduled tasks', '配置和管理计划任务'),
        ('Manage provider model catalogs', '管理提供商模型目录'),
        ('List supported AI providers', '列出支持的 AI 提供商'),
        ('Manage channels', '管理频道'),
        ('Browse 50+ integrations', '浏览集成'),
        ('Manage skills', '管理技能'),
        ('Migrate data', '迁移数据'),
        ('Manage authentication profiles', '管理认证配置'),
        ('Discover USB hardware', '发现 USB 硬件'),
        ('Manage hardware peripherals', '管理硬件外设'),
        ('Manage agent memory', '管理 agent 记忆'),
        ('Manage configuration', '管理配置'),
        ('Generate shell completion', '生成 shell 补全'),
    ],

    # daemon/mod.rs
    "daemon/mod.rs": [
        ('ZeroClaw daemon started', 'ZeroClaw 守护进程已启动'),
        ('Gateway:', '网关：'),
        ('Components:', '组件：'),
    ],

    # gateway/mod.rs
    "gateway/mod.rs": [
        ('ZeroClaw Channel Server', 'ZeroClaw 频道服务器'),
        ('Model:', '模型：'),
        ('Memory:', '记忆：'),
        ('Channels:', '频道：'),
        ('Listening for messages', '正在监听消息'),
        ('In-flight message limit', '飞行中消息限制'),
    ],
}


def translate_file(filepath, translations):
    """翻译单个文件"""
    if not os.path.exists(filepath):
        return 0

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    count = 0

    for original, translated in translations:
        if original in content:
            content = content.replace(original, translated)
            count += 1

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return count


def main():
    """主函数"""
    print(f"使用源代码目录: {SOURCE_DIR}")

    total = 0
    for filename, translations in TRANSLATIONS.items():
        filepath = os.path.join(SOURCE_DIR, 'src', filename)
        count = translate_file(filepath, translations)
        if count > 0:
            print(f"  {filename}: {count} 条")
            total += count

    print(f"\n总共翻译: {total} 条")
    return total


if __name__ == '__main__':
    main()
