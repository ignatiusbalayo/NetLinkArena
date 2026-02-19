# Submissions

This folder contains all participant submissions.

## Structure

```
submissions/
└── inbox/
    └── <team_name>/
        └── <run_id>/
            ├── predictions.csv (required)
```

## How to Submit

1. **Fork this repository**

2. **Create your submission folder:**
   ```bash
   mkdir -p submissions/inbox/<your_username>/<run_id>
   ```
   Example: `submissions/inbox/alice/run_001/`

3. **Add your files:**
   - `predictions.csv` (required) - Your predictions
   - `metadata.json` (optional) - Model info

4. **Open a Pull Request**

## Files

### predictions.csv (Required)

Format:
```csv
id,y_pred
0,0.85
1,0.23
...
```

- Must have exactly 1,822 rows
- `id` must match test_nodes.csv
- `y_pred` must be probability in [0, 1]

### metadata.json (Optional)

Example:
```json
{
  "model": "GAT",
  "notes": "3-layer Graph Attention Network with dropout"
}
```

## Validation

Your submission will be automatically:
1. ✅ Validated for correct format
2. 📊 Evaluated (AUC-ROC calculated)
3. 💬 Score posted as PR comment
4. 🏆 Added to leaderboard (if valid)

## Rules

- ❌ **ONE submission only** per participant
- ❌ Duplicate submissions will be rejected
- ✅ You can validate locally before submitting:
  ```bash
  python competition/validate_submission.py predictions.csv
  ```

## Need Help?

Open an issue: https://github.com/ignatiusbalayo/NetLinkArena/issues
