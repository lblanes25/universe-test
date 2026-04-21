# Stage 2 Batching — Dry Run Summary

Batches: **11**
Target budget: 85,000 tokens
Hard ceiling: 110,000 tokens
Worst-case multiplier: 1.5
Severed handoff edges: 134 / 199 (coverage remains via target/source context)

| # | Focal | Target ctx | Source ctx | Avg tokens | Worst-case tokens | Isolated | Split from |
|---|-------|------------|------------|------------|-------------------|----------|------------|
| 001 | 3 | 3 | 2 | 22,412 | 31,511 |  |  |
| 002 | 5 | 9 | 3 | 48,360 | 70,433 |  |  |
| 003 | 7 | 13 | 2 | 58,746 | 86,054 |  |  |
| 004 | 7 | 7 | 8 | 52,405 | 76,307 |  |  |
| 005 | 6 | 14 | 7 | 70,979 | 104,206 |  | 5 |
| 006 | 1 | 3 | 1 | 15,573 | 21,290 |  | 5 |
| 007 | 5 | 5 | 5 | 35,121 | 50,466 |  |  |
| 008 | 4 | 10 | 2 | 47,091 | 68,544 |  |  |
| 009 | 4 | 5 | 4 | 35,382 | 50,873 |  |  |
| 010 | 3 | 8 | 2 | 37,710 | 54,457 |  |  |
| 011 | 3 | 8 | 4 | 33,815 | 48,574 |  |  |

Avg batch (mean/max): 41,599 / 70,979
Worst-case batch (mean/max): 60,246 / 104,206

## Focal composition per batch
- **batch_001:** focal=['AE-2', 'AE-22', 'AE-41']
- **batch_002:** focal=['AE-12', 'AE-20', 'AE-38', 'AE-5', 'AE-9']
- **batch_003:** focal=['AE-1', 'AE-15', 'AE-36', 'AE-4', 'AE-40', 'AE-46', 'AE-47']
- **batch_004:** focal=['AE-13', 'AE-18', 'AE-3', 'AE-33', 'AE-34', 'AE-6', 'AE-7']
- **batch_005:** focal=['AE-14', 'AE-27', 'AE-30', 'AE-39', 'AE-44', 'AE-8']
- **batch_006:** focal=['AE-10']
- **batch_007:** focal=['AE-16', 'AE-25', 'AE-26', 'AE-28', 'AE-31']
- **batch_008:** focal=['AE-11', 'AE-23', 'AE-32', 'AE-35']
- **batch_009:** focal=['AE-17', 'AE-19', 'AE-42', 'AE-45']
- **batch_010:** focal=['AE-21', 'AE-24', 'AE-29']
- **batch_011:** focal=['AE-37', 'AE-43', 'AE-48']