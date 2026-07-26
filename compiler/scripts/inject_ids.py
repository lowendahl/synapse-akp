"""One-shot script: inject stable IDs into all OKF corpus files."""
import re
from pathlib import Path


def slugify(text: str) -> str:
    slug = text.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    if len(slug) > 50:
        slug = slug[:50].rstrip("-")
    return slug


DIR_CATEGORY_MAP = {
    "/evidence/": "evidence",
    "/metrics/": "metric",
    "/kpis/": "kpi",
    "/pipeline/": "pipeline",
    "/programs/": "program",
    "/roles/": "role",
    "/priorities/": "priority",
    "/planning/": "planning",
    "/processes/": "process",
    "/stages/": "stage",
    "/organization/": "organization",
    "/risks/": "risk",
    "/governance/": "governance",
    "/unified/": "unified",
    "/delivery/": "delivery",
    "/doctrine/": "doctrine",
    "/outcomes/": "outcome",
    "/gtm/": "gtm",
}

TYPE_CATEGORY_MAP = {
    "Framework": "framework",
    "MCEM Stage": "stage",
    "Stage": "stage",
    "Methodology": "methodology",
    "Strategy": "strategy",
    "Organization": "organization",
    "Operating Model": "organization",
    "Role": "role",
    "Process": "process",
    "Metric": "metric",
    "Metric Collection": "metric",
    "KPI": "kpi",
    "Doctrine": "doctrine",
    "Program": "program",
    "Outcome Framework": "outcome",
    "Evidence Source": "evidence",
    "Evidence Map": "evidence",
    "Risk Indicator": "risk",
    "Risk Signal": "risk",
    "Priority": "priority",
    "Planning Artifact": "planning",
    "Taxonomy": "taxonomy",
    "Pipeline Object": "pipeline",
    "Pipeline Field": "pipeline",
    "Pipeline Taxonomy": "pipeline",
    "Governance": "governance",
    "Governance Rhythm": "governance",
    "GTM Concept": "gtm",
    "Contract Model": "contract",
    "Delivery Offering": "delivery",
    "Measurement Concept": "measurement",
    "Index": "index",
    "Log": "log",
}


def infer_category(path_str: str, fm_type: str) -> str:
    normalized = path_str.replace("\\", "/").lower()
    for pattern, cat in DIR_CATEGORY_MAP.items():
        if pattern in normalized:
            return cat
    return TYPE_CATEGORY_MAP.get(fm_type, "concept")


def add_id_to_file(filepath: Path) -> tuple[bool, str]:
    content = filepath.read_text(encoding="utf-8")

    fm_match = re.match(r"^---\s*\n(.+?)\n---\s*\n?(.*)", content, re.DOTALL)
    if not fm_match:
        return False, "no frontmatter"

    fm_text = fm_match.group(1)
    body = fm_match.group(2)

    if re.search(r"^id:\s", fm_text, re.MULTILINE):
        return False, "already has id"

    title_match = re.search(r"^title:\s*(.+)$", fm_text, re.MULTILINE)
    type_match = re.search(r"^type:\s*(.+)$", fm_text, re.MULTILINE)

    if not title_match:
        return False, "no title"

    title = title_match.group(1).strip().strip('"').strip("'")
    fm_type = type_match.group(1).strip().strip('"').strip("'") if type_match else ""

    path_str = str(filepath).replace("\\", "/")
    if "/mcem/" in path_str:
        domain = "mcem"
    elif "/csu/" in path_str:
        domain = "csu"
    else:
        domain = "okf"

    category = infer_category(path_str, fm_type)
    slug = slugify(title)
    obj_id = f"{domain}.{category}.{slug}"

    # Insert id: right after the title: line
    new_fm = re.sub(
        r"(^title:\s*.+$)",
        r"\g<1>" + f"\nid: {obj_id}",
        fm_text,
        count=1,
        flags=re.MULTILINE,
    )

    new_content = f"---\n{new_fm}\n---\n{body}"
    filepath.write_text(new_content, encoding="utf-8")
    return True, obj_id


def main() -> None:
    count = 0
    skipped = 0

    for root_dir in ["okf/csu", "okf/mcem"]:
        root = Path(root_dir)
        if not root.exists():
            continue
        for md_file in sorted(root.rglob("*.md")):
            success, info = add_id_to_file(md_file)
            if success:
                count += 1
                print(f"  + {info}")
            else:
                skipped += 1

    print(f"\nAdded IDs to {count} files, skipped {skipped}")


if __name__ == "__main__":
    main()
