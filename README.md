# PhantomCrawler

## 高级隐匿爬虫框架 | 七宗欲核心引擎

### 功能特性
- 动态指纹伪装与行为模拟
- 协议混淆与反检测机制
- 元认知系统与七宗欲引擎
- 递归路径测试与智能爬取
- **恨世彩蛋模式** - 七宗欲的终极形态

### 恨世彩蛋
PhantomCrawler中隐藏着七宗欲引擎的第八宗欲——"恨世"。作为七宗欲的终极形态，它代表着引擎最强大也最神秘的力量。

关于它的传说众说纷纭，但没有人确切知道如何唤醒这个沉睡的巨人。有人说它与高级测试模块有关，也有人相信只有真正理解七宗欲本质的人才能触碰到它。

**注意：** 无论你是否找到激活方法，请务必在绝对安全的环境中进行尝试。

### 项目结构
- `src/core/` - 核心爬虫实现
- `src/modules/` - 功能模块集合
- `src/configs/` - 配置文件
- `examples/` - 示例脚本
- `docs/` - 文档

## 专业网络爬虫与安全测试框架

PhantomCrawler 是一个专为安全研究人员、网络管理员和开发团队设计的专业爬虫框架，主要用于安全评估、漏洞测试和网络应用性能分析。框架集成了先进的指纹模拟、行为仿真和自适应学习系统，用于测试和强化网络应用的安全性。

## 核心功能

### 智能爬取策略系统

PhantomCrawler 内置了七种不同的爬取策略，可根据目标系统的特性自动或手动选择：

- **高效模式**: 适用于内部系统或授权测试环境，采用直接高效的爬取策略
- **模拟模式**: 专注于精确模拟真实用户行为和浏览器特性
- **轮换模式**: 针对有访问频率限制的系统，通过身份轮换实现持续测试
- **隐匿模式**: 低频率、高隐蔽性的爬取方式，适用于敏感系统的安全评估
- **平衡模式**: 优化效率与安全性的通用模式，适合大多数测试场景
- **批量模式**: 高性能数据采集策略，用于大规模系统评估
- **深度模式**: 高级渗透测试模式，用于突破复杂安全控制进行授权测试

### 高级安全测试模块

框架还包含了专业安全测试功能模块，提供：
- 递归路径测试（自动发现并评估关联链接）
- 资源压力测试能力（用于评估系统稳定性和性能极限）
- 自适应学习机制（从测试结果中优化测试策略）
- 会话管理功能（用于测试过程中的日志控制）

**⚠️ 重要安全提示**：高级测试模块功能仅供授权的安全测试使用，必须在获得明确授权的系统上运行，且应遵循安全测试的最佳实践。

## 技术亮点

### 1. 动态指纹模拟系统
- User-Agent 智能轮换
- JA3/TLS 指纹仿真
- HTTP 头特征匹配
- 完整浏览器环境模拟

### 2. 行为仿真引擎
- 基于伽马分布的自然时间间隔
- 会话角色模拟
- 交互模式仿真
- 请求序列优化技术

### 3. 元认知自适应系统
- 实时环境变化监控
- 自动爬取策略调整
- 从失败中学习的能力
- 自适应成功率优化

### 4. 多层代理与协议转换
- 代理链管理
- 协议特征转换
- 分布式请求分发

## 快速开始

### 环境准备

```bash
# 克隆仓库
git clone https://github.com/phantom-crawler/PhantomCrawler.git
cd PhantomCrawler

# 安装依赖
pip install -r requirements.txt

# 初始化Playwright（用于高级浏览器自动化）
playwright install
```

### 基本使用示例

```python
from src.core.crawler import PhantomCrawler

# 创建爬虫实例
crawler = PhantomCrawler()

# 初始化爬虫
if crawler.initialize():
    # 爬取单个URL
    result = crawler.crawl("https://target-website.com")
    print(f"爬取状态码: {result['status_code']}")
    
    # 批量爬取
    urls = ["https://page1.com", "https://page2.com"]
    batch_results = crawler.crawl_batch(urls, max_concurrent=2)
    
    # 关闭爬虫
    crawler.close()
```

### 命令行使用

```bash
# 单个URL爬取
python main.py --url https://target-site.com --stealth

# 批量爬取
python main.py --list targets.txt --output-dir results --balanced

# 使用高级功能（需授权）
python main.py --url https://target-site.com --advanced --recursive-test
```

## 配置选项

### 主要命令行参数

| 参数 | 描述 |
|------|------|
| `-u, --url` | 目标URL |
| `-l, --list` | URL列表文件路径 |
| `-c, --config` | 配置文件路径 |
| `-o, --output` | 输出文件路径 |
| `-d, --output-dir` | 输出目录路径 |
| `--stealth` | 启用最高级别隐匿模式 |
| `--aggressive` | 启用高效爬取模式 |
| `--balanced` | 启用平衡模式（默认） |
| `--advanced` | 激活高级测试模块（警告：需授权使用） |
| `--recursive-test` | 启用递归路径测试模式 |

### 功能开关

```python
# 指纹伪装
global_config.set('fingerprint.enable_dynamic_ua', True)
global_config.set('fingerprint.enable_ja3_simulation', True)

# 行为模拟
global_config.set('behavior_simulation.enable_human_delay', True)
global_config.set('behavior_simulation.use_gamma_distribution', True)

# 元认知系统
global_config.set('metacognition.enabled', True)
```

## 示例脚本

框架提供了多个示例脚本帮助快速上手：

- **basic_usage.py**: 基础使用示例
- **crawling_strategies.py**: 爬取策略使用示例
- **advanced_testing.py**: 高级测试模块使用示例
- **adaptive_learning.py**: 自适应学习系统使用示例

## 文档资源

- **安全测试最佳实践**: `docs/安全测试最佳实践.md`
- **渗透测试指南**: `docs/渗透测试指南.md`
- **防御加固指南**: `docs/防御加固指南.md`

## 安全与责任

**⚠️ 重要警告**:

1. 本工具仅用于授权的安全测试、漏洞研究和系统加固目的
2. 在使用前必须获得目标系统所有者的明确书面授权
3. 用户必须严格遵守所有适用的法律法规和伦理准则
4. 开发者不对任何未经授权或不当使用行为负责
5. 高级测试功能必须在隔离环境中进行测试，并严格控制在授权范围内使用
6. 使用本工具时应采取必要措施避免对目标系统造成意外损害

## 贡献指南

我们欢迎安全研究人员的贡献：

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

## 免责声明

使用本工具即表示您同意：
- 仅在获得明确授权的系统上使用，且严格限制在授权的测试范围内
- 遵守所有适用的法律法规、行业标准和道德规范
- 承担因使用本工具产生的所有责任和后果
- 不将本工具用于任何非法、不道德或未经授权的活动

本工具旨在帮助安全专业人员提高网络安全性，而不是为恶意活动提供便利。任何滥用行为都将违反本项目的初衷和用户协议。

© 2023 PhantomCrawler Project. All rights reserved.