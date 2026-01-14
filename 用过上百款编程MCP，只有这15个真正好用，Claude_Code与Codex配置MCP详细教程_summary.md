# 用过上百款编程MCP，只有这15个真正好用，Claude Code与Codex配置MCP详细教程

**Channel:** 技术爬爬虾  TechShrimp | **Duration:** 22 mins | **Date:** 2026/1/14

![Thumbnail](https://i.ytimg.com/vi/UW5iQGE3264/maxresdefault.jpg)

## Executive Summary
本期视频详细介绍了15款实用的编程类MCP（模型上下文协议）工具，并通过Cline和Cursor两个热门AI编程工具进行实战演示。MCP作为AI的标准化工具箱，使AI能够与外部系统交互，自动化完成各种任务。视频涵盖了从浏览器自动化、云端数据库操作、设计稿生成网页、产品配图生成、安全扫描到全自动部署等多个领域的MCP应用。具体演示了如何配置和使用这些MCP，包括Chrome DevTools MCP、Neon MCP、Supabase MCP、Figma MCP、Context.xyz MCP、Replicate MCP、Vercel MCP、GitLab MCP、Stripe MCP、shadcn/ui MCP、Semgrep MCP等，并通过实际案例展示了如何利用这些工具大幅提升开发效率。最后，视频还引导观众如何利用官方SDK创建自定义的MCP Server。

## Key Points
- **MCP核心概念**: MCP（模型上下文协议）是AI的标准化工具箱，允许AI与外部系统对话并代替人类执行操作，如操作浏览器、数据库等。
- **浏览器自动化工具**: Chrome DevTools MCP由Google官方开发，无需复杂配置，安装后即可让AI自动化操作Chrome浏览器，例如打开网页、搜索、点击、调试代码（获取网络请求、控制台日志等）。
- **云端数据库集成**: Neon MCP（基于PostgreSQL）和Supabase MCP为AI提供了免费的云端数据库操作能力。AI可以执行SQL语句创建项目、表、插入数据，甚至结合Supabase的用户认证等功能快速构建完整的后端应用。
- **设计稿转代码**: Figma MCP允许AI读取Figma设计稿的结构和资源，并自动生成对应的网页代码，实现从设计到代码的一键转换，相似度可达90%。
- **知识更新与文档检索**: Context.xyz MCP和ReX MCP帮助AI查找最新的编程文档和知识（如Python 3.14的新特性），弥补大模型知识截止日期后的信息缺口。
- **AI生成产品配图**: Replicate MCP利用其API生成AI图片，可让AI在编写网页时自动生成并插入符合场景的配图，提升产品美观度和原型开发速度。
- **一键部署与平台管理**: Vercel MCP和Zeabur MCP（国内平台）允许AI将项目一键部署到对应的云平台。Vercel MCP还能用于查询项目列表等信息。Cloudflare也提供了多种MCP Server用于部署、监控、查询流量等。
- **代码仓库与协作集成**: GitLab MCP将AI连接到GitLab平台，使AI能够读取仓库、管理Issue、分析代码并自动创建Pull Request（PR），实现从问题发现到代码修复提交的全流程自动化。
- **支付功能集成**: Stripe MCP为AI接入了Stripe支付平台的能力，AI可以获取商品信息、价格，并编写前端支付页面，快速为产品集成支付功能。
- **UI组件库与安全扫描**: shadcn/ui MCP让AI能够自动查找并复制该组件库的代码到项目中。Semgrep MCP则提供静态安全扫描，帮助AI检查代码中的安全漏洞，内置超过5000条规则。
- **自定义MCP开发**: 视频最后指向GitHub上的MCP官方仓库，提供了多种语言的SDK，鼓励开发者创建属于自己的、更贴合特定需求的MCP Server。

## Chapters
- **00:00** - 引言与MCP概述: 介绍视频主题：15款好用的编程类MCP工具。解释MCP（模型上下文协议）是AI的标准化工具箱，能让AI操作外部系统。
- **00:00** - 浏览器自动化：Chrome DevTools MCP: 演示如何为Cline和Cursor配置Google官方的Chrome DevTools MCP，展示AI自动化操作浏览器（打开网页、搜索、点Star）和辅助调试代码（获取控制台日志、网络请求）的能力。
- **00:00** - 云端数据库：Neon MCP: 展示如何配置Neon MCP，让AI能够创建项目、执行SQL语句，将CSV数据存入云端数据库，赋予AI完整的数据库操作能力。
- **00:00** - 全栈后端：Supabase MCP: 演示配置Supabase MCP，AI利用其创建数据表、并结合其自带的用户认证功能，快速生成一个带有登录注册和后台数据库的完整Next.js应用。
- **00:00** - 设计转代码：Figma MCP: 讲解如何配置参数较多的Figma MCP，并演示AI根据Figma设计稿链接，自动下载资源并生成对应网页代码的过程，最终效果与设计稿高度相似。
- **00:00** - 知识更新：Context.xyz MCP: 展示配置Context.xyz MCP，帮助AI查找Python 3.14等新技术的文档，使其能够正确编写关于新特性（如T模板字符串）的代码。
- **00:00** - AI生成图片：Replicate MCP: 演示配置Replicate MCP，让AI在编写网页时调用其API生成配图（如为销售套餐页面生成6张匹配的图片），提升页面美观度。
- **00:00** - 项目部署：Vercel MCP: 展示配置Vercel MCP，实现AI一键将Next.js项目部署到Vercel平台，并演示其查询团队项目列表的附加功能。同时提及国内类似平台Zeabur。
- **00:00** - 代码协作：GitLab MCP: 演示配置GitLab MCP，实现AI自动读取GitLab Issue、修复代码（如修改不清晰的按钮样式）、并创建Pull Request提交修复的全流程自动化。
- **00:00** - 支付集成：Stripe MCP: 展示配置Stripe MCP，AI利用其获取商品目录和价格信息，编写支付页面，最终成功完成测试支付，为产品快速接入支付能力。
- **00:00** - UI组件与安全扫描: 简要介绍shadcn/ui MCP用于自动获取UI组件代码，以及Semgrep MCP用于对项目代码进行静态安全漏洞扫描。
- **00:00** - 创建自定义MCP与结尾: 引导观众前往GitHub MCP官方仓库，利用提供的SDK创建属于自己的MCP Server，强调自定义工具的重要性。视频结束致谢。

## Terminology
- **MCP (Model Context Protocol)**: 模型上下文协议，一种让AI能够与外部系统和服务进行标准化交互的协议，可视为AI的工具箱。
- **Cline**: 一款AI编程工具（视频中演示用的其中之一）。
- **Cursor**: 另一款热门的AI编程工具（视频中演示用的其中之一）。
- **Neon**: 一个基于PostgreSQL的免费云端数据库服务。
- **Supabase**: 一个开源的Firebase替代品，提供PostgreSQL数据库、身份验证、存储等后端服务。
- **Figma**: 一款流行的基于浏览器的UI/UX设计协作工具。
- **Context.xyz**: 一个提供文档检索服务的MCP，用于为AI补充最新知识。
- **Replicate**: 一个提供AI模型API的平台，可用于生成图像等。
- **Vercel**: 一个专注于前端框架（如Next.js）的云部署平台。
- **Zeabur**: 一个国内的云部署平台（类似Vercel）。
- **GitLab**: 一个基于Git的代码仓库管理和DevOps生命周期平台。
- **Stripe**: 一个在线支付处理服务平台。
- **shadcn/ui**: 一个可复制粘贴代码的高质量UI组件库。
- **Semgrep**: 一个用于静态代码分析、寻找安全漏洞和代码问题的工具。
- **PR (Pull Request)**: 拉取请求，在Git协作中用于提议将代码更改合并到主分支。
- **SDK (Software Development Kit)**: 软件开发工具包，用于创建特定类型软件的一组工具。
