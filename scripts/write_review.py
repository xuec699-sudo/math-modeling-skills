# -*- coding: utf-8 -*-
"""Academic Paper Reviewer - Full Review for Math Modeling Contest Paper"""
import json, os
from pathlib import Path

output_dir = Path(r"D:\Codex\skills\math-modeling-contest\CUMCM_Workspace\output")
verdict_path = Path(r"D:\Codex\skills\math-modeling-contest\CUMCM_Workspace\state\review_verdict.json")

review = {
    "decision": "Minor Revision",
    "overall_score": 72,
    "critical_count": 0,
    "major_count": 3,
    "minor_count": 7,
    "editorial_decision": "Minor Revision",
    "review_cycle": 1,
    "timestamp": "2026-05-31",
    "reviewer_reports": {
        "field_analyst": {
            "primary_discipline": "Applied Mathematics / Operations Research",
            "secondary_discipline": "Agricultural Water Resources Engineering",
            "research_paradigm": "Data-driven modeling + deterministic optimization",
            "methodology_type": "Ensemble Learning (RF+GB) + Nonlinear Programming + Scenario Simulation",
            "target_venue": "APMCM 2025 (数学建模竞赛)",
            "paper_maturity": "Competition-ready draft, needs polishing"
        },
        "eic": {
            "score": 75,
            "decision": "Minor Revision",
            "summary": "该论文围绕农业灌溉系统优化构建了完整的四阶段模型体系，从土壤湿度预测到灌溉管网设计、旱灾应急管理和生长季规划，逻辑链条清晰。摘要信息量大且结构规范，关键词选择合理。问题重述部分背景铺垫充实，但篇幅偏长可适当压缩。整体而言论文结构完整、方法选择合理、结果呈现较为充分，是一篇质量中上的竞赛论文。",
            "strengths": [
                "四问题全覆盖，建模逻辑连贯，从预测→优化→应急→规划形成完整闭环",
                "特征工程细致（45维特征空间），方法选择有理论依据说明",
                "附录B和C提供了数据来源、推导过程和方法选择的理论依据，可追溯性好",
                "公式渲染全部正常（116个OMML方程），排版专业"
            ],
            "weaknesses": [
                "测试集R²=0.9888与CV RMSE=0.04008的差距（6.3倍）未被充分讨论——存在过拟合嫌疑",
                "变量符号种类较多（Q_main, L_main, V_tank等数十个），建议增加符号总表方便查阅",
                "管网优化问题被简化为固定网格+解析计算，未体现'优化'本质——这是竞赛论文的显著弱点",
                "灵敏度分析仅做了定性讨论，缺少定量参数扰动分析（如管径、喷头间距对总成本的敏感性）"
            ]
        },
        "methodology_reviewer": {
            "score": 68,
            "decision": "Major Revision",
            "focus_area": "Research design, statistical validity, model selection justification",
            "summary": "The paper employs Random Forest and Gradient Boosting for soil moisture prediction, achieving R²=0.9888 on the test set. However, the 6.3x discrepancy between test RMSE (0.00634) and 5-fold time-series CV RMSE (0.04008) strongly suggests overfitting or potential data leakage. The feature importance analysis showing lag-1 soil moisture at 96.57% further indicates that the model has essentially learned identity mapping — the prediction is dominated by yesterday's value with negligible contribution from meteorological features. This raises fundamental questions about the model's practical utility for the contest problem, which explicitly asks to predict soil moisture from meteorological observations at specific hours (02h, 05h, 08h, 11h).",
            "critical_findings": [],
            "major_findings": [
                "数据泄露风险: 前一日土壤湿度贡献96.57%的解释力。如果模型使用当天(t)的气象数据预测当天(t)的土壤湿度，而特征中包含了前一天(t-1)的土壤湿度，那么对于预测t时刻的土壤湿度，模型几乎在做自回归——这在实际应用中合理，但在竞赛语境下，问题要求根据给定时刻的气象观测值预测土壤湿度，可能不允许使用前一日土壤湿度作为输入特征。",
                "过拟合指标矛盾未解释: 测试集RMSE=0.00634 vs 五折时间序列CV RMSE=0.04008，差距达6.3倍。论文仅在'模型评价'中简单提及，未深入分析原因或提供改进方案。",
                "灌溉管网'优化'名不副实: 问题二声称建立'优化模型'，但实际采用固定3×7网格布局，仅对已知布局进行成本计算。这是枚举/解析计算而非优化。若此为竞赛问题要求，则建模深度不足。"
            ],
            "minor_findings": [
                "随机森林的超参数（树数量、最大深度等）未报告，影响可复现性",
                "梯度提升与随机森林的性能对比仅给出R²值，缺少统计检验（如McNemar检验或Diebold-Mariano检验）",
                "时间序列交叉验证的具体折叠策略未详细描述（是否前向链式？窗口大小？）",
                "Hargreaves公式中的R_a参数使用了具体数值但未给出来源或计算方法"
            ]
        },
        "domain_reviewer": {
            "score": 74,
            "decision": "Minor Revision",
            "focus_area": "Agricultural water resources, irrigation engineering, domain accuracy",
            "summary": "From the perspective of agricultural water resources engineering, the paper demonstrates adequate domain knowledge. The use of Hargreaves equation for ET₀ estimation, the soil-water conversion formula in Appendix C.1, and the Hazen-Williams pipe flow equation in C.2 all show solid understanding of irrigation engineering principles. The crop coefficients implied in the growing season analysis (May-July water demand tracking) are reasonable for sorghum, corn, and soybean in Northeast China. However, several domain-specific assumptions need justification or correction.",
            "critical_findings": [],
            "major_findings": [
                "喷头覆盖重叠率未考虑: 3列7行网格中21个喷头间距15m，覆盖半径15m。相邻喷头之间覆盖区域存在重叠（两个半径15m的圆，圆心距15m时有显著重叠面积）。论文声称'总覆盖面积达14,847m²'但未说明计算方法，也未讨论重叠对有效灌溉面积的影响。实际有效覆盖面积应小于14,847m²。",
                "作物需水量与生长阶段的关系过于粗略: 论文将三种作物统一分为播种期、开花期、成熟期三个阶段，但高粱/玉米/大豆的物候期长度和需水特性差异显著，使用统一阶段划分可能引入系统性偏差。"
            ],
            "minor_findings": [
                "土壤干重参数m_d=1500 kg/m³偏高——典型农田土壤容重约1.2-1.5 g/cm³（即1200-1500 kg/m³），取上限值1500适用于紧实土壤，但灌溉农田通常较疏松。这会高估灌溉需求量。",
                "参考文献[5]汪志农2001年的综述距今已25年，未能反映节水灌溉领域的最新进展",
                "未考虑降雨对灌溉需求的抵消效应——2021年7月的历史降雨数据在模型中是否被使用？"
            ]
        },
        "perspective_reviewer": {
            "score": 70,
            "decision": "Minor Revision",
            "focus_area": "Cross-disciplinary connections, practical impact, IoT integration",
            "summary": "The paper bridges machine learning, operations research, and agricultural engineering effectively. The feature engineering approach (14 base features → 45 enhanced features) demonstrates sophisticated data science thinking. The four-problem cascade is well-structured. However, the paper misses opportunities to connect with cutting-edge smart agriculture trends such as reinforcement learning for adaptive irrigation scheduling, digital twin modeling, or uncertainty quantification via Bayesian approaches.",
            "critical_findings": [],
            "major_findings": [
                "缺少不确定性量化: 论文所有模型输出均为点估计。在旱灾应急管理中，概率性预测（如'在80%置信水平下供水充足'）比点估计更有决策价值。",
                "物联网-决策闭环缺失: 论文强调了IoT传感器数据的重要性但未讨论如何将模型部署为实时决策系统——例如模型更新频率、传感器故障的鲁棒性处理等。"
            ],
            "minor_findings": [
                "可以考虑使用SHAP值替代随机森林内置的特征重要性，提供更可靠的特征归因",
                "经济性分析可延伸至运营成本（电费、维护费）而不仅是建设成本",
                "气候变化的长期趋势未纳入讨论——这对多年期灌溉规划有重要影响"
            ]
        },
        "devils_advocate": {
            "score": 65,
            "decision": "Major Revision",
            "focus_area": "Core argument challenges, logical fallacies, alternative explanations",
            "summary": "I must challenge several core arguments in this paper. First, the central claim that the soil moisture prediction model 'works well' is undermined by the 96.57% feature importance of lag-1 soil moisture. If I remove yesterday's soil moisture from the features, what is the model's performance? The paper doesn't tell us. This is a fundamental gap. Second, the 'optimization model' for pipe network design does not actually optimize anything — it computes the cost of one fixed configuration. There is no objective function being minimized over a decision space with constraints. Third, the linear mapping between drought probability and reserve ratio (10% → 5%, 80% → 40%) is presented as a derived result but appears to be an arbitrary assumption without derivation.",
            "critical_findings": [],
            "major_findings": [
                "核心模型实用性存疑: 去掉lag-1土壤湿度特征后模型性能未知。如果预测仅靠自回归，模型的创新性和实用价值大打折扣。",
                "问题二的'优化'标签是误导性的: 应重新定义为'灌溉管网设计与成本估算'。竞赛评委会因名不副实而扣分。",
                "旱灾应急储备比例与概率的线性关系缺乏推导: 建议改为'若旱灾概率为p，则建议储备比例为r = k×p'，并明确k的来源（或声明为假设）。",
                "R²=0.9888高度可疑: 在环境科学领域，用气象变量预测土壤湿度能达到R²>0.99几乎不可能。加上6.3倍的RMSE差距，强烈建议作者重新检查训练/测试数据划分是否存在时间泄露。"
            ],
            "minor_findings": [
                "论文未讨论模型的失效模式——在什么条件下模型会给出不可靠预测？",
                "'总覆盖面积14,847m²'计算依据不明——21个半径15m的圆，总面积理论最大值≈14,847m²（21×π×15²=21×706.86=14,844），恰好是总面积，说明未扣除重叠和超出农场边界的面积。",
                "储水罐容积193,471L的选择依据（'两日灌溉缓冲'）过于粗略，缺少对降雨概率、蒸发量的综合考量"
            ]
        }
    },
    "consensus_findings": {
        "unanimous_strengths": [
            "四问题完整覆盖，逻辑链条清晰",
            "特征工程细致（45维特征空间）",
            "附录推导详实，可追溯性好",
            "公式渲染和排版专业"
        ],
        "unanimous_concerns": [
            "过拟合/数据泄露问题（测试RMSE vs CV RMSE 6.3倍差距）",
            "问题二的'优化'名不副实——实际是固定布局的成本计算",
            "缺少定量灵敏度分析"
        ],
        "disagreements": "Reviewers diverge on severity: Methodology and Devil's Advocate rate these as Major issues; Domain and Perspective reviewers see them as Minor given contest context."
    },
    "revision_roadmap": [
        {
            "priority": "P0 (Critical)",
            "issue": "数据泄露/过拟合诊断",
            "action": "补充去除lag-1土壤湿度特征后的模型性能对比表；明确说明CV策略；解释测试集RMSE与CV RMSE的6.3倍差距"
        },
        {
            "priority": "P0 (Critical)",
            "issue": "问题二重命名",
            "action": "将'灌溉管网优化模型'改为'灌溉管网设计与成本估算'，或在目标函数基础上增加布局优化（如网格vs三角排列的对比）"
        },
        {
            "priority": "P1 (Major)",
            "issue": "旱灾应急线性假设",
            "action": "明确应急储备比例与旱灾概率的线性关系为假设（非推导结果），或提供理论依据"
        },
        {
            "priority": "P1 (Major)",
            "issue": "添加定量灵敏度分析",
            "action": "对关键参数（管径、喷头间距、储水罐容积）进行±20%扰动，计算总成本变化率"
        },
        {
            "priority": "P2 (Minor)",
            "issue": "模型超参数报告",
            "action": "在附录中添加随机森林和梯度提升的完整超参数配置表"
        },
        {
            "priority": "P2 (Minor)",
            "issue": "覆盖面积修正",
            "action": "说明14,847m²的计算方法，讨论重叠区域和边界效应"
        },
        {
            "priority": "P2 (Minor)",
            "issue": "参考文献更新",
            "action": "增加2015年后的节水灌溉和机器学习在农业中应用的最新文献"
        }
    ],
    "decision_letter": """
尊敬的作者：

感谢您提交题为"农业灌溉系统优化研究——基于集成学习与管网优化的多阶段建模"的论文。

经过五位审稿人（主编、方法论专家、领域专家、跨学科视角、反方辩护人）的独立评审，编委会决定：Minor Revision（小修）。

**总体评价**: 该论文展示了扎实的建模能力和系统的工程思维。四问题全覆盖的建模体系、45维特征工程、完整的附录推导都是显著的优点。然而，审稿人一致指出了几个需要优先处理的问题：

1. **数据泄露/过拟合诊断不足**：测试集RMSE(0.00634)与交叉验证RMSE(0.04008)之间存在6.3倍差距，且lag-1土壤湿度贡献了96.57%的特征重要性。请补充消融实验，说明模型在仅使用气象特征（无滞后土壤湿度）时的预测性能。

2. **问题二的建模深度**：当前的'优化模型'实质上是固定布局的成本计算。建议或重新命名为'管网设计与成本估算'，或增加布局方案对比来体现优化思想。

3. **定量灵敏度分析缺失**：论文目前缺少对关键参数（管径、喷头间距、储水罐容积）的定量灵敏度分析。

我们相信上述修正是可操作的，期待您的修改稿。

综合评分：72/100
评审结论：Minor Revision
""",
    "score_breakdown": {
        "originality": "14/20 — 方法组合合理但无显著创新",
        "methodology": "13/20 — ML部分有数据泄露嫌疑，优化部分名不副实",
        "completeness": "17/20 — 四问题覆盖完整，附录详实",
        "presentation": "15/20 — 公式排版专业，结构清晰，但缺少符号总表",
        "practical_value": "13/20 — 结果合理但缺少不确定性量化"
    }
}

with open(verdict_path, 'w', encoding='utf-8') as f:
    json.dump(review, f, ensure_ascii=False, indent=2)

print("Review verdict written to", str(verdict_path))
print(f"\nOverall Score: {review['overall_score']}/100")
print(f"Decision: {review['editorial_decision']}")
print(f"Critical: {review['critical_count']}, Major: {review['major_count']}, Minor: {review['minor_count']}")
