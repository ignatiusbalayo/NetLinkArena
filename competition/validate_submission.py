import pandas as pd
import sys
import os

def main(pred_path):
    """
    Validate submission format.
    Now loads test_nodes.csv automatically from data/public/
    """
    try:
        preds = pd.read_csv(pred_path)
    except Exception as e:
        raise ValueError(f"Could not read prediction file: {e}")
    
    # Auto-detect test_nodes.csv location
    possible_paths = [
        'data/public/test_nodes.csv',
        'NetLinkArena_Dataset/data/public/test_nodes.csv',
        '../data/public/test_nodes.csv'
    ]
    
    test_df = None
    for path in possible_paths:
        if os.path.exists(path):
            test_df = pd.read_csv(path)
            break
    
    if test_df is None:
        raise ValueError(
            "Could not find test_nodes.csv. "
            "Expected in data/public/test_nodes.csv"
        )
    
    # 1. Column Check
    if "id" not in preds.columns or "y_pred" not in preds.columns:
        raise ValueError("Submission must contain 'id' and 'y_pred' columns.")
    
    # 2. Duplicates Check
    if preds["id"].duplicated().any():
        raise ValueError(
            "Duplicate IDs found in submission. "
            "Each pair can only be predicted once."
        )
    
    # 3. Missing Values Check
    if preds["y_pred"].isna().any():
        raise ValueError(
            "NaN predictions found. "
            "Every ID needs a valid probability."
        )
    
    # 4. Bounds Check (Probabilities must be 0 to 1)
    if ((preds["y_pred"] < 0) | (preds["y_pred"] > 1)).any():
        raise ValueError(
            "Predictions out of bounds. "
            "All y_pred values must be between 0 and 1."
        )
    
    # 5. ID Match Check
    pred_ids = set(preds["id"])
    test_ids = set(test_df["id"])
    
    if pred_ids != test_ids:
        missing = len(test_ids - pred_ids)
        extra = len(pred_ids - test_ids)
        raise ValueError(
            f"ID mismatch! "
            f"Missing {missing} required IDs, "
            f"found {extra} unexpected IDs."
        )
    
    print("✅ VALID SUBMISSION")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_submission.py <pred_path>")
        sys.exit(1)
    
    try:
        main(sys.argv[1])
    except ValueError as e:
        print(f"❌ VALIDATION FAILED: {e}")
        sys.exit(1)
