import pandas as pd

df = pd.read_csv("data/shopping_trends.csv")
df.columns = df.columns.str.strip()

def spending_cat(amount):
        if amount >= 93:
           return "Very High"
        elif amount >= 60:
            return "High"
        elif amount >= 50:
            return "Medium"
        elif amount >= 30:
            return "Low"
        else:
            return "Very Low"
df["spend_category"] = df["Purchase Amount (USD)"].apply(spending_cat)
print("A large portion of customers fall into the “High spend” category")

def frequency_cat(no):
    if no in ["Weekly", "Bi-Weekly", "Fortnightly"]:
        return "High"
    elif no in ["Monthly", "Every 3 Months"]:
        return "Medium"
    elif no in ["Quarterly", "Annually"]:
        return "Low"
df["frequency_category"] = df["Frequency of Purchases"].apply(frequency_cat)
print("High-frequency customers form the largest group, indicating strong repeat engagement across a significant portion of users.")

print("Since many customers are both frequent and moderate/high spenders, retention strategies may yield better ROI than aggressive acquisition.")
print("High-frequency, low-spend customers represent a strong target for upselling through bundled offers.")            

def vs(row):
   return row["Purchase Amount (USD)"]*row["Previous Purchases"] 
df["value_score"] = df.apply(vs, axis=1)

q1 = df["value_score"].quantile(0.25)
q2 = df["value_score"].quantile(0.5)
q3 = df["value_score"].quantile(0.75)
q4 = df["value_score"].quantile(0.9)

def value_cat(score):
    if score >= q4:
        return "High Score"
    elif score >= q3:
        return "Above Average Score"
    elif score >= q2:
        return "Average Score"
    else:
        return "Low Score"
df["value_category"] = df["value_score"].apply(value_cat)
print(df["value_category"].value_counts())

def assign_segment(row):
    if row["value_category"] == "High Score":
        if row["frequency_category"] == "Low":
            return "Infrequent Premium"
        else:
            return "High Value Customer"
    
    elif row["value_category"] == "Above Average Score":
        if row["frequency_category"] == "High":
            return "Loyal Customer"
        else:
            return "Regular Customer"
    
    elif row["value_category"] == "Low Score":
        if row["frequency_category"] == "High":
            return "Frequent Low Value"
        else:
            return "Low Engagement"
    
    else:
        return "Regular Customer"
df["segment"] = df.apply(assign_segment, axis=1)
