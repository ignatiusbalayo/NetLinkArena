import pandas as pd
import sys
from metrics import calculate_metrics

def main(pred_path, label_path):
    try:
        preds = pd.read_csv(pred_path)
        labels = pd.read_csv(label_path)
    except Exception as e:
        raise ValueError(f"Error reading CSV files: {e}")
    
    # Validate submission format
    if "id" not in preds.columns or "y_pred" not in preds.columns:
        raise ValueError("Submission must contain 'id' and 'y_pred' columns.")
    
    # Sort and merge on 'id' column
    preds = preds.sort_values("id")
    labels = labels.sort_values("id")
    merged = labels.merge(preds, on="id", how="inner")
    
    if len(merged) != len(labels):
        raise ValueError(
            f"ID mismatch! Expected {len(labels)} pairs, "
            f"but got {len(merged)} matching pairs in submission."
        )
    
    # Calculate metrics
    scores = calculate_metrics(merged["label"], merged["y_pred"])
    
    # Output ONLY the AUC-ROC score (workflow expects single value)
    print(f"{scores['roc_auc']:.4f}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python evaluate.py <pred_path> <label_path>")
        sys.exit(1)
    
    main(sys.argv[1], sys.argv[2])
