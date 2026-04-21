"""Generate a synthetic controls CSV for dummy data with seeded coarse-handoff patterns.

Output: data/input/dummy_controls.csv with columns
  Audit Entity ID, Control ID, Control Title, Control Description,
  KPA ID, KPA Description, Specific Risk ID, Specific Risk Description

Seeded scenarios:

  COARSE HANDOFF — AE-20 Customer Onboarding → AE-22 AML Monitoring
    AE-22 carries program-level AML SRs only (framework, training, monitoring
    calibration, SAR filing). Embedded KYC/CDD/EDD SRs are deliberately ABSENT.
    AE-21 KYC/CDD cleanly owns the embedded set. AE-20 does not retain them.
    Stage 2 Task 5 should detect: AE-20 transfers AML-related to AE-22 but
    AE-22's library has zero embedded coverage for SR-101/102/104.

  CLEAN MATCH — AE-9 Mortgage Origination → AE-38 Credit Risk Management
    Both carry embedded credit SRs (SR-110, SR-111). Task 5 should classify
    as conforms.

  VAGUE PROSE (dummy default) — AE-1 Consumer Lending
    Boilerplate handoff description. Exercises Task 5 step 1 thin-prose clause.

Restricted SRs (see SR_RESTRICTED) can ONLY land on entities whose name
matches one of the allowed keywords. Random fill cannot override.
Seeded assignments can — they are explicit.
"""
from __future__ import annotations

import argparse
import random
from collections import defaultdict
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "data" / "input" / "dummy_audit_universe_50.csv"
DEFAULT_OUTPUT = ROOT / "data" / "input" / "dummy_controls.csv"

KPAS: list[tuple[str, str]] = [
    ("KPA-001", "Customer Onboarding"),
    ("KPA-002", "Credit Origination"),
    ("KPA-003", "Transaction Processing"),
    ("KPA-004", "Payment Authorization"),
    ("KPA-005", "Account Servicing"),
    ("KPA-006", "Financial Reporting — Period Close"),
    ("KPA-007", "Financial Reporting — Consolidation"),
    ("KPA-008", "Vendor Due Diligence"),
    ("KPA-009", "Vendor Performance Monitoring"),
    ("KPA-010", "Access Management"),
    ("KPA-011", "Change Management"),
    ("KPA-012", "Model Development"),
    ("KPA-013", "Model Validation"),
    ("KPA-014", "Issue Management"),
    ("KPA-015", "Regulatory Reporting"),
    ("KPA-016", "AML Program Framework"),
    ("KPA-017", "AML Transaction Monitoring Calibration"),
    ("KPA-018", "Sanctions Program Oversight"),
    ("KPA-019", "Fraud Case Management"),
    ("KPA-020", "Training & Awareness"),
]

SRS: list[tuple[str, str, str, str]] = [
    ("SR-101", "Risk that KYC identity verification is not performed at customer onboarding", "KPA-001", "embedded"),
    ("SR-102", "Risk that Customer Due Diligence is not refreshed per policy cadence", "KPA-001", "embedded"),
    ("SR-103", "Risk that sanctions screening is not performed at customer onboarding", "KPA-001", "embedded"),
    ("SR-104", "Risk that enhanced due diligence is not completed for high-risk customers", "KPA-001", "embedded"),
    ("SR-105", "Risk that the AML program framework and policies are not maintained", "KPA-016", "program"),
    ("SR-106", "Risk that annual AML training is not delivered to in-scope staff", "KPA-020", "program"),
    ("SR-107", "Risk that transaction monitoring rules are not calibrated against typologies", "KPA-017", "program"),
    ("SR-108", "Risk that Suspicious Activity Reports are not filed within regulatory deadlines", "KPA-017", "program"),
    ("SR-109", "Risk that the sanctions screening program has inadequate list coverage", "KPA-018", "program"),
    ("SR-110", "Risk that credit decisioning criteria are not applied at origination", "KPA-002", "embedded"),
    ("SR-111", "Risk that credit limits are not approved per delegated authority", "KPA-002", "embedded"),
    ("SR-112", "Risk that payment instructions are not authorized before release", "KPA-004", "embedded"),
    ("SR-113", "Risk that daily payment reconciliations are not completed and reviewed", "KPA-004", "embedded"),
    ("SR-114", "Risk that period-end financial statements contain material misstatement", "KPA-006", "embedded"),
    ("SR-115", "Risk that intercompany eliminations are not applied during consolidation", "KPA-007", "embedded"),
    ("SR-116", "Risk that vendors are not onboarded per Third Party Risk policy", "KPA-008", "program"),
    ("SR-117", "Risk that vendor SLAs and performance are not monitored periodically", "KPA-009", "program"),
    ("SR-118", "Risk that production access is not provisioned per least-privilege policy", "KPA-010", "embedded"),
    ("SR-119", "Risk that user access is not recertified on the required cadence", "KPA-010", "embedded"),
    ("SR-120", "Risk that production changes are not approved before release", "KPA-011", "embedded"),
    ("SR-121", "Risk that emergency changes are not documented post-implementation", "KPA-011", "embedded"),
    ("SR-122", "Risk that models are not validated before production deployment", "KPA-013", "embedded"),
    ("SR-123", "Risk that model performance is not monitored against thresholds", "KPA-013", "program"),
    ("SR-124", "Risk that audit findings are not tracked to remediation", "KPA-014", "program"),
    ("SR-125", "Risk that regulatory reports are not filed by required deadlines", "KPA-015", "embedded"),
    ("SR-126", "Risk that fraud cases are not investigated and closed", "KPA-019", "embedded"),
    ("SR-127", "Risk that fraud trend reporting is not delivered to governance", "KPA-019", "program"),
    ("SR-128", "Risk that periodic entity-level risk assessments are not completed", "KPA-014", "program"),
    ("SR-129", "Risk that customer complaints are not logged and triaged", "KPA-005", "embedded"),
    ("SR-130", "Risk that customer data is not protected in transit and at rest", "KPA-010", "embedded"),
]

KPA_DESC = {kid: desc for kid, desc in KPAS}
SR_BY_ID = {sr[0]: sr for sr in SRS}

# Restricted SRs: only entities whose name contains one of the keywords below (case-insensitive)
# may carry the SR via random fill. Seeded assignments bypass this — they are explicit. Keywords
# define the business context in which the SR plausibly operates.
SR_RESTRICTED: dict[str, list[str]] = {
    "SR-101": ["Onboarding", "Consumer Lending", "Retail", "Branch", "Digital", "Mortgage", "Wealth", "KYC", "Private"],
    "SR-102": ["Onboarding", "Consumer Lending", "Retail", "Branch", "Digital", "Mortgage", "Wealth", "KYC", "Private"],
    "SR-103": ["Onboarding", "Consumer Lending", "Retail", "Branch", "Digital", "Mortgage", "Wealth", "KYC"],
    "SR-104": ["Onboarding", "Wealth", "Asset Management", "KYC", "Private"],
    "SR-110": ["Credit", "Consumer Lending", "Commercial", "Mortgage", "Merchant", "Trade Finance", "Investment"],
    "SR-111": ["Credit", "Consumer Lending", "Commercial", "Mortgage", "Merchant", "Trade Finance", "Investment"],
    "SR-112": ["Payment", "ACH", "Wire", "Treasury", "Card", "Merchant", "Branch", "ATM", "Foreign Exchange", "Capital", "Accounts Payable", "Payroll"],
    "SR-113": ["Payment", "ACH", "Wire", "Treasury", "Card", "Merchant", "Foreign Exchange", "Accounts Payable"],
    "SR-114": ["Financial Reporting", "General Ledger", "Accounts Payable", "Payroll", "Regulatory Reporting"],
    "SR-115": ["Financial Reporting", "General Ledger", "Treasury", "Consolidation"],
    "SR-122": ["Model"],
    "SR-123": ["Model"],
    "SR-125": ["Regulatory Reporting", "Financial Reporting"],
    "SR-126": ["Fraud", "Dispute", "Card"],
    "SR-127": ["Fraud"],
    "SR-129": ["Retail", "Branch", "Digital", "Consumer Lending", "Dispute", "Mortgage Servicing", "Onboarding", "Customer"],
}


def _entity_allows_sr(entity_name: str, sr_id: str) -> bool:
    if sr_id not in SR_RESTRICTED:
        return True
    n = entity_name.lower()
    return any(kw.lower() in n for kw in SR_RESTRICTED[sr_id])


def _control_for_sr(sr_id: str, serial: int) -> dict:
    _, sr_desc, kpa_id, tier = SR_BY_ID[sr_id]
    kpa_desc = KPA_DESC[kpa_id]
    if tier == "embedded":
        title = f"Operating control over {kpa_desc}"
        description = (
            f"Control operated within {kpa_desc}. Mitigates the risk: {sr_desc}. "
            "Evidence is retained per the control operator's workpapers and is "
            "executed at the transaction or event level."
        )
    else:
        title = f"Program-level oversight of {kpa_desc}"
        description = (
            f"Governance control providing oversight of {kpa_desc}. Mitigates the risk: {sr_desc}. "
            "Evidence is produced at the program or framework level and is reviewed by "
            "second-line governance on a defined cadence."
        )
    return {
        "Audit Entity ID": None,
        "Control ID": f"CTRL-{serial:04d}",
        "Control Title": title,
        "Control Description": description,
        "KPA ID": kpa_id,
        "KPA Description": kpa_desc,
        "Specific Risk ID": sr_id,
        "Specific Risk Description": sr_desc,
    }


# Seeded assignments bypass SR_RESTRICTED. They define the test scenarios.
SEEDED: dict[str, list[str]] = {
    "AE-20": ["SR-129", "SR-130", "SR-103"],            # customer complaints + data protection + sanctions at onboarding
    "AE-21": ["SR-101", "SR-102", "SR-103", "SR-104"],  # clean owner of embedded KYC/CDD/sanctions-at-onboarding/EDD
    "AE-22": ["SR-105", "SR-106", "SR-107", "SR-108", "SR-109"],  # program-level AML only; the seeded gap
    "AE-9":  ["SR-110", "SR-111"],                      # mortgage credit decisioning + limits
    "AE-38": ["SR-110", "SR-111", "SR-123", "SR-124"],  # credit oversight + model monitoring
    "AE-1":  ["SR-110", "SR-111", "SR-129"],            # consumer lending credit (no AML embedded — still leaky)
}

# Rough coverage of remaining entities by business-unit keyword. Only program-level SRs and
# broadly-carried embedded SRs (access, change, issue management) should appear here to avoid
# polluting the seeded scenarios via hints.
BU_SR_HINTS: list[tuple[str, list[str]]] = [
    ("Payment", ["SR-112", "SR-113"]),
    ("ACH", ["SR-112", "SR-113"]),
    ("Wire", ["SR-112", "SR-113"]),
    ("Card", ["SR-112", "SR-113", "SR-126"]),
    ("Treasury", ["SR-112", "SR-113", "SR-115"]),
    ("Merchant", ["SR-117", "SR-126"]),
    ("Financial Reporting", ["SR-114", "SR-115", "SR-125"]),
    ("Regulatory Reporting", ["SR-125", "SR-128"]),
    ("General Ledger", ["SR-114", "SR-115"]),
    ("Sanctions", ["SR-109"]),           # program-level sanctions oversight only
    ("Fraud", ["SR-126", "SR-127"]),
    ("Vendor", ["SR-116", "SR-117"]),
    ("Model", ["SR-122", "SR-123"]),
    ("Cyber", ["SR-118", "SR-119", "SR-130"]),
    ("IT", ["SR-118", "SR-119", "SR-120", "SR-121"]),
    ("Cloud", ["SR-118", "SR-120"]),
    ("Application Development", ["SR-120", "SR-121"]),
    ("Data Governance", ["SR-130", "SR-128"]),
    ("Compliance", ["SR-105", "SR-128", "SR-124"]),
    ("Internal Controls", ["SR-124", "SR-128"]),
    ("Operational Risk", ["SR-128", "SR-124"]),
    ("Market Risk", ["SR-122", "SR-123"]),
    ("Credit Risk", ["SR-123", "SR-124"]),   # program oversight only here; seeded handles SR-110/111
    ("HR", ["SR-106", "SR-119"]),
    ("Payroll", ["SR-114"]),
    ("Accounts Payable", ["SR-114"]),
    ("Issue", ["SR-124"]),
    ("Business Continuity", ["SR-128", "SR-124"]),
    ("Facilities", ["SR-118"]),
    ("Branch", ["SR-112"]),
    ("Digital", ["SR-118", "SR-130"]),
    ("ATM", ["SR-112", "SR-118"]),
    ("Retail", ["SR-112"]),
    ("Dispute", ["SR-126"]),
    ("Mortgage Servicing", ["SR-129"]),
    ("Asset Management", ["SR-117"]),
    ("Wealth", ["SR-117"]),
    ("Foreign Exchange", ["SR-112", "SR-113"]),
    ("Capital Markets", ["SR-122"]),
    ("Investment Banking", []),              # generic — random fill handles this
    ("Trade Finance", ["SR-109"]),
]


def _entity_srs(entity_id: str, entity_name: str, rng: random.Random) -> list[str]:
    # 1) Seeded set has absolute priority and bypasses restrictions.
    if entity_id in SEEDED:
        base = list(SEEDED[entity_id])
    else:
        base = []
        for keyword, hint_srs in BU_SR_HINTS:
            if keyword.lower() in entity_name.lower():
                for sr in hint_srs:
                    # Even BU hints must respect restrictions — the embedded SRs are business-specific.
                    if _entity_allows_sr(entity_name, sr):
                        base.append(sr)
        base = list(dict.fromkeys(base))  # dedup preserving order

    target_control_count = rng.randint(10, 30)
    control_srs: list[str] = []
    for sr in base:
        for _ in range(rng.randint(1, 3)):
            control_srs.append(sr)

    # Fill remainder: only SRs that either (a) aren't restricted or (b) match the entity's keywords.
    available = [
        s[0] for s in SRS
        if _entity_allows_sr(entity_name, s[0])
    ]
    # If an entity is in SEEDED, still hard-block forbidden SRs (preserve the coarse-handoff gap).
    if entity_id == "AE-22":
        available = [s for s in available if s not in {"SR-101", "SR-102", "SR-103", "SR-104"}]
    if entity_id == "AE-20":
        # AE-20 keeps SR-103 from seeded but must not sneakily gain SR-101/102/104 via fill.
        available = [s for s in available if s not in {"SR-101", "SR-102", "SR-104"}]
    if not available:
        available = [s[0] for s in SRS if SR_BY_ID[s[0]][3] == "program"]  # fallback to program-level
    while len(control_srs) < target_control_count:
        control_srs.append(rng.choice(available))
    return control_srs[:target_control_count]


def build(input_path: Path, output_path: Path, seed: int = 7) -> pd.DataFrame:
    df = pd.read_csv(input_path, dtype=str)
    active = df[(df["Audit Entity Type"] == "Audit") & (df["Audit Entity Status"] == "Active")].copy()
    rng = random.Random(seed)
    rows: list[dict] = []
    serial = 1
    for _, r in active.iterrows():
        eid = r["Audit Entity ID"]
        ename = r["Audit Entity Name"]
        srs_for_entity = _entity_srs(eid, ename, rng)
        for sr_id in srs_for_entity:
            rec = _control_for_sr(sr_id, serial)
            rec["Audit Entity ID"] = eid
            rows.append(rec)
            serial += 1
    out = pd.DataFrame(rows, columns=[
        "Audit Entity ID", "Control ID", "Control Title", "Control Description",
        "KPA ID", "KPA Description", "Specific Risk ID", "Specific Risk Description",
    ])
    out.to_csv(output_path, index=False)
    return out


def _sanity_check_seeded(df: pd.DataFrame, active_df: pd.DataFrame) -> str:
    """Print diagnostics showing whether each seeded scenario is distinguishable from noise."""
    name_by_id = dict(zip(active_df["Audit Entity ID"], active_df["Audit Entity Name"]))
    srs_by_entity: dict[str, set[str]] = {
        eid: set(sub["Specific Risk ID"]) for eid, sub in df.groupby("Audit Entity ID")
    }
    entity_count = df["Audit Entity ID"].nunique()
    lines: list[str] = []
    lines.append("[sanity] Seeded scenario diagnostics")
    lines.append(f"[sanity] Total entities: {entity_count}")

    # Scenario 1: KYC/CDD embedded SRs (101, 102, 104) should cluster on AE-21 and a small number
    # of plausible consumer-facing entities. AE-22 must NOT carry any of them. If many entities
    # coincidentally carry 2+ of these, the signal is diluted.
    kyc_set = {"SR-101", "SR-102", "SR-104"}
    kyc_carriers = {e: (kyc_set & s) for e, s in srs_by_entity.items() if kyc_set & s}
    multi_kyc = {e: srs for e, srs in kyc_carriers.items() if len(srs) >= 2}
    lines.append("")
    lines.append("[sanity] Scenario 1 — AE-20 -> AE-22 coarse-handoff (KYC embedded SRs 101/102/104):")
    lines.append(f"  expected owner (AE-21): {'OK' if kyc_set <= srs_by_entity.get('AE-21', set()) else 'MISS'} "
                 f"(has {sorted(srs_by_entity.get('AE-21', set()) & kyc_set)})")
    violation = kyc_set & srs_by_entity.get("AE-22", set())
    lines.append(f"  target must lack them (AE-22): {'OK (empty)' if not violation else f'LEAK: {sorted(violation)}'}")
    lines.append(f"  total carriers of any KYC SR: {len(kyc_carriers)} ({100*len(kyc_carriers)/entity_count:.0f}% of entities)")
    lines.append(f"  entities with 2+ KYC SRs (strong owners): {len(multi_kyc)}")
    for e, srs in sorted(multi_kyc.items()):
        tag = " SEEDED" if e in SEEDED and kyc_set & set(SEEDED[e]) else " (random)"
        lines.append(f"    {e} {name_by_id.get(e,'')}: {sorted(srs)}{tag}")
    # SR-103 stands alone since AE-20 is seeded to carry it.
    sr103_carriers = sorted(e for e, s in srs_by_entity.items() if "SR-103" in s)
    lines.append(f"  SR-103 carriers: {sr103_carriers}")

    # Scenario 2: AE-9 and AE-38 both have SR-110 and SR-111. Should be distinctive — few others.
    credit_set = {"SR-110", "SR-111"}
    credit_both = {e: srs_by_entity[e] & credit_set for e in srs_by_entity if credit_set <= srs_by_entity[e]}
    lines.append("")
    lines.append("[sanity] Scenario 2 — AE-9 / AE-38 clean credit match (SR-110 AND SR-111):")
    for e in sorted(credit_both):
        tag = " SEEDED" if e in {"AE-9", "AE-38", "AE-1"} else " (random)"
        lines.append(f"    {e} {name_by_id.get(e,'')}{tag}")
    seeded_ct = sum(1 for e in credit_both if e in {"AE-9", "AE-38", "AE-1"})
    random_ct = len(credit_both) - seeded_ct
    verdict = "clean" if random_ct <= seeded_ct else "DILUTED"
    lines.append(f"  seeded={seeded_ct}, random={random_ct} -> {verdict}")

    # Per-SR distribution for the restricted risks.
    lines.append("")
    lines.append("[sanity] Restricted-SR distribution:")
    restricted_to_show = ["SR-101", "SR-102", "SR-103", "SR-104", "SR-110", "SR-111", "SR-122", "SR-123", "SR-126"]
    for sr in restricted_to_show:
        carriers = sorted(e for e, s in srs_by_entity.items() if sr in s)
        lines.append(f"  {sr}: {len(carriers)} carriers -> {carriers}")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()
    df = build(args.input, args.output, seed=args.seed)
    active_df = pd.read_csv(args.input, dtype=str)
    active_df = active_df[(active_df["Audit Entity Type"] == "Audit") & (active_df["Audit Entity Status"] == "Active")]
    print(f"[stub_controls] {len(df)} rows across {df['Audit Entity ID'].nunique()} entities -> {args.output}")
    counts = df.groupby("Audit Entity ID").size()
    print(f"[stub_controls] per-entity count: min={counts.min()} max={counts.max()} mean={counts.mean():.1f}")
    print(_sanity_check_seeded(df, active_df))


if __name__ == "__main__":
    main()
