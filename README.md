# PhantomCrawler 🚀

## 七宗欲驱动的爬虫突破系统 | 突破反爬壁垒的专业利器

PhantomCrawler 不是普通的爬虫框架。它是世界首款具备七宗欲引擎的数据采集系统，通过七种不同欲望模式驱动爬虫行为，智能应对各类反爬挑战，融合了一线工程师在数百个项目中积累的实战经验与前沿技术。

## 七宗欲引擎介绍

七宗欲引擎是PhantomCrawler的核心智能系统，基于七种不同的欲望模式驱动爬虫行为，每种欲望代表一种独特的爬取策略：

- **傲慢**: 自信高效，适度伪装，适合低风险网站
- **嫉妒**: 精细模仿，全面保护，适合复杂验证码场景
- **愤怒**: 快速激进，频繁轮换，适合短期高强度爬取
- **懒惰**: 最小交互，长间隔，适合资源敏感型爬取
- **贪婪**: 平衡效率与安全，适合一般场景
- **暴食**: 快速处理，高频轮换，适合批量数据采集
- **色欲**: 极致保护，专注细节，适合高防护网站突破

七宗欲引擎能够根据爬取结果自动调整欲望强度，识别危险信号并切换最佳策略，实现真正的智能爬取。

**当普通爬虫被封锁时，PhantomCrawler 能自我调整并突破障碍，持续完成任务。**

---

## 为什么选择 PhantomCrawler？

在当今竞争激烈的数据分析领域，数据就是金矿。但网站的反爬技术也在不断升级 - 从简单的IP封锁到复杂的行为分析，从验证码到浏览器指纹识别。

PhantomCrawler 通过以下方式解决这些挑战，且**完全零成本**：

- **元认知能力**：内置自我感知和学习优化机制，能像人类工程师一样从经验中学习并调整策略
- **模拟真实用户**：不仅模仿浏览器指纹，更复制真实人类的浏览习惯和行为模式
- **智能适应**：根据目标网站的反应动态调整策略，就像经验丰富的爬虫工程师在操作
- **环境感知**：自动检测反爬策略变化，实时调整行为模式，实现持续有效的数据采集
- **企业级稳定性**：经过实战验证的架构设计，确保在大规模数据采集任务中稳定可靠
- **合规可控**：提供精细的配置选项，让你在获取所需数据的同时，遵守相关法律法规
- **零成本实现**：可在个人电脑上完全运行，无需昂贵的云服务器，一杯可乐的价格都不需要

## 🔍 核心技术亮点

### 动态浏览器指纹模拟
* **多维度指纹伪装**：生成符合Chrome、Firefox、Safari等真实浏览器的HTTP头部、TLS握手参数和JavaScript环境特征
* **JA3/JA3S指纹定制**：精确模拟主流浏览器的TLS握手行为，有效规避基于SSL指纹的爬虫检测
* **指纹轮换策略**：智能管理指纹池，根据网站响应动态切换指纹，降低被识别风险

### 人类行为仿真引擎
* **自然鼠标轨迹生成**：基于真实用户数据训练的贝塞尔曲线算法，生成包含加速度变化和微小抖动的自然鼠标移动路径
* **阅读节奏模拟**：根据页面内容复杂度自动调整滚动速度和停留时间，完全符合人类阅读习惯
* **随机决策系统**：引入合理的随机性，模拟人类浏览时的注意力分散和无意识操作，让AI检测系统难以区分

### 网络层优化与混淆
* **智能代理管理**：支持HTTP/SOCKS5/SSH隧道混合使用，提供自动代理健康检查和故障转移机制
* **请求时序优化**：基于马尔可夫链模型生成自然的请求间隔和时序模式
* **协议特征微调**：精细调整TCP参数、TLS握手行为和HTTP/2帧特征，减少与真实浏览器的差异

### 智能请求链生成
* **上下文感知爬取**：根据目标页面内容自动构建合理的前置请求链，模拟用户的自然浏览路径
* **资源请求模拟**：自动加载页面关联的CSS、JavaScript和图片资源，生成完整的浏览行为图谱
* **会话状态管理**：智能维护Cookie和会话信息，避免常见的会话异常模式

### 元认知系统
* **自我感知能力**：实时监控爬虫行为模式、成功率和响应特征，建立行为-结果映射模型
* **环境适应性**：自动检测网站反爬策略变化，动态调整指纹和行为参数，实现对反爬机制的自适应
* **学习优化机制**：基于历史爬取数据和成功/失败经验，使用强化学习算法持续优化爬取策略
* **智能故障恢复**：在检测到被封锁或识别时，自动触发备用策略，包括切换指纹、调整行为模式和使用不同的爬取路径

## 🚀 架构设计与性能

PhantomCrawler 采用模块化设计，将反爬技术、核心爬取逻辑和元认知系统分离，既保证了高度的可扩展性，又提供了优秀的性能表现，同时实现了零成本部署：

* **双引擎架构**：同时支持轻量级的httpx引擎（适用于简单页面）和全功能的playwright引擎（适用于复杂的JavaScript渲染页面）
* **异步并发处理**：基于Python 3.8+的asyncio实现高效并发，在保证隐匿性的同时最大化爬取效率
* **内存管理优化**：针对长时间运行的爬虫任务进行了内存泄漏防护和资源回收优化，即使在普通个人电脑或GitHub Actions环境中也能稳定运行
* **可观测性设计**：内置详细的日志系统和指标收集，方便监控爬虫状态和问题排查
* **零依赖硬件配置**：无需专业服务器，普通笔记本、台式机或免费云服务环境即可满足运行需求
* **资源自适应**：智能检测运行环境资源限制，自动调整并发数和内存使用策略
* **元认知架构**：采用分层设计，将感知层、决策层和执行层分离，支持复杂的自适应决策

## 💻 快速上手

### 基本爬取示例
```python
from src.core.crawler import PhantomCrawler

# 创建爬虫实例
crawler = PhantomCrawler()

# 初始化并执行爬取
if crawler.initialize():
    # 爬取单个URL
    result = crawler.crawl("https://target-website.com")
    print(f"爬取成功，状态码: {result['status_code']}")
    
    # 批量爬取示例
    urls = ["https://page1.com", "https://page2.com"]
    batch_results = crawler.crawl_batch(urls, max_concurrent=2)
    
    # 关闭爬虫释放资源
    crawler.close()
```

### 高级配置
```python
from src.config import global_config

# 配置隐匿模式
global_config.set('fingerprint.enable_dynamic_ua', True)
global_config.set('fingerprint.enable_ja3_simulation', True)

# 优化行为模拟
global_config.set('behavior_simulation.enable_human_delay', True)
global_config.set('behavior_simulation.use_gamma_distribution', True)
global_config.set('behavior_simulation.delay_min', 1.2)  # 最小延迟1.2秒
global_config.set('behavior_simulation.delay_max', 4.5)  # 最大延迟4.5秒

# 启用元认知系统（强烈推荐）
global_config.set('metacognition.enabled', True)
global_config.set('metacognition.memory_size', 1000)  # 历史记录容量
global_config.set('metacognition.learning_rate', 0.1)  # 学习率
global_config.set('metacognition.adaptation_threshold', 0.7)  # 策略调整阈值

# 配置代理
proxies = [
    {'type': 'http', 'host': 'proxy1.example.com', 'port': 8080},
    {'type': 'socks5', 'host': 'proxy2.example.com', 'port': 1080}
]
global_config.set('proxy_chain', proxies)
```

## 📊 实际应用场景

PhantomCrawler 在各种真实业务场景中表现出色：

* **电商数据采集**：绕过各大电商平台的严格反爬，稳定获取产品信息、价格和库存数据
* **金融信息监控**：从金融网站安全获取市场数据、公司公告和经济指标
* **内容聚合与分析**：从新闻、社交媒体和博客平台采集内容，用于舆情分析和内容推荐
* **SEO与竞争对手分析**：模拟真实用户访问，收集SEO数据和竞争对手网站信息
* **学术研究**：在获得适当授权的情况下，进行大规模数据挖掘和网络行为研究

## 🛡️ 负责任的使用指南

PhantomCrawler 设计用于合法的数据采集场景。作为负责任的开发者，请确保：

* 遵守目标网站的robots.txt规则和服务条款
* 仅在获得必要授权的情况下爬取受版权保护的内容
* 控制爬取频率，避免对目标服务器造成过大负载
* 尊重用户隐私，不采集或滥用个人身份信息

不当使用可能违反法律法规，用户需自行承担相关责任。

## 📚 深入学习

* [反侦测战术手册](./docs/反侦测战术手册.md) - 深入了解爬虫与反爬的技术对抗
* [红队行动指南](./docs/红队行动指南.md) - 针对特定网站的爬取策略和实战技巧
* [蓝队防御指南](./docs/蓝队防御指南.md) - 了解网站如何防御爬虫，知己知彼

## 🆓 零成本实战方案

PhantomCrawler 不仅支持本地运行，还可以通过以下白嫖级资源组合拳实现完全零成本部署和运行：

### 白嫖级资源组合拳：

**云服务 ：GitHub Actions免费额度 + Vercel/Netlify边缘函数**
- GitHub Actions每月提供2000分钟免费运行时间，足以应对中小规模爬取任务
- Vercel和Netlify的边缘函数提供全球分布式执行环境，可用于代理中转和任务调度
- 完美支持无服务器架构，按需执行，无需维护常驻服务器

**代理池 ：公开免费代理筛选 + Tor网络混用 + 临时VPS试用券**
- PhantomCrawler内置免费代理自动筛选模块，定期测试并更新可用代理列表
- 集成Tor网络支持，提供额外的匿名性和IP轮换能力
- 智能利用各大云服务商的临时VPS试用资源，进一步扩展IP池

**指纹库 ：社区共享指纹池 + 自动生成算法 = 无限轮换**
- 接入开源浏览器指纹库，定期更新主流浏览器的最新指纹特征
- 内置智能指纹生成算法，可动态生成符合特定浏览器特征的新指纹
- 支持指纹自动测试和评分系统，确保生成的指纹具有较高的真实性

**存储 ：GitHub LFS + 对象存储免费额度**
- 利用GitHub LFS存储爬取结果和配置文件，免费额度可达1GB
- 支持自动同步到各大云服务商的免费对象存储（如AWS S3 5GB免费额度、阿里云OSS 10GB免费额度）
- 内置增量存储策略，优化存储空间使用

### 部署示例

将PhantomCrawler与GitHub Actions结合，实现完全自动化的零成本爬取流水线：

```yaml
# .github/workflows/crawler.yml 示例配置
name: PhantomCrawler

on:
  schedule:
    - cron: '0 0 * * *'  # 每天运行一次
  workflow_dispatch:      # 支持手动触发

jobs:
  crawl:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run crawler
        run: python examples/basic_usage.py
      - name: Save results
        uses: actions/upload-artifact@v3
        with:
          name: crawl-results
          path: results/
```

通过这种组合，你可以在不花费一分钱的情况下，获得接近专业爬虫系统的功能和性能。

## 💻 本地运行指南

如果你不想使用云服务，PhantomCrawler 也可以直接在你的个人电脑上运行：

```bash
# 在你自己的电脑上安装依赖
pip install -r requirements.txt

# 直接运行示例
python examples/basic_usage.py
```

即使在个人电脑上运行，PhantomCrawler 内置的指纹模拟和行为仿真技术也能提供出色的反爬效果，无需配置代理服务器。

## 🔄 持续进化

网络环境和反爬技术在不断变化，PhantomCrawler团队也在持续更新框架。我们密切关注最新的反爬技术趋势，并定期发布更新，帮助用户应对新的挑战。

---

PhantomCrawler - 专业级反爬解决方案，让数据采集不再困难。

© 2023 PhantomCrawler. 保留所有权利。