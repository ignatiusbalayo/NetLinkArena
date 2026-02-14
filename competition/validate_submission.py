import pandas as pd
import sys

def main(pred_path, test_file_path):
    try:
        preds = pd.read_csv(pred_path)
        test_df = pd.read_csv(test_file_path)
    except Exception as e:
        raise ValueError(f"Could not read CSV files: {e}")

    # 1. Column Check
    if "id" not in preds.columns or "y_pred" not in preds.columns:
        raise ValueError("Submission must contain 'id' and 'y_pred' columns.")

    # 2. Duplicates Check
    if preds["id"].duplicated().any():
        raise ValueError("Duplicate IDs found in submission. Each pair can only be predicted once.")

    # 3. Missing Values Check
    if preds["y_pred"].isna().any():
        raise ValueError("NaN predictions found. Every ID needs a valid probability.")

    # 4. Bounds Check (Probabilities must be 0 to 1)
    if ((preds["y_pred"] < 0) | (preds["y_pred"] > 1)).any():
        raise ValueError("Predictions out of bounds. All y_pred values must be between 0 and 1.")

    # 5. ID Match Check
    pred_ids = set(preds["id"])
    test_ids = set(test_df["id"])
    
    if pred_ids != test_ids:
        missing = len(test_ids - pred_ids)
        extra = len(pred_ids - test_ids)
        raise ValueError(f"ID mismatch! Missing {missing} required IDs, found {extra} unexpected IDs.")

    print("✅ VALID SUBMISSION")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python validate_leaderboard.py <pred_path> <test_file_path>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
