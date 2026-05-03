import pandas as pd
import plotly.express as px
import argparse #It lets the program take input from the command line

#========================= FEATURE ENGINEERING =========================
# Spend Category
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
    
# Frequency Category
def frequency_cat(freq):
    if freq in ["Weekly", "Bi-Weekly", "Fortnightly"]:
        return "High"
    elif freq in ["Monthly", "Every 3 Months"]:
        return "Medium"
    else:
        return "Low"
# Value Score
def compute_value_score(row):
    return row["Purchase Amount (USD)"] * row["Previous Purchases"]



# ========================= SEGMENTATION =========================
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

    return "Regular Customer"

# ========================= ACTIONS =========================
def get_recommended_action(row):
    if row["segment"] == "High Value Customer":
        if row["priority"] == "Priority 1":
            return "VIP Treatment"
        elif row["priority"] == "Priority 2": 
            return "Offer premium membership or exclusive deals"
        else:
            return "Maintain Customer"
    elif row["segment"] == "Frequent Low Value":
        if row["priority"] =="Priority 1":
            return "Surprising case. Investigate."
        else:
            return "Encourage bundle purchases or upsell"
    elif row["segment"] == "Loyal Customer":
        if row["priority"] == "Priority 1":
            return "High-priority retention"
        else:
            return "Retention campaigns"
    elif row["segment"] in ["Infrequent Premium", "Low Engagement"]:
        return "Re-engagement campaigns"
    return "General Marketing"

# ========================= INSIGHT =========================
def generate_insight(row):
    return (
        f"Customer has a score of {row['final_score']:.2f}, placing them in {row['priority']}, "
        f"and is a {row['segment']} with {row['value_category']} value and {row['frequency_category']} frequency. "
        f"Recommended action: {row['recommended_action']}.")


def run_pipeline():
# ========================= LOAD DATA ========================= 
    df = pd.read_csv("data/shopping_trends.csv")
    df.columns = df.columns.str.strip()

# ========================= NUMERIC SCORING =========================
    spend_map = {"Very Low": 1, "Low": 2, "Medium": 3, "High": 4, "Very High": 5}
    freq_map = {"Low": 1, "Medium": 2, "High": 3}
    value_map = {"Low Score": 1, "Average Score": 2, "Above Average Score": 3, "High Score": 4}

# ========================= APPLY FEATURES =========================
    df["spend_category"] = df["Purchase Amount (USD)"].apply(spending_cat)
    df["frequency_category"] = df["Frequency of Purchases"].apply(frequency_cat)
    df["value_score"] = df.apply(compute_value_score, axis=1)
    
# ========================= VALUE CATEGORY (quantiles) =========================
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
    
    df["spend_score"] = df["spend_category"].map(spend_map)
    df["freq_score"] = df["frequency_category"].map(freq_map)
    df["value_score_num"] = df["value_category"].map(value_map)
    df["final_score"] = (df["spend_score"] * 0.4 + df["freq_score"] * 0.3 + df["value_score_num"] * 0.3)
    
# ========================= PRIORITY ========================
    q5 = df["final_score"].quantile(0.75)
    q6 = df["final_score"].quantile(0.9)
    def get_priority(score):
        if score >= q6:
            return "Priority 1"
        elif score >= q5:
            return "Priority 2"
        else:
            return "Priority 3"
    
    df["priority"] = df["final_score"].apply(get_priority)
    df["segment"] = df.apply(assign_segment, axis=1)
    df["recommended_action"] = df.apply(get_recommended_action, axis=1)
    df["insight"] = df.apply(generate_insight, axis=1)
    df_final = df[["Customer ID", "segment", "priority", "recommended_action","insight"]]
    
    # ========================= FINAL OUTPUT =========================
    top_customers = df.sort_values(by="final_score", ascending=False).head(10)
    print(top_customers[["Customer ID", "final_score", "priority"]])
    print(df.groupby("segment")["final_score"].mean())

    # ========================= VISUALIZATION =========================
    action_counts = df_final["recommended_action"].value_counts().reset_index()
    action_counts.columns = ["action", "count"]

    fig1 = px.pie(action_counts, values="count", names="action")
    fig1.show()

    priority_values= df_final["priority"].value_counts().reset_index()
    priority_values.columns = ["priority", "count"]
    fig2 = px.bar(priority_values, x="priority", y="count", title="Priority Distribution")
    fig2.show()
    
    df_final.to_csv("outputs/customer_insights.csv", index=False)
    return df_final

def show_customer_summary(df, customer_id):
    result = df[df["Customer ID"] == customer_id]
    
    if result.empty:
        print("Customer not found")
        return
    
    row = result.iloc[0]
    
    print("Customer ID:", row["Customer ID"])
    print("Segment:", row["segment"])
    print("Priority:", row["priority"])
    print("Insight:", row["insight"])
    
if __name__ == "__main__":
    df_final = run_pipeline()

    parser = argparse.ArgumentParser()
    parser.add_argument("--customer_id", type=int) #User can pass a number called customer_id
    args = parser.parse_args() #reads input

    if args.customer_id:
        show_customer_summary(df_final, args.customer_id) #args.customer id holds the value; this line uses it
    else:
        print(df_final.head())




