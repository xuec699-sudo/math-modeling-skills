# Documents 插件交互式论文构建指南

本文档说明如何使用 Codex Documents 插件以交互式方式构建数模竞赛论文。
这是对旧 `build_docx.py` 单体脚本方式的替代，速度提升 3-5 倍。

---

## 核心原则：分节构建 + 即时渲染

**不要一次性写完整篇论文再检查。** 而是：

```
写一节 → 渲染PNG → 查看效果 → 通过则继续，有问题则立即修复该节
```

这避免了旧方式的根本问题：写完 200+ 行脚本后发现格式全错，只能重写。

---

## 准备工作

### 1. 确认 Documents 插件可用

```python
# 测试 python-docx 可用性
from docx import Document
doc = Document()
doc.save("test.docx")
print("OK")
```

### 2. 确认渲染链可用

```bash
python render_docx.py test.docx --output_dir ./qa/
# 检查 qa/page-1.png 是否生成
```

如果渲染失败，参见 Documents 插件 `troubleshooting/` 目录。

### 3. 加载竞赛模板

```python
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

doc = Document("templates/51mcm_template.docx")
```

模板已预设好页面边距、默认字体、段落样式。只需填充内容，格式从模板继承。

---

## 阶段 1：标题页 + 摘要（页面 1-2）

### 设置论文题目

```python
# 定位模板中的题目段落并替换
title_para = doc.paragraphs[0]  # 假设模板第一段是题目位
title_para.clear()
title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title_para.add_run("C题：边坡预警问题数学模型研究")
run.font.name = "黑体"
run._element.rPr.rFonts.set(qn("w:eastAsia"), "黑体")
run.font.size = Pt(16)
run.font.bold = True
```

### 设置摘要

```python
# "摘要" 标题
abs_title = doc.add_paragraph()
run = abs_title.add_run("摘要")
run.font.name = "黑体"
run._element.rPr.rFonts.set(qn("w:eastAsia"), "黑体")
run.font.size = Pt(14)
run.font.bold = True

# 摘要正文
abs_body = doc.add_paragraph()
abs_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
abs_body.paragraph_format.first_line_indent = Cm(0.74)  # ~2字符
run = abs_body.add_run("本文针对边坡预警问题，建立了...")
run.font.name = "宋体"
run._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
run.font.size = Pt(12)
```

### 第一次渲染检查

```bash
python render_docx.py output/论文.docx --output_dir output/qa/
```

打开 `output/qa/page-1.png` 和 `page-2.png`，确认：
- 题目居中、黑体三号
- 摘要标题黑体四号
- 摘要正文宋体小四、首行缩进

---

## 阶段 2：问题重述 + 问题分析

```python
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

# 一级标题
h1 = doc.add_paragraph()
h1.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = h1.add_run("一、问题重述")
run.font.name = "黑体"
run._element.rPr.rFonts.set(qn("w:eastAsia"), "黑体")
run.font.size = Pt(14)
run.font.bold = True

# 正文段落（可封装为函数）
def add_body(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = Cm(0.74)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run(text)
    run.font.name = "宋体"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
    run.font.size = Pt(12)
    return p

add_body(doc, "边坡稳定性预警是地质灾害防治中的关键问题...")
```

渲染检查后继续。

---

## 阶段 3：模型建立与求解（每个子问题）

### 子问题结构模板

```
4.x.1 模型建立
  P1: 问题定位（要解决什么 + 为什么难）
  P2: 建模思路（选什么方法 + 为什么）
  P3: 数学推导（完整公式 + 变量解释）
  P4: 方法优势与假设

4.x.2 模型求解与结果分析
  P1: 求解过程（如何求解 + 参数选择依据）
  P2: 核心结果（数字 + 含义）
  P3: 交叉验证/鲁棒性（指标 + 含义）
  P4: 物理/工程解释

[插入图表 + 图表说明文字]
```

### 插入 OMML 公式

```python
from scripts.build_docx import build_omath, _mr, om_sub, om_frac, om_sum

# 构建公式
omath = build_omath(
    _mr("F_"), om_sub("s", "安全"), _mr(" = "),
    om_frac(_mr("R"), _mr("S"))
)

# 插入到段落中
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run()
run._element.append(omath)
```

### 插入三线表

```python
from scripts.build_docx import add_three_line_table

table = add_three_line_table(
    doc,
    headers=["参数", "含义", "取值"],
    rows=[
        ["c", "黏聚力 (kPa)", "25.0"],
        ["φ", "内摩擦角 (°)", "30.0"],
        ["γ", "重度 (kN/m³)", "18.5"],
    ],
    caption="表2  边坡岩土力学参数"
)
```

### 插入图片

```python
from docx.shared import Inches

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run()
run.add_picture("latex/images/fig1_calibration.png", width=Inches(5.5))

# 图题
cap = doc.add_paragraph()
cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = cap.add_run("图1  边坡位移监测数据标定结果")
run.font.name = "黑体"
run._element.rPr.rFonts.set(qn("w:eastAsia"), "黑体")
run.font.size = Pt(10.5)
run.font.bold = True
```

**每张图/表后必须有说明段落**（nature-writing 标准）。

---

## 阶段 4：参考文献 + 附录

```python
# 参考文献标题
h1 = doc.add_paragraph()
h1.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = h1.add_run("参考文献")
run.font.name = "黑体"
run._element.rPr.rFonts.set(qn("w:eastAsia"), "黑体")
run.font.size = Pt(14)
run.font.bold = True

# 参考文献条目
refs = [
    "[1] Duncan J M. State of the art: limit equilibrium and finite-element analysis of slopes. Journal of Geotechnical Engineering, 1996, 122(7): 577-596.",
    "[2] 陈祖煜. 土质边坡稳定分析——原理·方法·程序. 北京: 中国水利水电出版社, 2003.",
]
for ref in refs:
    p = doc.add_paragraph()
    run = p.add_run(ref)
    run.font.name = "宋体"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
    run.font.size = Pt(12)
```

---

## 阶段 5：最终渲染 QA

```bash
python render_docx.py output/论文.docx --output_dir output/qa/ --emit_pdf
```

### 逐页检查清单

打开所有 `output/qa/page-<N>.png`（100% 缩放），逐页确认：

| 检查项 | 标准 |
|--------|------|
| 字体 | 标题黑体、正文宋体、数字Times New Roman |
| 字号 | 标题三号、一级四号、正文小四、表格五号 |
| 对齐 | 标题居中、正文两端对齐、表格居中 |
| 三线表 | 顶线1.5pt、表头下0.5pt、底线1.5pt、无竖线 |
| 公式 | OMML渲染正常、居中、编号右对齐 |
| 图片 | 清晰无模糊、图题黑体五号居中 |
| 行距 | 单倍行距、首行缩进2字符 |
| 页码 | 无页眉页脚、页数不超过30页 |
| 内容完整 | 所有章节按序出现、无遗漏 |

### 发现问题时

1. 修改对应段的 python-docx 代码
2. 重新运行渲染
3. 再次检查该页 PNG
4. 重复直到通过

---

## 最终交付

```python
doc.save("output/论文-C题-xxx.docx")
```

```bash
# 可选：转换为 PDF 提交格式
python render_docx.py output/论文-C题-xxx.docx --output_dir output/ --emit_pdf
```

### 交付前最终确认

- [ ] 所有页面 PNG 检查通过
- [ ] `quality_gate.py` 格式检测通过
- [ ] 字数符合要求（摘要 ≤ 1页，正文 ≤ 30页）
- [ ] 无裸露数字、无孤图、无黑箱跳跃
- [ ] 参考文献 ≥ 2 条/子问题
- [ ] AI 声明在附录中

---

## 常见问题

### Q: 中文显示为方块？
设置 `run._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")`。

### Q: 三线表边框不对？
使用 `scripts/build_docx.py` 中的 `add_three_line_table()` 函数，不要手动设置表格边框。

### Q: 公式渲染不出来？
确保导入了 `build_omath` 和所有需要的 helper 函数。OMML 公式只能通过 `run._element.append(omath)` 方式插入，不能用 `run.text`。

### Q: 渲染出来的 PNG 有重影？
这是 LibreOffice headless 的已知问题，不影响实际 DOCX 文件。以 Word 中打开的效果为准做最终判断。

### Q: 渲染命令报错？
参见 Documents 插件的 `troubleshooting/libreoffice_headless.md`。