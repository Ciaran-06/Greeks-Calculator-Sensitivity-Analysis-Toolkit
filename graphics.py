import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="white")

df = pd.read_csv('./data/calculated/sensitivity_by_moneyness.csv')
df = df.set_index('moneyness_bin')

df_means = df[['delta_mean', 'vega_mean', 'theta_mean', 'gamma_mean', 'rho_mean']]
sns.heatmap(df_means, annot=True, fmt='.2f', cmap='coolwarm', cbar_kws={'label': 'Value'})
plt.title('Greeks Sensitivity by Moneyness')
plt.ylabel('Moneyness Bin')
plt.xlabel('Greek')
plt.tight_layout()
plt.savefig('./data/graphics/greeks_sensitivity_heatmap.png', dpi=300)
plt.show()