#!/usr/bin/env python3
"""
Model Remediation Engine
Auto-detects model quality issues and suggests/executes fixes.
Called by the pipeline when quality_gate.model_quality fails.

Usage:
  python scripts/model_remediator.py diagnose --report-text "R2=0.07, pF=0.0001"
  python scripts/model_remediator.py remediate --model-file model_1.py --issue low_r2
"""

import re
import sys
from pathlib import Path


def diagnose_model(report_text: str) -> list[dict]:
    """Parse model output and identify quality issues."""
    issues = []

    # Check R-squared
    r2_match = re.search(r'R[²2]\s*[=:]\s*([0-9.]+)', report_text, re.IGNORECASE)
    if r2_match:
        r2 = float(r2_match.group(1))
        if r2 < 0.05:
            issues.append({
                "severity": "HARD_FAIL",
                "type": "low_r2",
                "value": r2,
                "threshold": 0.05,
                "fix": "Try nonlinear transforms (log, sqrt, Box-Cox), add interaction terms, or use mixed-effects model",
            })
        elif r2 < 0.15:
            issues.append({
                "severity": "SOFT_WARN",
                "type": "weak_r2",
                "value": r2,
                "threshold": 0.15,
                "fix": "Consider polynomial features, interaction terms, or nonlinear models. Explain limitation in paper.",
            })

    # Check CV R-squared
    cv_matches = re.findall(r'CV\s*R[²2]\s*[=:]\s*([-0-9.]+)', report_text, re.IGNORECASE)
    if cv_matches:
        cv_r2 = min(float(m) for m in cv_matches)  # use worst CV score
        if cv_r2 < -0.5:
            issues.append({
                "severity": "HARD_FAIL",
                "type": "cv_r2_negative",
                "value": cv_r2,
                "threshold": -0.5,
                "fix": "Model has NO predictive power. Do NOT use for prediction. Report honestly: grouping-based approach is recommended.",
            })

    # Check AUC
    auc_match = re.search(r'AUC\s*[=:]\s*([0-9.]+)', report_text, re.IGNORECASE)
    if auc_match:
        auc = float(auc_match.group(1))
        if auc < 0.60:
            issues.append({
                "severity": "HARD_FAIL",
                "type": "low_auc",
                "value": auc,
                "threshold": 0.60,
                "fix": "Try different algorithms, feature engineering, or class balancing (SMOTE).",
            })
        elif auc < 0.75:
            issues.append({
                "severity": "SOFT_WARN",
                "type": "weak_auc",
                "value": auc,
                "threshold": 0.75,
                "fix": "Acceptable but could improve. Consider hyperparameter tuning or additional features.",
            })

    # Check recall for classification
    recall_match = re.search(r'recall\s*[=:]\s*([0-9.]+)', report_text, re.IGNORECASE)
    if recall_match:
        recall = float(recall_match.group(1))
        if recall < 0.10:
            issues.append({
                "severity": "HARD_FAIL",
                "type": "low_recall",
                "value": recall,
                "threshold": 0.10,
                "fix": "Model misses too many positives. Lower probability threshold (e.g., 0.3 for screening) or use cost-sensitive learning.",
            })

    return issues


REMEDIATION_SCRIPTS = {
    "low_r2": """
# AUTO-REMEDIATION: Low R-squared fix
# 1. Try log transform on dependent variable
import numpy as np
y_log = np.log(y + 0.001)  # avoid log(0)

# 2. Add interaction terms
X['weeks_bmi'] = X['weeks'] * X['bmi']
X['weeks2'] = X['weeks'] ** 2
X['bmi2'] = X['bmi'] ** 2

# 3. Try polynomial regression
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)

# 4. Try mixed-effects if repeated measures exist
# import statsmodels.formula.api as smf
# model = smf.mixedlm("Y ~ weeks + bmi + age", data, groups=data["subject_id"])
""",

    "cv_r2_negative": """
# AUTO-REMEDIATION: CV R2 negative - model has no predictive power
# DO NOT use this model for prediction.
# RECOMMENDED: Switch to grouping-based approach (like Model 2)
# In paper: honestly state "multi-factor linear prediction is infeasible;
# BMI-based grouping provides the most reliable NIPT timing recommendation."
""",

    "low_auc": """
# AUTO-REMEDIATION: Low AUC fix
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

# 1. Try multiple algorithms
models = {
    'lr': LogisticRegression(class_weight='balanced', max_iter=2000),
    'rf': RandomForestClassifier(class_weight='balanced', n_estimators=200),
    'gb': GradientBoostingClassifier(n_estimators=100),
    'svm': SVC(kernel='rbf', class_weight='balanced', probability=True),
}

# 2. Try SMOTE for imbalanced data
from imblearn.over_sampling import SMOTE
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)
""",

    "low_recall": """
# AUTO-REMEDIATION: Low recall fix
# For screening applications, lower the threshold
probs = model.predict_proba(X_test)[:, 1]
for threshold in [0.2, 0.25, 0.3, 0.35, 0.4]:
    preds = (probs >= threshold).astype(int)
    from sklearn.metrics import recall_score
    rec = recall_score(y_test, preds)
    print(f"Threshold={threshold:.2f}, Recall={rec:.3f}")

# Use the threshold that gives recall >= 0.80 for screening
best_threshold = 0.3  # adjust based on results
""",
}


def print_remediation(issues: list[dict]):
    """Print remediation suggestions for each issue."""
    if not issues:
        print("[model_remediator] No issues found.")
        return

    print(f"[model_remediator] Found {len(issues)} issue(s):\n")
    for i, issue in enumerate(issues):
        sev_icon = "HARD_FAIL" if issue["severity"] == "HARD_FAIL" else "WARN"
        print(f"  [{sev_icon}] {issue['type']}: {issue.get('value', 'N/A')} "
              f"(threshold: {issue.get('threshold', 'N/A')})")
        print(f"         Fix: {issue['fix']}")
        if issue['type'] in REMEDIATION_SCRIPTS:
            print(f"         Remediation code available (use --action remediate)")
        print()

    hard_fails = [i for i in issues if i["severity"] == "HARD_FAIL"]
    if hard_fails:
        print(f"[model_remediator] {len(hard_fails)} HARD_FAIL(s) detected.")
        print("Pipeline MUST NOT advance until fixed or explicitly waived.\n")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Model Remediation Engine")
    p.add_argument("action", choices=["diagnose", "remediate"])
    p.add_argument("--report-text", default="", help="Model output text to analyze")
    p.add_argument("--issue", default="", help="Specific issue type to remediate")

    args = p.parse_args()

    if args.action == "diagnose":
        if args.report_text:
            issues = diagnose_model(args.report_text)
        else:
            # Read from stdin
            issues = diagnose_model(sys.stdin.read())
        print_remediation(issues)

    elif args.action == "remediate":
        if args.issue and args.issue in REMEDIATION_SCRIPTS:
            print(REMEDIATION_SCRIPTS[args.issue])
            print(f"\n# Apply the above code to fix: {args.issue}")
        else:
            print("Available remediations:")
            for k in REMEDIATION_SCRIPTS:
                print(f"  {k}")
