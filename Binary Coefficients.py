list_day_col1=re.findall(r"([A-Z][a-z]+ [0-9]{1,2},.[0-9]{4})",full_str_filter)
word_list = re.split(r"([A-Z][a-z]+ [0-9]{1,2},.[0-9]{4})", full_str_filter)
word_list2=[]
for x in list_day_col1:
    word_list.remove(x)
word_list_final=[x.replace("\n","").replace("        ","") for x in word_list]
del word_list_final[0]
list_filter_apnic=[]
list_filter_arin=[]

for j in word_list_final:
    if re.search("APNIC".upper(),j.upper()):
        get_value=re.split("APNIC",j,flags=re.I)[1]
        if re.search("Under".upper(),get_value.upper()):
            get_value2=re.split("Under",get_value,flags=re.I)[0]
            list_filter_apnic.append(get_value2.replace("       ",""))
            continue
        else:
            list_filter_apnic.append(get_value.replace("       ",""))
            continue
    else:
        list_filter_apnic.append("no information")
        continue

for j in word_list_final:
    if re.search("arin".upper(),j.upper()):
        get_value=re.split("arin",j,flags=re.I)[1]
        if re.search("Under".upper(),get_value.upper()):
            get_value2=re.split("Under",get_value,flags=re.I)[0]
            list_filter_arin.append(get_value2.replace("       ",""))
            continue
        else:
            list_filter_arin.append(get_value.replace("       ",""))
            continue
    else:
        list_filter_arin.append("no information")
        continue
#print(len(list_filter_apnic))
col_name=["Data_Revised","Revisions","is_APNIC","is_ARIN","APNIC_IP","ARIN_IP"]
generate_dict_for_df={}
for col in range(len(col_name)):
    generate_dict_for_df[col_name[col]]=[]

for x in list_day_col1:
    generate_dict_for_df['Data_Revised'].append(x)
for x in word_list_final:
    generate_dict_for_df['Revisions'].append(x)
for x in list_filter_apnic:
    generate_dict_for_df['APNIC_IP'].append(x)
for x in list_filter_arin:
    generate_dict_for_df['ARIN_IP'].append(x)
for x in range(len(list_day_col1)):
    generate_dict_for_df['is_APNIC'].append(0)
for x in range(len(list_day_col1)):
    generate_dict_for_df['is_ARIN'].append(0)

final_df = pd.DataFrame({ key:pd.Series(value) for key, value in generate_dict_for_df.items() })
final_df.loc[(final_df['APNIC_IP']!='no information'),'is_APNIC']="1"
final_df.loc[(final_df['ARIN_IP'] !='no information'),'is_ARIN']="1"


################################### fix filter unstructured data ####################################################
for index, row in final_df.iterrows():
    if final_df.loc[index, 'ARIN_IP']!="no information":
        arin_fix_str=str(final_df.loc[index, 'ARIN_IP']).split(":")
        for j in arin_fix_str:
            if re.search(r"\d{1,4}.\d{1,4}.\d{1,4}.\d{1,4}\W\d{1,3}",j):
                fix_str='|'.join(re.findall(r"\d{1,4}.\d{1,4}.\d{1,4}.\d{1,4}\W\d{1,3}",j))
                final_df.loc[index, 'ARIN_IP'] = fix_str
                break
    #if re.search(r"arin",final_df.loc[index, 'Revisions'],flags=re.I):
    if final_df.loc[index, 'ARIN_IP']!="no information" and len(final_df.loc[index, 'ARIN_IP']) < 8:
        arin_fix_str=''.join(re.split('arin',final_df.loc[index, 'Revisions'],flags=re.I)[1:])
        arin_fix_str=arin_fix_str.split(":")
        #print(arin_fix_str)
        for j in arin_fix_str:
            if re.search(r"\d{1,4}.\d{1,4}.\d{1,4}.\d{1,4}\W\d{1,3}",j):
                fix_str='|'.join(re.findall(r"\d{1,4}.\d{1,4}.\d{1,4}.\d{1,4}\W\d{1,3}",j))
                #print(fix_str)
                final_df.loc[index, 'ARIN_IP'] = fix_str
                break
 
for index, row in final_df.iterrows():
    #if re.search(r"arin",final_df.loc[index, 'Revisions'],flags=re.I):
    if final_df.loc[index, 'APNIC_IP']!="no information":
        apnic_str=str(final_df.loc[index, 'APNIC_IP']).split(":")
        print(apnic_str ,"\n\n")
        for j in apnic_str:
            if re.search(r"\d{1,4}.\d{1,4}.\d{1,4}.\d{1,4}\W\d{1,3}",j):
                fix_str='|'.join(re.findall(r"\d{1,4}.\d{1,4}.\d{1,4}.\d{1,4}\W\d{1,3}",j))
                final_df.loc[index, 'APNIC_IP'] = fix_str
                print(fix_str)
                break
    if final_df.loc[index, 'APNIC_IP']!="no information" and len(final_df.loc[index, 'APNIC_IP']) < 8:
        apnic_str=''.join(re.split('apnic',final_df.loc[index, 'Revisions'],flags=re.I)[1:])
        apnic_str=apnic_str.split(":")
        for j in arin_fix_str:
            if re.search(r"\d{1,4}.\d{1,4}.\d{1,4}.\d{1,4}\W\d{1,3}",j):
                fix_str='|'.join(re.findall(r"\d{1,4}.\d{1,4}.\d{1,4}.\d{1,4}\W\d{1,3}",j))
                #print(fix_str)
                final_df.loc[index, 'APNIC_IP'] = fix_str
                break


today = datetime.today().strftime('%Y-%m-%d')
final_df["datetime"]=today
final_df['Data_Revised']=final_df['Data_Revised'].apply(lambda x: str(' '.join(str(x).split(", ")[0:])).replace(" ","-"))
print(final_df)
final_df.to_csv('testcsv.csv',index=False)
