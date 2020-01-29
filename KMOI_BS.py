import requests
from bs4 import BeautifulSoup
import pandas as pd
list = []
cvplist = []
durum =[]
#Soruların var olduğu link alınır.
def link(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content,"html.parser")
    gelen_veri = soup.find_all("div",{"Question__text hyphenate"})

    for i in range(len(gelen_veri)):
        st= str(gelen_veri[i])
        start=st.find("href")
        finish=st.find("-soru")
        list.append(st[start+5:finish+6])

#Sorulardan doğru cevabı ve yarışmacının durumu alınır.
def cevap(url2):
    r = requests.get(url2)
    soup = BeautifulSoup(r.content,"html.parser")
    gelen_veri = soup.find_all("div",{"class":"Multiple__choices Multiple__right_answer"})
    gelen_veri2 = soup.find("div",{"class":"Details hyphenate"})
    gelen_veri2= gelen_veri2.find("p")
    
    if "Details__title elendi" in str(gelen_veri2):
        durum.append("elendi")
    elif "Details__title bildi" in str(gelen_veri2):
        durum.append("bildi")
    else :
        durum.append("cekildi")
    b=str(gelen_veri)
    cvplist.append(b[87])
url ="https://milyonist.com/tv/milyoner/butun/sorular?sayfa="

for i in range(1,2):
    link((url + str(i)))

for i in range(len(list)):
    url2 = list[i][1:-1]
    cevap(str(url2))

soru_no=[]
for i in range(len(list)):
    soru_no.append(list[i][-7:-6])



dict = {"Soru_no":(soru_no),"Cevap":(cvplist),"Durum":(durum)}
pd_veri = pd.DataFrame(dict)

#Hangi harften kaç tane var 
harf_sayısı = pd_veri.groupby('Cevap').count()[['Durum']]


#Her soruda cıkan harf sayısı 
columns_names=["Soru1","Soru2","Soru3","Soru4","Soru5","Soru6","Soru7","Soru8","Soru9","Soru10","Soru11","Soru12"]
index_names = ["A","B","C","D"]
dfsorucevap = pd.DataFrame(columns=columns_names,index=index_names)

for i in range(12,0,-1):
    temp = (pd_veri[pd_veri.Soru_no == str(i)].iloc[:,1]).value_counts()
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










        


















