import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/sales_data.csv')
df['revenue'] = df['units_sold'] * df['price']

print('Total Revenue:', df['revenue'].sum())
print('Top Product:', df.groupby('product')['revenue'].sum().idxmax())
print('Top Region:', df.groupby('region')['revenue'].sum().idxmax())

df.groupby('product')['revenue'].sum().plot(kind='bar', title='Revenue by Product')
plt.xlabel('Product')
plt.ylabel('Revenue')
plt.tight_layout()
plt.show()