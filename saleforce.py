from bs4 import BeautifulSoup #install pip BeautifulSoup / Bs4
import pandas as pd
import re
import datetime
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import time
from datetime import datetime,timedelta

url='https://help.salesforce.com/s/articleView?id=000321501&type=1'


################ REQUEST ZONE ##################################
for i in range(5):
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)

        driver.maximize_window()
        driver.get(url)
        time.sleep(3)
        y = 1000
        for timer in range(0,10): #cd mouse score-down for download full script js
            driver.execute_script("window.scrollTo(0, "+str(y)+")")
            y += 1000  
            time.sleep(1)
        time.sleep(6)
        html = driver.execute_script('return document.documentElement.outerHTML')
        soup = BeautifulSoup(html,'html.parser')
        data = soup.findAll("tr")
        if data:
            driver.close()
            print("############# get data from js web ###############")
            break
    except:
        print("########### connection errors #################")
        driver.close()
        pass

##################################################################
#html=html.split("Revisions made approximately within the past 6 months")[:1]

list_all_data=[]
for i,x in enumerate(data):
   #print(i,x.text,"#######################\n")
   list_all_data.append(x.text)
   if re.search("Revisions",x.text):
       index_frist=i

list_all_data=list_all_data[index_frist+1:]


full_str_filter=str(''.join(list_all_data))
#final_list_all_data=full_str_filter.split("Added to")[0:]

#for i,x in enumerate(final_list_all_data):
#    print(i,x,"\n\n")

#print(full_str_filter)
list_day_col1=re.findall(r"([A-Z][a-z]+ [0-9]{1,2},.[0-9]{4})",full_str_filter)

word_list = re.split(r"([A-Z][a-z]+ [0-9]{1,2},.[0-9]{4})", full_str_filter)

word_list2=[]
for x in list_day_col1:
    word_list.remove(x)


word_list_final=[x.replace("\n","").replace("        ","") for x in word_list]

del word_list_final[0]

#for i in word_list_final:
#    print(i,"\n\n\n\n")

list_filter_apnic=[]
for j in word_list_final:
    if re.search("Under APNIC".upper(),j.upper()):
        get_value=re.split("Under APNIC",j,flags=re.I)[1]
        if re.search("Under".upper(),get_value.upper()):
            get_value2=re.split("Under",get_value,flags=re.I)[0]
            list_filter_apnic.append(get_value2.replace("       ",""))
        else:
            list_filter_apnic.append(get_value.replace("       ",""))
    else:
        list_filter_apnic.append("no information")


#print(len(list_filter_apnic))


col_name=["Data_Revised","Revisions","Apnic_ip","flag"]
generate_dict_for_df={}
for col in range(len(col_name)):
    generate_dict_for_df[col_name[col]]=[]

for x in list_day_col1:
    generate_dict_for_df['Data_Revised'].append(x)
for x in word_list_final:
    generate_dict_for_df['Revisions'].append(x)
for x in list_filter_apnic:
    generate_dict_for_df['Apnic_ip'].append(x)

final_df = pd.DataFrame({ key:pd.Series(value) for key, value in generate_dict_for_df.items() })
final_df.loc[(final_df['Apnic_ip']=='no information'),'flag']="N"
final_df.loc[(final_df['Apnic_ip'] !='no information'),'flag']="Y"

today = datetime.today().strftime('%Y-%m-%d')
final_df["datetime"]=today

final_df['Data_Revised']=final_df['Data_Revised'].apply(lambda x: str(' '.join(str(x).split(", ")[0:])).replace(" ","-"))
final_df.to_csv("test_sale_force2.csv",index=False)
