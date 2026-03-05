#!/usr/bin/env python3
"""
ZeroClaw 翻译同步脚本

用法:
    python sync_translations.py                    # 应用翻译并编译
    python sync_translations.py --check           # 检查未翻译的字符串
    python sync_translations.py --pull            # 从上游拉取最新代码
    python sync_translations.py --build           # 编译
    python sync_translations.py --install         # 安装
    python sync_translations.py --all             # 完整流程
"""

import os
import re
import subprocess
import sys
import shutil
from pathlib import Path
from datetime import datetime

# 配置
ZEROCLAW_REPO = os.environ.get('ZEROCLAW_REPO', '/tmp/zeroclaw-upstream')
TRANSLATIONS_DIR = Path(__file__).parent

# 精确翻译映射表 - 只翻译用户可见的字符串
# 格式: (文件路径, 原始字符串, 翻译后字符串)
TRANSLATIONS = [
    # channels/mod.rs
    ("channels/mod.rs", '"Supervised non-CLI tool approvals:\n"', '"受监管的非 CLI 工具授权:\n"'),
    ("channels/mod.rs", '"- Runtime auto_approve (effective): (none)\n"', '"- Runtime auto_approve (effective): (无)\n"'),
    ("channels/mod.rs", '"- Runtime always_ask (effective): (none)\n"', '"- Runtime always_ask (effective): (无)\n"'),
    ("channels/mod.rs", '"- Runtime session grants: (none)\n"', '"- Runtime session grants: (无)\n"'),
    ("channels/mod.rs", '"- Runtime non_cli_approval_approvers: (any channel-allowed sender)\n"', '"- Runtime non_cli_approval_approvers: (任何允许的发送者)\n"'),
    ("channels/mod.rs", '"- Runtime non_cli_natural_language_approval_mode_by_channel: (none)\n"', '"- Runtime non_cli_natural_language_approval_mode_by_channel: (无)\n"'),
    ("channels/mod.rs", '"- Pending approvals (sender+chat/channel scoped): (none)\n"', '"- 待处理的授权 (sender+chat/channel 范围): (无)\n"'),
    ("channels/mod.rs", '"- Pending approvals (sender+chat/channel scoped):\n"', '"- 待处理的授权 (sender+chat/channel 范围):\n"'),
    ("channels/mod.rs", '"- Runtime non_cli_excluded_tools: (none)\n"', '"- Runtime non_cli_excluded_tools: (无)\n"'),
    ("channels/mod.rs", '"- Persisted autonomy.auto_approve: (none)\n"', '"- Persisted autonomy.auto_approve: (无)\n"'),
    ("channels/mod.rs", '"- Persisted autonomy.always_ask: (none)\n"', '"- Persisted autonomy.always_ask: (无)\n"'),
    ("channels/mod.rs", '"- Config path: {}"', '"- 配置文件路径: {}"'),
    ("channels/mod.rs", '"Current provider: `{}`\\nCurrent model: `{}`"', '"当前提供商: `{}`\\n当前模型: `{}`"'),
    ("channels/mod.rs", '"\\nSwitch model with `/model <model-id>`.\\n"', '"\\n使用 `/model <模型ID>` 切换模型。\\n"'),
    ("channels/mod.rs", '"Request supervised tool approval with `/approve-request <tool-name>`.\\n"', '"使用 `/approve-request <工具名>` 请求工具授权。\\n"'),
    ("channels/mod.rs", '"Request one-time all-tools approval with `/approve-all-once`.\\n"', '"使用 `/approve-all-once` 请求一次性全工具授权。\\n"'),
    ("channels/mod.rs", '"Confirm approval with `/approve-confirm <request-id>`.\\n"', '"使用 `/approve-confirm <请求ID>` 确认授权。\\n"'),
    ("channels/mod.rs", '"Deny approval with `/approve-deny <request-id>`.\\n"', '"使用 `/approve-deny <请求ID>` 拒绝授权。\\n"'),
    ("channels/mod.rs", '"List pending requests with `/approve-pending`.\\n"', '"使用 `/approve-pending` 查看待处理请求。\\n"'),
    ("channels/mod.rs", '"Approve supervised tools with `/approve <tool-name>`.\\n"', '"使用 `/approve <工具名>` 授权工具。\\n"'),
    ("channels/mod.rs", '"Revoke approval with `/unapprove <tool-name>`.\\n"', '"使用 `/unapprove <工具名>` 撤销授权。\\n"'),
    ("channels/mod.rs", '"List approval state with `/approvals`.\\n"', '"使用 `/approvals` 查看授权状态。\\n"'),
    ("channels/mod.rs", '"Natural language also works (policy controlled).\\n\\         - `direct` mode (default): `授权工具 shell` grants immediately.\\n\\         - `request_confirm` mode: `授权工具 shell` then `确认授权 apr-xxxxxx`.\\n"',
     '"自然语言也可以（受策略控制）。\\n - `direct` 模式（默认）：`授权工具 shell` 立即授予。\\n - `request_confirm` 模式：`授权工具 shell` 然后 `确认授权 apr-xxxxxx`。\\n"'),
    ("channels/mod.rs", '"\\nNo cached model list found for `{}`. Ask the operator to run `zeroclaw models refresh --provider {}`."',
     '"\\n未找到 `{}` 的缓存模型列表。请让管理员运行 `zeroclaw models refresh --provider {}`。"'),
    ("channels/mod.rs", '"\\nCached model IDs (top {}):"', '"\\n缓存的模型 ID (前{}个):"'),
    ("channels/mod.rs", '"\\nSwitch provider with `/models <provider>`.\\n"', '"\\n使用 `/models <提供商>` 切换提供商。\\n"'),
    ("channels/mod.rs", '"Available providers:\\n"', '"可用提供商:\\n"'),
    ("channels/mod.rs", '"Pending approval request `{}` was not found."', '"待处理的授权请求 `{}` 未找到。"'),
    ("channels/mod.rs", '"Pending approval request `{}` has expired."', '"待处理的授权请求 `{}` 已过期。"'),
    ("channels/mod.rs", '"Pending approval request `{}` can only be approved by the same sender in the same chat/channel that created it."',
     '"待处理的授权请求 `{}` 只能由在同一聊天/频道中创建的发送者批准。"'),
    ("channels/mod.rs", '"Usage: `/approve-confirm <request-id>`".to_string()', '"用法: `/approve-confirm <请求ID>`".to_string()'),
    ("channels/mod.rs", '"Pending approval requests (sender+chat/channel scoped):\\n"', '"待处理的授权请求 (sender+chat/channel 范围):\\n"'),
    ("channels/mod.rs", '"- Runtime non_cli_natural_language_approval_mode (current channel `{}`): {}"',
     '"- Runtime non_cli_natural_language_approval_mode (当前频道 `{}`): {}"'),
    ("channels/mod.rs", '"- Runtime non_cli_natural_language_approval_mode: {}"', '"- Runtime non_cli_natural_language_approval_mode: {}"'),
]


def run_cmd(cmd, cwd=None, check=True):
    """运行命令并返回结果"""
    result = subprocess.run(
        cmd, shell=True, cwd=cwd,
        capture_output=True, text=True
    )
    if check and result.returncode != 0:
        print(f"命令失败: {cmd}")
        print(result.stderr)
        sys.exit(1)
    return result


def pull_upstream():
    """从上游拉取最新代码"""
    print("正在从上游拉取最新代码...")

    if os.path.exists(ZEROCLAW_REPO):
        os.chdir(ZEROCLAW_REPO)
        run_cmd("git fetch origin")
        run_cmd("git checkout main")
        run_cmd("git pull origin main")
    else:
        run_cmd(f"git clone https://github.com/zeroclaw-labs/zeroclaw.git {ZEROCLAW_REPO}")

    print(f"已更新代码到: {ZEROCLAW_REPO}")
    return ZEROCLAW_REPO


def apply_translations(source_dir):
    """应用翻译到源代码"""
    print("\n正在应用翻译...")

    translated_files = set()

    for file_path, original, translated in TRANSLATIONS:
        full_path = Path(source_dir) / "src" / file_path

        if not full_path.exists():
            print(f"  警告: 文件不存在 {full_path}")
            continue

        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if original in content:
            content = content.replace(original, translated)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            translated_files.add(file_path)

    for f in translated_files:
        print(f"  已翻译: {f}")

    print(f"\n翻译完成! 共翻译 {len(translated_files)} 个文件")


def check_translations(source_dir):
    """检查翻译是否正确应用"""
    print("\n检查翻译...")
    issues = []

    for file_path, original, translated in TRANSLATIONS:
        full_path = Path(source_dir) / "src" / file_path
        if not full_path.exists():
            continue

        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查原始英文是否还存在
        if original in content:
            issues.append(f"{file_path}: 缺少翻译 - {original[:50]}...")

        # 检查翻译是否正确
        if translated not in content:
            issues.append(f"{file_path}: 翻译丢失 - {translated[:50]}...")

    if issues:
        print("发现的问题:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("所有翻译检查通过!")

    return len(issues) == 0


def build_zeroclaw(source_dir):
    """编译 ZeroClaw"""
    print("\n正在编译 ZeroClaw...")
    os.chdir(source_dir)

    # 设置 Rust 环境
    env = os.environ.copy()
    rust_env = os.path.expanduser("~/.cargo/env")
    if os.path.exists(rust_env):
        with open(rust_env) as f:
            for line in f:
                if line.startswith('export'):
                    _, var = line.strip().split(' ', 1)
                    key, value = var.split('=', 1)
                    env[key] = value.replace('"', '')

    result = subprocess.run(
        ["cargo", "build", "--release"],
        env=env,
        capture_output=True,
        text=True,
        cwd=source_dir
    )

    if result.returncode == 0:
        binary_path = Path(source_dir) / "target" / "release" / "zeroclaw"
        print(f"编译成功! 二进制文件: {binary_path}")
        return binary_path
    else:
        print(f"编译失败:")
        print(result.stderr[-2000:])
        return None


def install_binary(binary_path, install_path="/usr/local/bin/zeroclaw"):
    """安装二进制文件"""
    print(f"\n正在安装到 {install_path}...")

    # 如果文件忙，先停止 zeroclaw
    if os.path.exists(install_path):
        subprocess.run(["pkill", "-f", "zeroclaw"], capture_output=True)
        import time
        time.sleep(1)

    # 使用临时文件
    temp_path = install_path + ".new"
    shutil.copy(str(binary_path), temp_path)
    os.rename(temp_path, install_path)
    os.chmod(install_path, 0o755)

    print("安装完成!")

    # 验证
    result = subprocess.run([install_path, "--version"], capture_output=True, text=True)
    print(f"版本: {result.stdout.strip()}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="ZeroClaw 翻译同步工具")
    parser.add_argument("--pull", action="store_true", help="从上游拉取最新代码")
    parser.add_argument("--check", action="store_true", help="检查翻译是否正确")
    parser.add_argument("--apply", action="store_true", help="应用翻译")
    parser.add_argument("--build", action="store_true", help="编译")
    parser.add_argument("--install", action="store_true", help="安装")
    parser.add_argument("--all", action="store_true", help="执行完整流程")
    parser.add_argument("--source", default=ZEROCLAW_REPO, help="源代码目录")

    args = parser.parse_args()

    source_dir = args.source

    # 如果指定 --all 或没有参数，默认执行翻译+编译+安装
    if args.all or (not args.pull and not args.check and not args.build and not args.install):
        args.apply = True
        args.build = True
        args.install = True

    if args.pull:
        source_dir = pull_upstream()

    if args.apply:
        apply_translations(source_dir)

    if args.check:
        check_translations(source_dir)

    if args.build:
        binary = build_zeroclaw(source_dir)
        if binary and args.install:
            install_binary(binary)

    if args.apply and args.build and args.install:
        print("\n" + "="*50)
        print("ZeroClaw 翻译更新完成!")
        print("="*50)


if __name__ == "__main__":
    main()
