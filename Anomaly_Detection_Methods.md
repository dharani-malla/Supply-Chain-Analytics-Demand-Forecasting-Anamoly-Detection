# Anomaly Detection Methods

## Introduction
Anomaly detection is the process of identifying unusual or unexpected observations in a dataset that differ significantly from normal patterns. In supply chain analytics, 
anomaly detection helps identify abnormal sales, inventory shortages, unexpected demand spikes, supplier delays, pricing errors, and stock imbalances. Detecting these 
anomalies enables businesses to make informed decisions and improve inventory management.

# 1. Z-Score Anomaly Detection

## Overview:
Z-Score is a statistical technique used to identify outliers by measuring how far a data point is from the dataset's mean in terms of standard deviations.

### Formula:
Z = (X − μ) / σ
Where:
- X = Data value
- μ = Mean
- σ = Standard deviation
A data point is generally considered an anomaly if:
- Z > 3
- Z < -3

## Advantages
- Simple and easy to implement.
- Works well for normally distributed data.
- Fast computation.

## Limitations
- Sensitive to extreme values.
- Assumes normal distribution.
- Less effective for skewed datasets.

# 2. Interquartile Range (IQR) Anomaly Detection

## Objective:
Implement the Interquartile Range (IQR) method to identify unusual values in the retail inventory dataset.

## Overview:
The IQR method detects anomalies by calculating the spread of the middle 50% of the data.

The following values are calculated:
- First Quartile (Q1)
- Third Quartile (Q3)
- Interquartile Range (IQR)

## Formula:
IQR = Q3 − Q1
Lower Bound = Q1 − (1.5 × IQR)
Upper Bound = Q3 + (1.5 × IQR)
Any observation outside these bounds is considered an anomaly.

## Implementation
- Calculated Q1 and Q3.
- Computed the Interquartile Range.
- Determined lower and upper thresholds.
- Flagged anomalies using the calculated limits.
- Created the **IQR_Anomaly** column.

## Advantages
- Does not require normally distributed data.
- Easy to understand.
- Robust against extreme values.
- Suitable for skewed datasets.

## Limitations
- Works mainly with numerical features.
- May not detect complex anomaly patterns.

# 3. Isolation Forest

## Objective
Implement Isolation Forest to identify anomalies using a machine learning approach.

## Overview
Isolation Forest is an unsupervised machine learning algorithm specifically designed for anomaly detection. Instead of profiling normal observations, it isolates 
anomalies through random partitioning of the data.Since anomalous observations are rare and significantly different from normal records, they require fewer random splits to become isolated.

## Implementation
- Trained the Isolation Forest model.
- Predicted anomaly labels.
- Converted predictions into binary values.
- Created the **IF_Anomaly** column.

## Advantages
- Works well on large datasets.
- Detects complex anomaly patterns.
- Does not require labeled data.
- Efficient and scalable.

## Limitations
- Requires parameter tuning.
- Less interpretable than statistical methods.

# 4. Comparison of IQR and Isolation Forest
| Feature | IQR | Isolation Forest |
|---------|-----|------------------|
| Method Type | Statistical | Machine Learning |
| Data Distribution | No assumption | No assumption |
| Complexity | Simple | Moderate |
| Suitable for Large Data | Moderate | Excellent |
| Detects Complex Patterns | No | Yes |
| Computational Cost | Low | Medium |

## Observation
The IQR method effectively identifies obvious statistical outliers, while Isolation Forest can detect more subtle and complex anomalies that may not be identified using traditional 
statistical techniques.Using both methods provides a more comprehensive understanding of unusual inventory and sales patterns.

# 5. Business Applications
Anomaly detection plays a vital role in supply chain and inventory management.
Common business scenarios include:
- Unexpected demand spikes during festivals or promotions.
- Stock shortages caused by supplier delays.
- Overstock situations due to inaccurate demand forecasting.
- Pricing inconsistencies.
- Inventory recording errors.
- Unusual purchasing behavior.
Early detection of these anomalies helps organizations improve forecasting accuracy, reduce operational costs, and optimize inventory levels.

# Conclusion

In this project, the Interquartile Range (IQR) and Isolation Forest methods were implemented to detect anomalies in the retail inventory dataset. The IQR method provides a 
simple statistical approach for identifying outliers, while Isolation Forest offers a machine learning solution capable of detecting more complex anomalies.
Combining statistical and machine learning techniques improves anomaly detection performance and provides valuable insights for inventory optimization and demand planning.
