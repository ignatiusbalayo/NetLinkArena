import csv
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "leaderboard" / "leaderboard.csv"
MD_PATH = ROOT / "leaderboard" / "leaderboard.md"

def read_rows():
    if not CSV_PATH.exists():
        return []
    with CSV_PATH.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [r for r in reader if (r.get("team") or "").strip()]
    return rows

def main():
    rows = read_rows()
    
    # Sort by ROC-AUC desc, then AP desc, then timestamp desc
    def score_key(r):
        try:
            # Looks for 'score' (which our eval script outputs) or 'roc_auc'
            return float(r.get("score", r.get("roc_auc", "-inf")))
        except ValueError:
            return float("-inf")
            
    def ap_key(r):
        try:
            # Secondary tie-breaker metric
            return float(r.get("ap", "-inf"))
        except ValueError:
            return float("-inf")
            
    def ts_key(r):
        try:
            ts_str = r.get("timestamp_utc", "")
            if not ts_str:
                return datetime.fromtimestamp(0)
            return datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        except ValueError:
            return datetime.fromtimestamp(0)

    # Apply the sorting logic
    rows.sort(key=lambda r: (score_key(r), ap_key(r), ts_key(r)), reverse=True)

    lines = []
    lines.append("# Leaderboard\n\n")
    lines.append("This leaderboard is **auto-updated** when a submission PR is merged. ")
    lines.append("For interactive search and filters, enable GitHub Pages and open **/docs/leaderboard.html**.\n\n")

    # Added AP to the table header
    lines.append("| Rank | Team | Model | ROC-AUC | AP | Date (UTC) | Notes |\n")
    lines.append("|---:|---|---|---:|---:|---|---|\n")
    
    for i, r in enumerate(rows, start=1):
        team = (r.get("team") or "").strip()
        model = (r.get("model") or "").strip()
        score = r.get("score", r.get("roc_auc", ""))
        ap = (r.get("ap") or "").strip()
        ts = (r.get("timestamp_utc") or "").strip()
        notes = (r.get("notes") or "").strip()
        
        # Tiny "badge" feel with inline code
        model_disp = f"`{model}`" if model else ""
        
        # Ensure clean float formatting for the UI
        try:
            score_disp = f"{float(score):.4f}" if score else "-"
        except ValueError:
            score_disp = score
            
        try:
            ap_disp = f"{float(ap):.4f}" if ap else "-"
        except ValueError:
            ap_disp = ap

        lines.append(f"| {i} | {team} | {model_disp} | {score_disp} | {ap_disp} | {ts} | {notes} |\n")

    # Safety: ensure parent directory exists before writing
    MD_PATH.parent.mkdir(parents=True, exist_ok=True)
    MD_PATH.write_text("".join(lines), encoding="utf-8")
    print(f"✅ Leaderboard successfully rendered at {MD_PATH}")

if __name__ == "__main__":
    main()
