# NetLinkArena - Link Prediction Challenge

## 🎯 Challenge Overview
**Can you predict hidden connections in a scientific citation network?**

NetLinkArena is a link prediction competition where participants must infer missing citation links between research papers. Your score is determined by **AUC-ROC** - how well you rank true connections above false ones!

---

## 📊 Dataset Information

The dataset was processed using the `Planetoid` library with the following graph properties:

* **Undirected:** True
* **Self-loops:** False
* **Isolated Nodes:** False
* **Total Nodes:** 3,327
* **Total Node Features:** 2,742
* **Total Edges:** 9,104 (train + val + test)

---

## 🔥 What Makes This Hard?

- ✅ **Sparse Features** - 96.5% of feature values are zeros (bag-of-words representation)
- ✅ **Graph Structure Critical** - Node features alone are insufficient; GNN models required
- ✅ **Obfuscated Features** - Node features have been permuted and noise-injected to prevent information leakage
- ✅ **Large Graph** - 3,327 nodes with complex citation patterns

**Expected Performance:**
- Random baseline: ~50% AUC-ROC
- Feature-only model: ~55-60% AUC-ROC
- Good GNN: ~70-75% AUC-ROC
- Excellent GNN: **>80% AUC-ROC** 🎯

---

## 📈 Dataset Distribution

| Split | Positive Edges | Negative Edges | Total | Label Ratio |
|:------|:--------------|:---------------|:------|:------------|
| **Training** | 2,730 | 2,730 | 5,460 | 1:1 (balanced) |
| **Validation** | 911 | 911 | 1,822 | 1:1 (balanced) |
| **Testing** | 911 | 911 | 1,822 | 1:1 (balanced) |

---

## 1. Task Overview

**Task:** Link prediction on a citation graph  
**Input:** Node features for all papers + training edge labels  
**Output:** Probability predictions for test edge pairs  
**Metric:** AUC-ROC (Area Under the Receiver Operating Characteristic Curve)

Participants train any GNN or ML model *offline* and submit probability predictions for the test edges.

---

## 2. Repository Structure

```
.
├── data/
│   ├── public/
│   │   ├── node_features.csv      # Features for ALL nodes
│   │   ├── train_edges.csv        # Training edges WITH labels
│   │   ├── val_edges.csv          # Validation edges WITH labels
│   │   ├── test_nodes.csv         # Test edges WITHOUT labels
│   │   └── sample_submission.csv
│   └── private/
│       └── test_labels.csv        # Never committed (used only in CI)
├── competition/
│   ├── config.yaml
│   ├── validate_submission.py
│   ├── evaluate.py
│   └── metrics.py
├── submissions/
│   ├── README.md
│   └── submissions/inbox/<team_name>/<run_id>/
├── leaderboard/
│   ├── leaderboard.csv
│   └── leaderboard.md
└── .github/workflows/
    ├── score_submission.yml
    └── publish_leaderboard.yml
```

---

## 3. Dataset Files

### node_features.csv
Features for **ALL** papers in the network.

```csv
node_id,0,1,2,3,...,2741
0,0.0,1.0,0.0,1.0,...,0.0
1,1.0,0.0,0.0,0.0,...,1.0
...
3326,...
```

- **Rows:** 3,327 (one per paper)
- **Columns:** 2,742 features + node_id
- **Values:** Sparse bag-of-words (mostly 0/1)

### train_edges.csv
Training examples **WITH** labels.

```csv
source,target,label
15,234,1     ← Papers 15 and 234 ARE connected (citation exists)
42,891,0     ← Papers 42 and 891 are NOT connected
...
```

- **Rows:** 5,460 edge pairs
- **Label:** 1 = edge exists, 0 = no edge

### val_edges.csv
Validation examples **WITH** labels (same format as train).

```csv
source,target,label
56,789,1
12,345,0
...
```

### test_nodes.csv
Test edges **WITHOUT** labels - you must predict!

```csv
id,source,target
0,456,789    ← Does paper 456 cite paper 789? PREDICT!
1,123,456    ← Does paper 123 cite paper 456? PREDICT!
...
```

---

## 4. Submission Format

Participants submit a **single CSV file**:

**predictions.csv**
```csv
id,y_pred
0,0.85
1,0.23
2,0.91
...
```

**Rules:**
- `id` must match exactly the IDs in `test_nodes.csv`
- One row per test edge (1,822 rows)
- `y_pred` must be a probability in [0, 1]
- No missing or duplicate IDs

A sample is provided in:
```
data/public/sample_submission.csv
```

---

## 5. How to Submit

### Pull Request 

1. Fork this repository
2. Create a new folder:
```
submissions/inbox/<team_name>/<run_id>/
```

3. Add:
   - `predictions.csv`
   - `metadata.json`

Example `metadata.json`:
```json
{
  "team": "awesome_team",
  "model": "GAT",
  "notes": "Graph Attention Network with negative sampling"
}
```

4. Open a Pull Request to `main`

The PR will be **automatically scored** and the result posted as a comment.

## 6. 📥 Download Dataset

The complete dataset is available in **GitHub Releases**.

### Quick Setup

```bash
# 1. Clone repository
git clone https://github.com/YOUR-USERNAME/NetLinkArena.git
cd NetLinkArena

# 2. Download dataset
wget https://github.com/YOUR-USERNAME/NetLinkArena/releases/download/v1.0.0/netlinkarena_dataset.zip

# 3. Extract
unzip netlinkarena_dataset.zip

# 4. Verify files
ls data/public/*.csv
# Should show: node_features.csv, train_edges.csv, val_edges.csv, test_nodes.csv, sample_submission.csv

# 5. Install dependencies
pip install -r requirements.txt

# 6. Run baseline
python baseline.py
```

**Alternative:** Download manually from [Releases](https://github.com/ignatiusbalayo/NetLinkArena/releases/download/v1.0/NetLinkArena_Dataset.zip)

---

## 7. 📊 Leaderboard

View the interactive leaderboard here: [**Leaderboard**](https://ignatiusbalayo.github.io/NetLinkArena/leaderboard.html)

After a PR is merged, the submission is added to:
- `leaderboard/leaderboard.csv`
- `leaderboard/leaderboard.md`

Rankings are sorted by **descending AUC-ROC score**.

**Privacy:** Submission files are private. Only scores, team names, and timestamps are public.

---

## 8. Rules

### Allowed
✅ Any graph neural network architecture  
✅ Feature engineering on node features  
✅ Negative sampling strategies  
✅ Ensemble models  
✅ Unlimited offline training  

### Not Allowed
❌ No external datasets  
❌ No manual labeling of test edges  
❌ No modification of evaluation scripts  
❌ No test set peeking  
❌ **ONE submission per participant** (strictly enforced)

Violations may result in disqualification.

---

## 9. Baseline Performance

**Simple GCN Baseline:**
2-layer GCN (128 → 64 dimensions, dot product decoder)
100 epochs, ~20 minutes on CPU
Expected AUC-ROC: 0.65-0.75

**Your goal:** Beat the baseline with advanced GNN models! 🎯

---

## 10. Getting Started

### Explore the Data

```python
import pandas as pd

# Load data
features = pd.read_csv('data/public/node_features.csv')
train = pd.read_csv('data/public/train_edges.csv')
val = pd.read_csv('data/public/val_edges.csv')
test = pd.read_csv('data/public/test_nodes.csv')

# Explore
print(f"Nodes: {len(features):,}")
print(f"Features per node: {features.shape[1]-1:,}")
print(f"Training edges: {len(train):,}")
print(f"Positive: {(train['label']==1).sum():,}")
print(f"Negative: {(train['label']==0).sum():,}")
```

### Build a GNN Model

```python
from torch_geometric.nn import GCNConv, GATConv

class LinkPredictor(nn.Module):
    def __init__(self, num_features, hidden_dim):
        super().__init__()
        self.conv1 = GCNConv(num_features, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, hidden_dim)
        
    def encode(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index)
        return x
    
    def decode(self, z, edge_index):
        # Link prediction via inner product
        return (z[edge_index[0]] * z[edge_index[1]]).sum(dim=-1)
```

### Generate Predictions

```python
# Predict on test edges
test = pd.read_csv('data/public/test_nodes.csv')

# Get embeddings
with torch.no_grad():
    z = model.encode(x, edge_index)
    test_edge_index = torch.tensor([test['source'].values, 
                                     test['target'].values])
    predictions = torch.sigmoid(model.decode(z, test_edge_index))

# Create submission
submission = pd.DataFrame({
    'id': test['id'],
    'y_pred': predictions.numpy()
})
submission.to_csv('predictions.csv', index=False)
```

---

## 11. Tips & Resources

### Key Insights
- 📊 **Use graph structure:** Features alone won't beat the baseline
- 🎯 **Handle sparsity:** 96.5% of features are zeros
- 🔗 **Link prediction techniques:** Inner product, MLP decoder, attention
- ⚖️ **Balanced data:** No class imbalance to worry about

### Recommended Architectures
- **GCN** (Graph Convolutional Network)
- **GAT** (Graph Attention Network)
- **GraphSAGE**
- **GIN** (Graph Isomorphism Network)

### Resources
- [PyTorch Geometric Tutorial](https://pytorch-geometric.readthedocs.io/)
- [GCN Paper](https://arxiv.org/abs/1609.02907)
- [GAT Paper](https://arxiv.org/abs/1710.10903)
- [Link Prediction Survey](https://arxiv.org/abs/2010.16103)

---

## 12. Human vs LLM Studies

To use this competition for research comparing human and LLM performance:

- Fix a time budget (e.g., 2 hours)
- Fix a submission budget (e.g., 5 runs)
- Record metadata fields (`model`, `team`, `notes`)
- Compare:
  - Validity rate (% of valid submissions)
  - Best score within K submissions
  - Score vs submission index
  - AUC-ROC distribution

---

## 13. References

- **Data:** [Planetoid-CiteSeer](https://pytorch-geometric.readthedocs.io/en/latest/generated/torch_geometric.datasets.Planetoid.html)
- **Task:** Link Prediction on Citation Networks
- **Framework:** PyTorch Geometric

---

## 14. License

MIT License.
