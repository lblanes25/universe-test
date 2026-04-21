# Stage 2 Batching — Dry Run Summary

Batches: **8**
Target budget: 85,000 tokens
Hard ceiling: 110,000 tokens
Worst-case multiplier: 1.5
Severed handoff edges: 122 / 199 (coverage remains via target/source context)

| # | Focal | Target ctx | Source ctx | Avg tokens | Worst-case tokens | Isolated | Split from |
|---|-------|------------|------------|------------|-------------------|----------|------------|
| 001 | 9 | 11 | 4 | 65,139 | 95,570 |  |  |
| 002 | 5 | 11 | 5 | 53,640 | 78,186 |  |  |
| 003 | 7 | 15 | 2 | 71,549 | 105,268 |  | 3 |
| 004 | 1 | 4 | 4 | 15,259 | 20,696 |  | 3 |
| 005 | 8 | 12 | 8 | 73,120 | 107,365 |  | 4 |
| 006 | 2 | 4 | 3 | 21,924 | 30,734 |  | 4 |
| 007 | 10 | 9 | 8 | 65,580 | 96,012 |  |  |
| 008 | 6 | 11 | 2 | 55,232 | 80,740 |  |  |

Avg batch (mean/max): 52,680 / 73,120
Worst-case batch (mean/max): 76,821 / 107,365

## Focal composition per batch
- **batch_001:** focal=['AE-11', 'AE-12', 'AE-15', 'AE-19', 'AE-26', 'AE-3', 'AE-31', 'AE-37', 'AE-42']
- **batch_002:** focal=['AE-1', 'AE-36', 'AE-44', 'AE-45', 'AE-47']
- **batch_003:** focal=['AE-20', 'AE-23', 'AE-35', 'AE-38', 'AE-43', 'AE-5', 'AE-9']
- **batch_004:** focal=['AE-48']
- **batch_005:** focal=['AE-14', 'AE-18', 'AE-32', 'AE-33', 'AE-34', 'AE-39', 'AE-6', 'AE-7']
- **batch_006:** focal=['AE-10', 'AE-13']
- **batch_007:** focal=['AE-17', 'AE-2', 'AE-22', 'AE-27', 'AE-30', 'AE-4', 'AE-40', 'AE-41', 'AE-46', 'AE-8']
- **batch_008:** focal=['AE-16', 'AE-21', 'AE-24', 'AE-25', 'AE-28', 'AE-29']