import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')

class FinancialAI:
    def __init__(self):
# basic income and expense categories
        self.income_categories = ['Salary', 'Business', 'Investment', 'Freelance', 'Other Income']
        self.expense_categories = ['Food', 'Transport', 'Entertainment', 'Shopping', 'Bills', 'Healthcare', 'Education', 'Other']

# Generate simple financial insights

    def get_insights(self, df):
        """Return simple financial insights"""
        if df.empty:
            print("No transaction data yet")  # debug
            return {}

        insights = {}

# convert date column

        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M')


# calculate totals

        try:
            total_income = df[df['type']=='income']['amount'].sum()
            total_expense = df[df['type']=='expense']['amount'].sum()
        except:
            total_income = 0
            total_expense = 0

# savings rate

        savings_rate = ((total_income - total_expense)/total_income*100) if total_income>0 else 0

        insights['total_income'] = round(total_income,2)
        insights['total_expense'] = round(total_expense,2)
        insights['savings_rate'] = round(savings_rate,2)
        insights['net_worth'] = round(total_income - total_expense,2)

# monthly trend

        monthly = df.groupby(['month','type'])['amount'].sum().unstack(fill_value=0)
        if not monthly.empty and len(monthly)>1:
            try:
                insights['income_trend'] = 'up' if monthly['income'].iloc[-1] > monthly['income'].iloc[-2] else 'down'
                insights['expense_trend'] = 'up' if monthly['expense'].iloc[-1] > monthly['expense'].iloc[-2] else 'down'
            except:
                pass  # sometimes income or expense column may not exist

# largest expense category

        exp_by_cat = df[df['type']=='expense'].groupby('category')['amount'].sum()
        if not exp_by_cat.empty:
            largest_cat = exp_by_cat.idxmax()
            largest_amt = exp_by_cat.max()
            insights['largest_expense_category'] = f"{largest_cat} (${largest_amt:.2f})"

# recommendations

        recs = []
        if savings_rate<20:
            recs.append("💡 Try to save at least 20% of your income")
        if total_expense > total_income*0.8:
            recs.append("⚠️ Your expenses are high compared to income")
        if len(recs)==0:
            recs.append("✅ Good job! Keep managing your money well")

        insights['recommendations'] = recs

        return insights

# Predict next months expenses

    def predict_future_spending(self, df, months=3):
        """Simple linear regression prediction"""
        if df.empty:
            print("No data to predict")  # debug
            return {}

        preds = {}
        try:
            df['date'] = pd.to_datetime(df['date'])
            monthly_exp = df[df['type']=='expense'].groupby(pd.Grouper(key='date', freq='M'))['amount'].sum().reset_index()

            if len(monthly_exp) > 1:
                monthly_exp['month_idx'] = range(len(monthly_exp))
                X = monthly_exp[['month_idx']]
                y = monthly_exp['amount']

                model = LinearRegression()
                model.fit(X, y)

                future_idx = [[len(monthly_exp)+i] for i in range(months)]
                future_vals = model.predict(future_idx)

                preds['next_month_prediction'] = round(max(future_vals[0],0),2)
                preds['trend'] = 'upward' if model.coef_[0]>0 else 'downward'
            else:
                preds['note'] = "Not enough past data to predict"
        except:
            preds['error'] = "Prediction failed (check data)"

        return preds

# Category breakdown

    def get_category_breakdown(self, df):
        """Return expense breakdown by category"""
        if df.empty:
            return []

        exp_df = df[df['type']=='expense']
        cat_totals = exp_df.groupby('category')['amount'].sum().reset_index()
        cat_totals['percentage'] = (cat_totals['amount']/cat_totals['amount'].sum()*100).round(2)

        return cat_totals.to_dict('records')

# Detect unusual spending

    def detect_anomalies(self, df):
        """Return transactions that are unusually high"""
        if df.empty:
            return []

        anomalies = []
        exp_df = df[df['type']=='expense']

        if len(exp_df)>0:
            mean_val = exp_df['amount'].mean()
            std_val = exp_df['amount'].std()
            unusual = exp_df[exp_df['amount']>mean_val + 2*std_val]

            for _, t in unusual.iterrows():
                anomalies.append({
                    'date': t['date'],
                    'amount': t['amount'],
                    'category': t['category'],
                    'description': t['description']
                })

        return anomalies
