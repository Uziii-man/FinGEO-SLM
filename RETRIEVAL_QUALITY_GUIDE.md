# Document Retrieval Quality Guide

## Problem: Model Getting Wrong Documents

You're right to be concerned! If the model gets the **wrong documents**, it will generate **wrong answers**, no matter how good the model is.

### Why This Happens

**Basic BM25 Issues:**
1. ❌ Keyword matching only - misses semantic meaning
2. ❌ No relevance filtering - includes marginally relevant docs
3. ❌ Poor ranking - best documents not always on top
4. ❌ No quality checks - can't tell if retrieval worked

---

## Solution: Enhanced Retrieval (Now Added!)

### What Was Added

✅ **Semantic Relevance Scoring**
- Goes beyond keyword matching
- Considers query term density
- Rewards early mention of key terms
- Detects exact phrase matches

✅ **Document Reranking**
- Retrieves 20 documents initially
- Reranks by relevance (not just keywords)
- Returns top 5 most relevant
- Filters out irrelevant results

✅ **Relevance Filtering**
- Minimum threshold (default: 0.15)
- Removes documents below threshold
- Ensures only relevant docs reach the model

✅ **Quality Diagnosis**
- Rates retrieval quality (Excellent/Good/Fair/Poor)
- Shows average relevance scores
- Provides recommendations
- Identifies issues automatically

---

## How to Use

### Step 1: Enable Enhanced Retrieval

In the notebook, find the test queries section:

```python
USE_ENHANCED_RETRIEVAL = True  # ⭐ Set this to True (RECOMMENDED)
INITIAL_RETRIEVE_K = 20  # Retrieve more documents initially
FINAL_TOP_K = 5  # Return top 5 after reranking
MIN_RELEVANCE_THRESHOLD = 0.15  # Filter out irrelevant docs
```

### Step 2: Run and Check Quality

The output will show:

```
Query 1/3: What major integrated resort project...
  Retrieval Quality: EXCELLENT
  Avg Relevance: 0.623
  Documents Retrieved: 5
  ✓ High quality retrieval
```

### Step 3: View Relevance Visualization

A new visualization shows:
- Bar chart of document relevance scores
- Color-coded by quality (Green/Yellow/Orange/Red)
- Threshold line showing minimum
- Quality assessment per query

---

## Understanding Relevance Scores

### Score Interpretation

| Score | Quality | Meaning | Action |
|-------|---------|---------|--------|
| **≥0.5** | 🟢 Excellent | Highly relevant - answers should be accurate | ✓ Keep as is |
| **0.3-0.5** | 🟡 Good | Relevant - answers likely helpful | ✓ Keep as is |
| **0.15-0.3** | 🟠 Fair | Marginally relevant - answers may be incomplete | ⚠ Consider adjusting |
| **<0.15** | 🔴 Poor | Not relevant - answers may be incorrect | ❌ Needs fixing |

### What Affects Relevance?

1. **Lexical Overlap (40%)**
   - How many query terms appear in document?
   - "revenue growth" → both terms present = higher score

2. **Term Density (30%)**
   - How concentrated are query terms?
   - Many mentions = higher relevance

3. **Positional Bonus (up to 30%)**
   - Are query terms mentioned early?
   - First 100 characters = bonus

4. **Phrase Matching (up to 20%)**
   - Does exact phrase appear?
   - "risk management" as phrase = bonus

---

## Troubleshooting Poor Retrieval

### Problem 1: All Scores Below 0.3 (Fair/Poor)

**Diagnosis:** Query doesn't match document vocabulary

**Solutions:**
1. **Rephrase Query:**
   ```python
   # Instead of:
   "What are the financial results?"
   
   # Try:
   "What are the revenue and profit numbers?"
   ```

2. **Lower Threshold:**
   ```python
   MIN_RELEVANCE_THRESHOLD = 0.10  # Instead of 0.15
   ```

3. **Increase Initial Retrieval:**
   ```python
   INITIAL_RETRIEVE_K = 30  # Instead of 20
   ```

### Problem 2: No Documents Retrieved

**Diagnosis:** All documents below threshold

**Solutions:**
1. **Check Documents Are Loaded:**
   ```python
   print(f"Total chunks: {len(chunks)}")
   # Should be > 0
   ```

2. **Lower Threshold Significantly:**
   ```python
   MIN_RELEVANCE_THRESHOLD = 0.05  # Very permissive
   ```

3. **Check PDF Content:**
   - Are PDFs in correct location?
   - Do they contain text (not just images)?
   - Are they financial documents?

### Problem 3: Inconsistent Quality

**Diagnosis:** Some queries work, others don't

**Solutions:**
1. **Analyze Working vs Failing Queries:**
   - What keywords work?
   - What vocabulary is in documents?

2. **Add Query Expansion:**
   ```python
   # Manually expand before querying
   query = "CEO compensation and bonuses"
   # Query contains relevant terms from documents
   ```

3. **Check Document Coverage:**
   - Do documents cover all query topics?
   - May need additional PDF sources

---

## Advanced Configuration

### For Very Picky Retrieval (High Precision)

```python
USE_ENHANCED_RETRIEVAL = True
INITIAL_RETRIEVE_K = 30
FINAL_TOP_K = 3  # Only top 3
MIN_RELEVANCE_THRESHOLD = 0.25  # Higher threshold
```

**Result:** Fewer but more relevant documents

### For Broader Retrieval (High Recall)

```python
USE_ENHANCED_RETRIEVAL = True
INITIAL_RETRIEVE_K = 40
FINAL_TOP_K = 8  # More documents
MIN_RELEVANCE_THRESHOLD = 0.10  # Lower threshold
```

**Result:** More documents, possibly less precise

### For Fastest Retrieval

```python
USE_ENHANCED_RETRIEVAL = False  # Basic BM25 only
```

**Result:** Faster but potentially less accurate

---

## Verification Workflow

### Step-by-Step Verification

1. **Run Retrieval with Enhanced Mode**
   ```python
   USE_ENHANCED_RETRIEVAL = True
   ```

2. **Check Quality Output**
   ```
   Retrieval Quality: EXCELLENT
   Avg Relevance: 0.623
   ```

3. **View Visualization**
   - Look at relevance bar chart
   - Check if most documents are Green/Yellow

4. **Generate Answers**
   - If retrieval quality is Good/Excellent → Answers should be accurate
   - If retrieval quality is Fair/Poor → Answers may be wrong

5. **Validate Answer Quality**
   - Check answer validation metrics
   - Compare with source documents
   - Verify citations point to right documents

---

## Before vs After

### Before (Basic BM25)

```
Query: "What are the key risk factors?"

Retrieved:
1. Document about board members (Score: unknown)
2. Document about company history (Score: unknown)
3. Document about risk factors (Score: unknown)
4. Document about revenue (Score: unknown)
5. Document about offices (Score: unknown)

❌ Problem: Can't tell which documents are relevant!
❌ Result: Model sees irrelevant docs → wrong answer
```

### After (Enhanced Retrieval)

```
Query: "What are the key risk factors?"

Retrieved (Reranked):
1. Document about risk factors (Score: 0.734) 🟢
2. Document about risk management (Score: 0.652) 🟢
3. Document about compliance risks (Score: 0.489) 🟡
4. Document about audit findings (Score: 0.342) 🟡
5. Document about regulatory issues (Score: 0.287) 🟠

Quality: EXCELLENT (Avg: 0.501)
✅ Solution: Only relevant docs → correct answer!
```

---

## Key Takeaways

✅ **Always Enable Enhanced Retrieval**
- Dramatically improves document relevance
- Filters out wrong documents
- Provides quality feedback

✅ **Check Relevance Scores**
- Look at visualization
- Aim for Green/Yellow documents
- Fix if seeing mostly Orange/Red

✅ **Adjust Thresholds as Needed**
- Higher threshold = more precise
- Lower threshold = more recall
- Balance based on your needs

✅ **Validate Answers**
- Good retrieval ≠ guaranteed correct answer
- But poor retrieval = almost certainly wrong answer
- Always check answer validation metrics

---

## Quick Reference

### Configuration Presets

**Balanced (Recommended):**
```python
INITIAL_RETRIEVE_K = 20
FINAL_TOP_K = 5
MIN_RELEVANCE_THRESHOLD = 0.15
```

**High Precision:**
```python
INITIAL_RETRIEVE_K = 30
FINAL_TOP_K = 3
MIN_RELEVANCE_THRESHOLD = 0.25
```

**High Recall:**
```python
INITIAL_RETRIEVE_K = 40
FINAL_TOP_K = 8
MIN_RELEVANCE_THRESHOLD = 0.10
```

### Quality Targets

- **Excellent (≥0.5):** Keep settings
- **Good (≥0.3):** Keep settings
- **Fair (≥0.15):** Consider adjustments
- **Poor (<0.15):** Needs fixing

---

## Summary

🎯 **The Problem:** Model was getting wrong documents → wrong answers

✅ **The Solution:** Enhanced retrieval with:
- Semantic relevance scoring
- Document reranking
- Relevance filtering
- Quality diagnosis

📊 **The Result:** 
- See which documents are relevant
- Filter out irrelevant documents
- Get better answers from the model
- Know when retrieval quality is poor

💡 **Pro Tip:** Always check the relevance visualization BEFORE looking at generated answers. If retrieval quality is poor, fix that first!
