
[🇬🇧 English](README.md) | [🇮🇷 فارسی](README.fa.md) | [🇸🇦 العربية](README.ar.md) | [🇨🇳 简体中文](README.zh-CN.md)

---
# AS-LMS — 学习管理系统

**AS-LMS** 是一款桌面学习管理应用，使用 Python、Tkinter 图形界面和 MySQL 数据库开发。

系统为管理员、教师和学生提供不同的操作界面，支持用户管理、课程管理、作业管理、作业提交、成绩评定和教学反馈等功能。

## 功能特点

### 系统管理员
- 管理用户账户及用户角色。
- 管理教学课程。
- 管理学生的课程注册信息。
- 管理学生与教师之间的指导关系。

### 教师
- 使用教师操作界面。
- 管理课程作业。
- 设置作业说明、最高分数和截止时间。
- 查看学生提交的作业。
- 评定作业成绩并提供反馈。

### 学生
- 查看已注册课程和分配的作业。
- 查看作业详情及截止时间。
- 提交作业内容或答案。
- 查看成绩和教师反馈。

## 技术栈

- **编程语言：** Python
- **图形界面：** Tkinter 和 ttk
- **数据库：** MySQL
- **数据库连接器：** MySQL Connector/Python
- **密码哈希：** SHA-256

## 运行环境

- Windows 10 或 Windows 11
- Python 3.10 或兼容版本
- MySQL Server
- pip

## 项目结构

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

实际仓库中的文件可能与上述示例略有不同。

## 安装与配置

### 1. 获取项目

运行以下命令克隆仓库：

```bash
git clone https://github.com/ArshamScode/AS-LMS.git
cd AS-LMS
```

你也可以在 GitHub 中选择 **Code → Download ZIP**，下载并解压项目文件。

### 2. 创建 Python 虚拟环境

```bash
python -m venv .venv
```

在 Windows 中激活虚拟环境：

```bash
.venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置 MySQL 连接

确保已安装并启动 MySQL Server。

检查应用程序使用的数据库连接设置，通常位于 `model.py` 中。根据本地 MySQL 配置设置主机、端口、用户名、密码和数据库名称。

不要将真实数据库密码或其他机密信息提交到公开仓库。

### 5. 创建数据库表

打开 MySQL Workbench 或其他 MySQL 客户端，执行以下 SQL 文件：

```text
database/schema.sql
```

该文件用于创建应用程序所需的数据库和数据表，不会主动删除已有数据库。

### 6. 导入演示数据

创建数据表后，执行：

```text
database/seed.sql
```

该文件会添加演示账户、一个示例课程、课程注册信息和一项示例作业。

建议只在新建的演示数据库中执行一次。重复执行可能因重复数据而产生错误。

### 7. 启动应用程序

在项目根目录运行：

```bash
python main.py
```

## 演示账户

成功执行 `database/seed.sql` 后，可以使用以下账户体验不同角色的功能。

**所有演示账户的密码均为：** `password123`

| 角色 | 用户名 | 密码 |
|---|---|---|
| 系统管理员 | `admin` | `password123` |
| 教师 | `teacher1` | `password123` |
| 学生 | `student1` | `password123` |
| 学生 | `student2` | `password123` |

这些账户仅用于演示和测试。请勿将该示例密码用于真实账户或敏感数据。

## 数据库说明

数据库包含以下类别的数据表：

- 用户和角色
- 教师与学生之间的指导关系
- 课程和课程注册信息
- 作业及作业分配记录
- 学生提交的作业
- 成绩和教师反馈

SQL 文件分别提供数据库结构和演示数据，方便用户按需初始化数据库。

## 安全说明

- 演示账户使用相同的测试密码。
- 当前项目使用 SHA-256 对密码进行哈希处理。对于生产环境，建议使用专门为密码存储设计的算法，例如 Argon2id、scrypt 或 bcrypt，并采用适当的安全配置。
- 请在本地配置自己的 MySQL 连接信息。
- 不要将真实密码、API 密钥、私密配置文件或敏感用户数据提交到公开仓库。
- 在用于真实用户或生产数据之前，请先审查并充分测试项目。

## 常见问题排查

**MySQL 连接失败**
- 确认 MySQL Server 正在运行。
- 检查主机、端口、用户名和密码。
- 确认数据库已成功创建。

**缺少 Python 模块**
- 激活虚拟环境。
- 重新运行 `pip install -r requirements.txt`。

**无法使用演示账户登录**
- 确认 `database/seed.sql` 已成功执行。
- 确认应用程序与演示数据使用的是同一个数据库。
- 检查应用程序的密码哈希方式是否与数据库中存储的哈希值一致。

## 项目目标

AS-LMS 是一个桌面软件开发项目，展示了 Python 图形界面开发、MySQL 数据库集成、基于用户角色的界面设计，以及常见学习管理流程的实现方式。

## 开发者

**Arsham Sarmast**

GitHub：[@ArshamScode](https://github.com/ArshamScode)

## 许可证

目前该仓库尚未指定许可证。在添加明确的许可证之前，不应默认允许重新分发、修改或商业使用本项目。

---

如果你觉得这个项目有帮助，欢迎在 GitHub 上为仓库点亮 Star。
