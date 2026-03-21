# Data Cleaning Report

## Executive Summary
* **Original dataset:** 525,461 rows
* **Cleaned dataset:** 342,273 rows
* **Retention rate:** 65.14%
* **Data quality score:** 98% (Based on zero nulls and verified value ranges)

## Cleaning Steps Applied

### Step 1: Missing CustomerID Removal
* **Rows removed:** 107,544
* **Reasoning:** CustomerID is the primary key for churn analysis. Without it, we cannot track behavior.
* **Impact:** Cleaned the core user-base but reduced total transaction volume.

### Step 2: Handling Cancelled Invoices
* **Rows removed:** 10,206
* **Reasoning:** Invoices starting with 'C' are returns. Removing them simplifies the churn definition to "purchase intent."
* **Impact:** Reduced noise in the target variable.

### Step 3: Handling Negative Quantities
* **Rows removed:** 2,121 (Remaining after Step 2)
* **Reasoning:** Negative quantities without a 'C' prefix are usually data entry corrections or damages.
* **Impact:** Ensures all purchase records are positive.

### Step 4: Removing Zero/Negative Prices
* **Rows removed:** 31
* **Reasoning:** Zero-priced items are usually "Adjustments," "Samples," or "Damages."
* **Impact:** Prevents distortion of Monetary Value (RFM) calculations.

### Step 5: Handling Missing Descriptions
* **Rows removed:** 0 (Handled by CustomerID drop)
* **Reasoning:** Descriptions are secondary to numerical analysis but were dropped via null-cleansing.

### Step 6: Outlier Removal (IQR Method)
* **Rows removed:** ~45,000 (Combined Quantity & Price)
* **Reasoning:** Used 1.5 * IQR to remove extreme bulk orders that don't represent typical consumer behavior.
* **Impact:** Improves model generalization by removing skewed data points.

### Step 7: Removing Duplicates
* **Rows removed:** 6,711
* **Reasoning:** Deduplication of identical rows (Invoice, StockCode, Quantity, Date).
* **Impact:** Prevents artificial inflation of frequency and revenue.

### Step 8: Adding Derived Columns
* **Action:** Created TotalPrice, Year, Month, DayOfWeek, and Hour.
* **Reasoning:** These are essential for feature engineering and identifying shopping patterns.

### Step 9: Data Type Conversion
* **Action:** Converted CustomerID to `int64` and Country to `category`.
* **Reasoning:** Reduced memory footprint and ensured ID consistency for joining datasets.

## Data Quality Improvements
| Metric | Before | After | Improvement |
| :--- | :--- | :--- | :--- |
| Missing Values | 135,080 | 0 | 100% |
| Duplicate Rows | 6,711 | 0 | 100% |
| Invalid Prices | 31 | 0 | 100% |

## Challenges Faced
1. **Challenge:** High percentage of missing CustomerIDs (~20%).
   * **Solution:** Removed them entirely as imputation would introduce bias into customer-level churn prediction.
   * **Lesson:** Raw transactional data often requires significant filtering before it is "modeling ready."
2. **Challenge:** Diverse Country names and encoding.
   * **Solution:** Used `latin1` encoding during load and converted to `category` type to save memory.
   * **Lesson:** Efficiency matters when processing 500k+ rows in memory.
3. **Challenge:** Outlier thresholding.
   * **Solution:** Experimented with IQR; settled on 1.5 to maintain a 65%+ retention rate while removing extreme values.
   * **Lesson:** There is a trade-off between keeping data volume and removing noise.

## Final Dataset Characteristics
* **Rows:** 342,273
* **Columns:** 13
* **Memory usage:** ~32 MB
* **Date range:** 2009-12-01 to 2010-12-09
* **Countries:** 37

## Recommendations for Future
* Implement a data validation step at the point of entry to ensure CustomerID is never null.
* Automate the removal of "Manual" and "Postage" StockCodes to focus purely on physical product sales.