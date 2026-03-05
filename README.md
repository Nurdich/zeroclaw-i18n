# ZeroClaw 中文国际化 (i18n)

本模块提供 ZeroClaw 的中文翻译支持。

## 目录结构

```
zeroclaw-i18n/
├── sync_translations.py    # 翻译同步脚本
├── src/
│   └── lib.rs              # 翻译库（可选）
└── README.md               # 本文件
```

## 快速开始

### 完整流程（翻译 + 编译 + 安装）

```bash
cd /root/work/zeroclaw-i18n
python3 sync_translations.py --all
```

### 分步执行

1. **从上游拉取最新代码**
```bash
python3 sync_translations.py --pull
```

2. **应用翻译**
```bash
python3 sync_translations.py --apply
```

3. **编译**
```bash
python3 sync_translations.py --build
```

4. **安装**
```bash
python3 sync_translations.py --install
```

### 检查翻译状态
```bash
python3 sync_translations.py --check
```

## 翻译更新流程

当上游 ZeroClaw 发布新版本时，执行：

```bash
# 1. 设置源代码目录（可选，默认 /tmp/zeroclaw-upstream）
export ZEROCLAW_REPO=/path/to/zeroclaw

# 2. 完整流程
python3 sync_translations.py --all
```

脚本会自动：
1. 从 GitHub 拉取最新代码
2. 应用翻译到源代码
3. 编译 ZeroClaw
4. 安装到系统

## 翻译覆盖

当前已翻译的消息：

- `/approvals` 命令输出
- `/model` 命令帮助
- `/models` 命令帮助
- `/approve-request` 命令帮助
- `/approve-confirm` 命令帮助
- `/approve-deny` 命令帮助
- 待处理授权相关消息

## 添加新翻译

编辑 `sync_translations.py` 中的 `TRANSLATIONS` 列表，添加新的翻译：

```python
("channels/mod.rs", '原始英文', '翻译后中文'),
```

## 注意事项

1. 翻译必须精确匹配原始字符串
2. 不要翻译代码标识符（如 `ToolSpec`, `ToolDispatcher` 等）
3. 编译前运行 `--check` 验证翻译
