import pandas as pd

pd_veri = pd.read_excel('KMOIpdveri.xlsx', index_col=0)
harf_sayısı = pd_veri.groupby('Cevap').count()[['Durum']]


#Her soruda cıkan harf sayısı
columns_names=["Soru1","Soru2","Soru3","Soru4","Soru5","Soru6","Soru7","Soru8","Soru9","Soru10","Soru11","Soru12"]
index_names = ["A","B","C","D"]
dfsorucevap = pd.DataFrame(columns=columns_names,index=index_names)

for i in range(12,0,-1):
    temp = (pd_veri[pd_veri.Soru_no == (i)].iloc[:,1]).value_counts() 
    if "A" in temp.index:
        dfsorucevap.loc["A",:"Soru"+str(i)] = temp.loc["A"]
    if "B" in temp.index:
        dfsorucevap.loc["B",:"Soru"+str(i)] = temp.loc["B"]    
    if "C" in temp.index:
        dfsorucevap.loc["C",:"Soru"+str(i)] = temp.loc["C"]    
    if "D" in temp.index:
        dfsorucevap.loc["D",:"Soru"+str(i)] = temp.loc["D"]
        
#Harflerin sorulara göre çıkma olasılığı
columns_names=["Soru1","Soru2","Soru3","Soru4","Soru5","Soru6","Soru7","Soru8","Soru9","Soru10","Soru11","Soru12"]
index_names = ["A","B","C","D"]
cevapolasılık = pd.DataFrame(columns=columns_names,index=index_names)
for ind in range(0,4):
    for col in range(0,12):
        if type(dfsorucevap.iloc[ind,col]) == int:
            adet = dfsorucevap.iloc[ind,col]
            sum_col = dfsorucevap.iloc[:,col].sum()
            cevapolasılık.iloc[ind,col] = (adet/sum_col)*100
            
#Görselleştirme

title=cevapolasılık.plot(kind="bar",figsize=(20,5))
title.set_title("Cevapların Sorulara Göre Yüzdesel Dağılımı")

title2=dfsorucevap.plot(kind="bar",figsize=(20,5))
title2.set_title("Cevapların Sorulara Göre Adetleri")
            