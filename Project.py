import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns


data = pd.read_csv("insurance.csv")

# Langkah #1 - Analisa Descriptive Statistic

# 1 1. Rata2 umur pengguna
age_mean = data["age"].mean()
print("1. Rata2 umur pengguna =", age_mean)

# 2 2. Rata-rata nilai BMI dari pengguna yang merokok
bmi_smoker_mean = data.loc[data['smoker'] == 'yes', 'bmi'].mean()
print("2. Rata-rata nilai BMI dari pengguna yang merokok =", bmi_smoker_mean)

# 3 5. Apakah variansi dari data charges perokok dan non perokok sama?
var_smoker = np.var(data.loc[data['smoker'] == "yes", 'charges'])
var_nonsmoker = np.var(data.loc[data['smoker'] == "no", 'charges'])
print("3.", var_smoker, var_nonsmoker, "sama?",
      var_smoker.round == var_nonsmoker.round)

# 4 6. Apakah rata rata umur perempuan dan laki-laki yang merokok sama?
age_male_mean = data.loc[(data['smoker'] == "yes") &
                         (data["sex"] == "male"), 'age'].mean()
age_female_mean = data.loc[(data['smoker'] == "yes")
                           & (data["sex"] == "female"), 'age'].mean()
print("4.", age_male_mean, age_female_mean, "sama? selisih",
      (age_male_mean) - (age_female_mean))

# 5 7. Mana yang lebih tinggi, rata rata tagihan kesehatan perokok atau non merokok?
charges_smoker_mean = data.loc[data['smoker'] == "yes", 'charges'].mean()
charges_nonsmoker_mean = data.loc[data['smoker'] == "no", 'charges'].mean()
print("5.", charges_smoker_mean, charges_nonsmoker_mean,
      "tagihan kesehatan perokok lebih besar?", charges_smoker_mean > charges_nonsmoker_mean ,"\n")

# Langkah #2 - Analisa Variabel Kategorik (PMF)

# 1 1. Gender mana yang memiliki tagihan paling tinggi?
max_charge_male = data.loc[data['sex'] == "male", "charges"].max()
max_charge_female = data.loc[data['sex'] == "female", "charges"].max()
print("1.","Pria:",max_charge_male,"Wanita:",max_charge_female,)

# 2 4. Mana yang lebih tinggi proporsi perokok atau non perokok?
proportion_smoker=data.loc[(data['smoker'] == "yes"),data.columns[0]].count()/len(data)
proportion_nonsmoker=data.loc[(data['smoker'] == "no"),data.columns[0]].count()/len(data)
print("2.","smoker:",proportion_smoker,"nonsmoker:",proportion_nonsmoker)

# 3 5. Berapa peluang seseorang tersebut adalah perempuan diketahui dia adalah perokok?
p_female_smoker=data.loc[(data['smoker'] == "yes")&(data['sex'] == "female"),data.columns[0]].count()/data.loc[(data['sex'] == "female"),data.columns[0]].count()
print("3. p female smokers:",p_female_smoker)

# 4 6. Berapa peluang seseorang tersebut adalah laki-laki diketahui dia adalah perokok?
p_male_smoker=data.loc[(data['smoker'] == "yes")&(data['sex'] == "male"),data.columns[0]].count()/data.loc[(data['sex'] == "male"),data.columns[0]].count()
print("4. p male smokers:",p_male_smoker)

# 5 7. Bagaimana bentuk distribusi peluang besar tagihan dari tiap-tiap region?
plt.hist(data["charges"],weights=np.ones(len(data["charges"])) / len(data["charges"]))
plt.show()
print("\n")
# Langkah #3 - Analisa Variabel Kontinu

# 1 Mana yang lebih mungkin terjadi

# a. Seseorang dengan BMI diatas 25 mendapatkan tagihan kesehatan diatas 16.7k
BMI_morethan25= data.loc[(data['bmi'] > 25)&(data['charges'] > 16700),data.columns[0]].count()/data.loc[(data['bmi'] > 25),data.columns[0]].count()

# b. Seseorang dengan BMI dibawah 25 mendapatkan tagihan kesehatan diatas 16.7k
BMI_lessthan25= data.loc[(data['bmi'] < 25)&(data['charges'] > 16700),data.columns[0]].count()/data.loc[(data['bmi'] < 25),data.columns[0]].count()
print("1. a>b?",BMI_morethan25>BMI_lessthan25,"\n")

# Langkah #4 - Analisa Korelasi Variabel

#korelation heatmap
# datasmoker=data.loc[data['smoker'] == "no",data].corr()
corr=data[data['smoker']=="yes"].corr()
corr1=data[data['smoker']=="no"].corr()
fig, (ax1, ax2) = plt.subplots(1,2)
sns.heatmap(corr, cmap="YlGnBu", annot=True, 
        xticklabels=corr.columns,
        yticklabels=corr.columns, ax=ax1)
sns.heatmap(corr1, cmap="YlGnBu", annot=True, 
        xticklabels=corr1.columns,
        yticklabels=corr1.columns, ax=ax2)
ax1.set_title('Smokers')
ax2.set_title('Non-Smokers')
plt.show()

#Langkah #5 - Pengujian Hipotesis

# 1 1. Tagihan kesehatan perokok lebih tinggi daripada tagihan kesehatan non perokok
alpha=0.05
stat, p = stats.ttest_ind(a = data.loc[data['smoker'] == "yes", "charges"], b = data.loc[data['smoker'] == "no", "charges"], equal_var=False, alternative='less')
if p > alpha:
    print('1. Two group means are equal (Gagal tolak H0)') 
else:
    print('1. Two group means are different (Tolak H0)')

# 2 4. Tagihan kesehatan dengan BMI diatas 25 lebih tinggi daripada tagihan kesehatan dengan BMI dibawah 25
alpha=0.05
stat, p = stats.ttest_ind(a = data.loc[data['bmi'] > 25, "charges"], b = data.loc[data['bmi']<25, "charges"], equal_var=False, alternative='less')
if p > alpha:
    print('2. Two group means are equal (Gagal tolak H0)') 
else:
    print('2. Two group means are different (Tolak H0)')

# 3 5. Tagihan kesehatan laki-laki lebih besar dari perempuan
alpha=0.05
stat, p = stats.ttest_ind(a = data.loc[data['sex'] == "male", "charges"], b = data.loc[data['sex'] == "female", "charges"], equal_var=False, alternative='less')
if p > alpha:
    print('3. Two group means are equal (Gagal tolak H0)') 
else:
    print('3. Two group means are different (Tolak H0)')
    