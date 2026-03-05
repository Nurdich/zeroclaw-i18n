// ZeroClaw 中文国际化模块
// ZeroClaw Chinese Internationalization Module

/// 中文翻译映射
pub mod zh_CN {
    // ============ 授权相关消息 ============
    
    pub const SUPERVISED_NON_CLI_TOOL_APPROVALS: &str = "受监管的非 CLI 工具授权:\n";
    
    pub const RUNTIME_AUTO_APPROVE_EFFECTIVE_NONE: &str = "- Runtime auto_approve (effective): (none)\n";
    pub const RUNTIME_AUTO_APPROVE_EFFECTIVE: &str = "- Runtime auto_approve (effective): ";
    
    pub const RUNTIME_ALWAYS_ASK_EFFECTIVE_NONE: &str = "- Runtime always_ask (effective): (none)\n";
    pub const RUNTIME_ALWAYS_ASK_EFFECTIVE: &str = "- Runtime always_ask (effective): ";
    
    pub const RUNTIME_SESSION_GRANTS_NONE: &str = "- Runtime session grants: (none)\n";
    pub const RUNTIME_SESSION_GRANTS: &str = "- Runtime session grants: ";
    
    pub const RUNTIME_NON_CLI_APPROVAL_APPROVERS: &str = "- Runtime non_cli_approval_approvers: (any channel-allowed sender)\n";
    pub const RUNTIME_NON_CLI_NATURAL_LANGUAGE_APPROVAL_MODE: &str = "- Runtime non_cli_natural_language_approval_mode (current channel telegram): ";
    pub const RUNTIME_NON_CLI_NATURAL_LANGUAGE_APPROVAL_MODE_BY_CHANNEL_NONE: &str = "- Runtime non_cli_natural_language_approval_mode_by_channel: (none)\n";
    pub const RUNTIME_NON_CLI_NATURAL_LANGUAGE_APPROVAL_MODE_BY_CHANNEL: &str = "- Runtime non_cli_natural_language_approval_mode_by_channel: ";
    
    pub const PENDING_APPROVALS_NONE: &str = "- Pending approvals (sender+chat/channel scoped): (none)\n";
    pub const PENDING_APPROVALS: &str = "- Pending approvals (sender+chat/channel scoped):\n";
    
    pub const RUNTIME_NON_CLI_EXCLUDED_TOOLS_NONE: &str = "- Runtime non_cli_excluded_tools: (none)\n";
    pub const RUNTIME_NON_CLI_EXCLUDED_TOOLS: &str = "- Runtime non_cli_excluded_tools: ";
    
    pub const PERSISTED_AUTONOMY_AUTO_APPROVE_NONE: &str = "- Persisted autonomy.auto_approve: (none)\n";
    pub const PERSISTED_AUTONOMY_AUTO_APPROVE: &str = "- Persisted autonomy.auto_approve: ";
    
    pub const PERSISTED_AUTONOMY_ALWAYS_ASK_NONE: &str = "- Persisted autonomy.always_ask: (none)\n";
    pub const PERSISTED_AUTONOMY_ALWAYS_ASK: &str = "- Persisted autonomy.always_ask: ";
    
    pub const CONFIG_PATH: &str = "- Config path: ";
    
    pub const RUNTIME_ONE_TIME_ALL_TOOLS_BYPASS_TOKENS: &str = "- Runtime one-time all-tools bypass tokens: ";
    
    // ============ 帮助消息 ============
    
    pub const CURRENT_PROVIDER: &str = "当前提供商: `{}`\n当前模型: `{}`";
    pub const CURRENT_PROVIDER_MODEL: &str = "当前提供商: `{}`\n当前模型: `{}`";
    
    pub const SWITCH_MODEL: &str = "\n使用 `/model <模型ID>` 切换模型。\n";
    pub const REQUEST_SUPERVISED_TOOL_APPROVAL: &str = "使用 `/approve-request <工具名>` 请求受监管工具授权。\n";
    pub const REQUEST_ONE_TIME_ALL_TOOLS_APPROVAL: &str = "使用 `/approve-all-once` 请求一次性全工具授权。\n";
    pub const CONFIRM_APPROVAL: &str = "使用 `/approve-confirm <请求ID>` 确认授权。\n";
    pub const DENY_APPROVAL: &str = "使用 `/approve-deny <请求ID>` 拒绝授权。\n";
    pub const LIST_PENDING_REQUESTS: &str = "使用 `/approve-pending` 查看待处理请求。\n";
    pub const APPROVE_SUPERVISED_TOOLS: &str = "使用 `/approve <工具名>` 授权受监管工具。\n";
    pub const REVOKE_APPROVAL: &str = "使用 `/unapprove <工具名>` 撤销授权。\n";
    pub const LIST_APPROVAL_STATE: &str = "使用 `/approvals` 查看授权状态。\n";
    
    pub const NATURAL_LANGUAGE_ALSO_WORKS: &str = "自然语言也可以（受策略控制）。\n - `direct` 模式（默认）：`授权工具 shell` 立即授予。\n - `request_confirm` 模式：`授权工具 shell` 然后 `确认授权 apr-xxxxxx`。\n";
    
    pub const NO_CACHED_MODEL_LIST: &str = "\n未找到 `{}` 的缓存模型列表。请让管理员运行 `zeroclaw models refresh --provider {}`。";
    pub const CACHED_MODEL_IDS: &str = "\n缓存的模型 ID (前{}个):";
    
    pub const SWITCH_PROVIDER: &str = "\n使用 `/models <提供商>` 切换提供商。\n";
    
    pub const AVAILABLE_PROVIDERS: &str = "\n可用提供商:\n";
    
    pub const PENDING_APPROVAL_REQUESTS: &str = "待处理的授权请求 (sender+chat/channel 范围):\n";
    
    // ============ 其他常用消息 ============
    
    pub const TOOL_USE_PROTOCOL: &str = "## 工具使用协议\n\n要使用工具，请在 <tool_call></tool_call> 标签中包装一个 JSON 对象:\n\n";
    pub const RUNTIME_TOOL_AVAILABILITY: &str = "\n## 运行时工具可用性 (权威)\n\n";
    pub const ALLOWED_TOOLS: &str = "- 允许的工具 ({}):";
    pub const MEMORY_CONTEXT: &str = "[记忆上下文]\n";
    pub const HARDWARE_DOCUMENTATION: &str = "[硬件文档]\n";
    pub const COMPLETED_STEPS: &str = "已完成步骤:\n";
    pub const IDENTITY: &str = "## 身份\n\n";
    pub const FILE_NOT_FOUND: &str = "\n\n[文件未找到: {}]\n";
}

/// 获取翻译后的授权状态描述
pub fn get_approval_description(tool: &str) -> String {
    match tool {
        "file_read" => "文件读取".to_string(),
        "memory_recall" => "记忆召回".to_string(),
        "shell" => "终端命令".to_string(),
        "file_write" => "文件写入".to_string(),
        "file_edit" => "文件编辑".to_string(),
        "memory_store" => "记忆存储".to_string(),
        "memory_forget" => "记忆删除".to_string(),
        "git_operations" => "Git 操作".to_string(),
        "browser" => "浏览器".to_string(),
        "browser_open" => "浏览器打开".to_string(),
        "http_request" => "HTTP 请求".to_string(),
        "schedule" => "计划任务".to_string(),
        "cron_add" => "添加定时任务".to_string(),
        "cron_remove" => "删除定时任务".to_string(),
        "cron_update" => "更新定时任务".to_string(),
        "cron_run" => "运行定时任务".to_string(),
        "proxy_config" => "代理配置".to_string(),
        "model_routing_config" => "模型路由配置".to_string(),
        "pushover" => "推送通知".to_string(),
        "composio" => "Composio 集成".to_string(),
        "delegate" => "委托".to_string(),
        "screenshot" => "截图".to_string(),
        "image_info" => "图片信息".to_string(),
        _ => tool.to_string(),
    }
}
