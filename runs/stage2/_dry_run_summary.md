# Stage 2 Batching — Dry Run Summary

Batches: **7**
Target budget: 85,000 tokens
Hard ceiling: 110,000 tokens
Worst-case multiplier: 1.5
Severed handoff edges: 105 / 184 (coverage remains via target/source context)

| # | Focal | Target ctx | Source ctx | Avg tokens | Worst-case tokens | Isolated | Split from |
|---|-------|------------|------------|------------|-------------------|----------|------------|
| 001 | 8 | 12 | 7 | 73,329 | 107,641 |  |  |
| 002 | 9 | 13 | 4 | 73,492 | 108,106 |  | 2 |
| 003 | 1 | 4 | 3 | 16,875 | 23,190 |  | 2 |
| 004 | 9 | 7 | 10 | 62,389 | 91,137 |  |  |
| 005 | 8 | 12 | 0 | 65,267 | 95,900 |  |  |
| 006 | 6 | 14 | 6 | 70,640 | 103,746 |  | 5 |
| 007 | 4 | 5 | 3 | 28,928 | 41,241 |  | 5 |

Avg batch (mean/max): 55,845 / 73,492
Worst-case batch (mean/max): 81,565 / 108,106

## Focal composition per batch
- **batch_001:** focal=['AE-10', 'AE-17', 'AE-27', 'AE-37', 'AE-40', 'AE-42', 'AE-44', 'AE-45']
- **batch_002:** focal=['AE-16', 'AE-2', 'AE-20', 'AE-22', 'AE-25', 'AE-33', 'AE-41', 'AE-43', 'AE-9']
- **batch_003:** focal=['AE-38']
- **batch_004:** focal=['AE-13', 'AE-18', 'AE-29', 'AE-3', 'AE-34', 'AE-39', 'AE-4', 'AE-6', 'AE-7']
- **batch_005:** focal=['AE-1', 'AE-12', 'AE-15', 'AE-19', 'AE-21', 'AE-24', 'AE-32', 'AE-36']
- **batch_006:** focal=['AE-11', 'AE-14', 'AE-30', 'AE-31', 'AE-35', 'AE-8']
- **batch_007:** focal=['AE-23', 'AE-26', 'AE-28', 'AE-5']