[🇬🇧 English](README.md) | [🇮🇷 فارسی](README.fa.md) | [🇸🇦 العربية](README.ar.md) | [🇨🇳 简体中文](README.zh-CN.md)

---

# AS-LMS — 学习管理系统

AS-LMS 是一个使用 Python、Tkinter 和 MySQL 开发的桌面学习管理系统。它为管理员、教师和学生提供独立的操作界面，用于管理课程、作业、作业提交、成绩以及教学反馈。

## 功能特性

### 管理员
- 管理用户账户和角色。
- 管理课程以及课程选课信息。
- 建立适当的教师与学生之间的教学关系。
- 管理教师与学生之间的指导关系。

### 教师
- 访问教师操作界面。
- 管理课程作业。
- 设置作业描述、最高分和截止日期。
- 查看学生提交的作业。
- 批改作业并提供反馈。

### 学生
- 访问已选课程和分配给自己的作业。
- 查看作业详情和截止日期。
- 提交作业内容。
- 查看成绩和教师反馈。

## 技术栈

- **编程语言：** Python
- **图形用户界面：** Tkinter 和 ttk
- **数据库：** MySQL
- **数据库连接器：** MySQL Connector/Python
- **密码哈希：** 当前实现使用 SHA-256

## 系统要求

- Windows 10 或 Windows 11
- Python 3.10 或兼容版本
- MySQL Server
- pip

## 项目结构

以下结构仅为示例，实际仓库中的文件可能与此不同。

```text
AS-LMS/
├── main.py
├── view.py
├── controller.py
├── model.py
├── style.py
├── requirements.txt
├── .gitignore
├── .env.example
├── help.txt
├── database/
│   ├── schema.sql
│   └── seed.sql
└── README.md
```

## 安装与配置

### 1. 获取项目

克隆仓库：

```bash
git clone https://github.com/ArshamScode/AS-LMS.git
cd AS-LMS
```

也可以在 GitHub 上选择 **Code → Download ZIP**，然后解压下载的压缩包。

### 2. 创建虚拟环境

```bash
python -m venv .venv
```

在 Windows 上激活虚拟环境：

```bat
.venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置 MySQL

确保 MySQL Server 已安装并正在运行。

根据本地 MySQL 环境配置数据库主机、端口、用户名、密码和数据库名称。请检查应用程序实际使用的数据库连接设置，这些设置通常位于 `model.py` 中。

不要将真实的数据库密码或其他私密凭据提交到公开仓库。

### 5. 创建数据库表

如果仓库中存在 `database/schema.sql`，请打开 MySQL Workbench 或其他 MySQL 客户端并执行该脚本，以创建数据库结构。

执行前请检查 SQL 脚本的内容，确认它不会删除或覆盖包含重要数据的数据库。

### 6. 插入演示数据

如果仓库中存在 `database/seed.sql`，请在创建数据库结构后执行该脚本，以插入演示数据。

仅在适当的情况下运行演示数据脚本。如果脚本没有专门设计为可重复执行，多次运行可能导致重复记录或其他数据库问题。

### 7. 运行应用程序

在项目目录中执行：

```bash
python main.py
```

## 演示登录账号

以下演示账号用于本地测试。只有在数据库中已经创建对应的账号记录，并且密码哈希与应用程序的验证逻辑匹配时，这些账号才能正常使用。

**演示密码：** `password123`

| 角色 | 用户名 | 密码 |
|---|---|---|
| 管理员 | `admin` | `password123` |
| 教师 | `teacher1` | `password123` |
| 学生 | `student1` | `password123` |
| 学生 | `student2` | `password123` |

这些账号仅供本地测试和演示使用。请勿将示例密码用于真实账户或敏感信息。

## 数据库

数据库旨在支持学习管理系统的常见工作流程，包括：

- 用户和角色
- 教师与学生之间的指导关系
- 课程和选课记录
- 作业及作业分配
- 学生作业提交
- 成绩和反馈

请查看仓库中实际提供的 SQL 文件，以了解真实的数据库结构以及可用的演示数据。

## 安全说明

- 演示账号使用相同的示例密码。
- 当前实现使用 SHA-256 对密码进行哈希处理。对于生产环境中的密码存储，不建议单独使用 SHA-256。应使用专门为密码存储设计的算法，例如 Argon2id、scrypt 或 bcrypt，并进行适当配置。
- 请在本地配置自己的 MySQL 连接凭据。
- 不要将真实密码、API 密钥、私有配置文件或敏感用户数据提交到公开仓库。
- 执行 SQL 脚本前请先检查其内容，尤其是可能创建、删除或覆盖数据库和数据表的脚本。
- 在将项目用于真实用户或生产数据之前，请先进行审查和测试。

## 故障排查

**MySQL 连接错误**
- 确认 MySQL Server 正在运行。
- 检查应用程序数据库配置中的主机、端口、用户名和密码。
- 确认所需的数据库和数据表已经创建。

**找不到 Python 模块**
- 激活虚拟环境。
- 再次运行 `pip install -r requirements.txt`。
- 确认 `requirements.txt` 中列出了应用程序所需的依赖。

**演示账号无法登录**
- 确认数据库中存在相应的演示账号记录。
- 检查应用程序是否连接到包含这些记录的同一个数据库。
- 确认应用程序的密码哈希逻辑与数据库中存储的密码哈希一致。

## 项目目的

AS-LMS 是一个桌面软件项目，旨在展示 Python 图形界面开发、MySQL 集成、基于角色的用户界面以及常见学习管理工作流程的实现。

## 项目截图

### 登录界面

![AS-LMS 登录界面](docs/screenshots/login.png)

### 管理员仪表板

![AS-LMS 管理员仪表板](docs/screenshots/admin-dashboard.png)

### 教师仪表板

![AS-LMS 教师仪表板](docs/screenshots/teacher-dashboard.png)

### 学生仪表板

![AS-LMS 学生仪表板](docs/screenshots/student-dashboard.png)

如果图片无法显示，请检查图片文件是否存在于指定路径，并确认文件名及大小写与 Markdown 链接完全一致。

## 作者

**Arsham Sarmast**

GitHub：[@ArshamScode](https://github.com/ArshamScode)

## 许可证

AS-LMS 使用 MIT 许可证发布。完整的许可证条款请参阅 [LICENSE](LICENSE) 文件。

MIT 许可证允许使用、修改、分发本软件以及将其用于商业用途，但必须遵守许可证条款，包括保留版权声明和许可证文本。本软件按“现状”提供，不附带任何保证。详情请参阅 `LICENSE` 文件。

---

如果你觉得这个项目有帮助，欢迎在 GitHub 上为仓库点亮一颗星。
