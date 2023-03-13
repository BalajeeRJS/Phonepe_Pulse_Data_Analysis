import os
import json
import pandas as pd
import sqlconnect

mydb = sqlconnect.db_connection()

mycursor = mydb.cursor()
#mycursor.execute("select version()")



#===================================================================> AGGREGATED TRANSACTION STATE LEVEL <============================================================================================
insert_data=[]
#Run only one time to create table
mycursor.execute("CREATE TABLE aggregated_transaction (state VARCHAR(100), year VARCHAR(5),quater INT(2),Transaction_type VARCHAR(100),Transaction_count VARCHAR(255),Transaction_amount VARCHAR(255))")


path1 = "H:/Phone_Pulse/pulse/data/aggregated/transaction/country/india/state/"

Agg_state_list = os.listdir(path1)


for i in Agg_state_list:
    p_i = path1 + i + "/"
    Agg_yr = os.listdir(p_i)

    for j in Agg_yr:
        p_j = p_i + j + "/"
        Agg_yr_list = os.listdir(p_j)

        for k in Agg_yr_list:
            p_k = p_j + k
            # print(p_k)
            Data = open(p_k, 'r')
            A = json.load(Data)
            
            for z in A['data']['transactionData']:
                Name = z['name']
                count = z['paymentInstruments'][0]['count']
                amount = z['paymentInstruments'][0]['amount']
                qtr=int(k.strip('.json'))
                combined_data=(i,j,qtr,Name,count,amount)
                insert_data.append(combined_data)
#print(insert_data)
sql_trns="INSERT INTO aggregated_transaction (state,year,quater,Transaction_type,Transaction_count,Transaction_amount)  VALUES (%s, %s, %s, %s, %s, %s)"
mycursor.executemany(sql_trns, insert_data)
mydb.commit()
print(mycursor.rowcount, "was inserted.")


#=============================================================> AGGREGATED USER STATE LEVEL <===========================================================================================
insert_data=[]
#Run only one time to create table
mycursor.execute("CREATE TABLE aggregated_user (state VARCHAR(50), year VARCHAR(5),quater INT(2),brand_type VARCHAR(100),count VARCHAR(255),Percentage VARCHAR(255))")

path2 = "H:/Phone_Pulse/pulse/data/aggregated/user/country/india/state/"
user_list = os.listdir(path2)

for i in user_list:
    p_i = path2 + i + "/"
    Agg_yr = os.listdir(p_i)

    for j in Agg_yr:
        p_j = p_i + j + "/"
        Agg_yr_list = os.listdir(p_j)

        for k in Agg_yr_list:
            p_k = p_j + k
            # print(p_k)
            Data = open(p_k, 'r')
            B = json.load(Data)
            try:
              for w in B["data"]["usersByDevice"]:
                    brand_name = w["brand"]
                    count_ = w["count"]
                    ALL_percentage = w["percentage"]
                    qtr=int(k.strip('.json'))
                    combined_data=(i,j,qtr,brand_name,count_,ALL_percentage)
                    insert_data.append(combined_data)
            except:
                pass
sql_user="INSERT INTO aggregated_user (state,year,quater,brand_type,count,Percentage)  VALUES (%s, %s, %s, %s, %s, %s)"
mycursor.executemany(sql_user, insert_data)
mydb.commit()           

print(mycursor.rowcount, "was inserted.")

#================================================================> MAP TRANSACTION STATE LEVEL <========================================================================
insert_data=[]   

#Run only one time to create table
mycursor.execute("CREATE TABLE map_transaction (state VARCHAR(50), year VARCHAR(5),quater INT(2),District VARCHAR(100),count VARCHAR(255),amount VARCHAR(255))")

path3 = "H:/Phone_Pulse/pulse/data/map/transaction/hover/country/india/state/"
hover_list = os.listdir(path3)

for i in hover_list:
    p_i = path3 + i + "/"
    Agg_yr = os.listdir(p_i)

    for j in Agg_yr:
        p_j = p_i + j + "/"
        Agg_yr_list = os.listdir(p_j)

        for k in Agg_yr_list:
            p_k = p_j + k
            # print(p_k)
            Data = open(p_k, 'r')
            C = json.load(Data)
            for x in C["data"]["hoverDataList"]:
                District = x["name"]
                count = x["metric"][0]["count"]
                amount = x["metric"][0]["amount"]
                qtr=int(k.strip('.json'))
                combined_data=(i,j,qtr,District,count,amount)
                insert_data.append(combined_data)


sql_maptrns="INSERT INTO map_transaction (state,year,quater,District,count,amount)  VALUES (%s, %s, %s, %s, %s, %s)"
mycursor.executemany(sql_maptrns, insert_data)
mydb.commit()           

print(mycursor.rowcount, "was inserted.")


#==================================================================> MAP USER STATE LEVEL <===========================================================================
insert_data=[]
#Run only one time to create table
mycursor.execute("CREATE TABLE map_user (state VARCHAR(50), year VARCHAR(5),quater INT(2),District VARCHAR(100),registereduser VARCHAR(255))")

path4 = "H:/Phone_Pulse/pulse/data/map/user/hover/country/india/state/"
map_list = os.listdir(path4)

for i in map_list:
    p_i = path4 + i + "/"
    Agg_yr = os.listdir(p_i)

    for j in Agg_yr:
        p_j = p_i + j + "/"
        Agg_yr_list = os.listdir(p_j)

        for k in Agg_yr_list:
            p_k = p_j + k
            # print(p_k)
            Data = open(p_k, 'r')
            D = json.load(Data)

            for u in D["data"]["hoverData"].items():
                district = u[0]
                registereduser = u[1]["registeredUsers"]
                qtr=int(k.strip('.json'))
                combined_data=(i,j,qtr,district,registereduser)
                insert_data.append(combined_data)

sql_mapuser="INSERT INTO map_user (state,year,quater,District,registereduser)  VALUES (%s, %s, %s, %s, %s)"
mycursor.executemany(sql_mapuser, insert_data)
mydb.commit()           

print(mycursor.rowcount, "was inserted.")


#======================================================================> TOP TRANSACTION STATE LEVEL <================================================================================================
insert_data=[]
#Run only one time to create table
mycursor.execute("CREATE TABLE top_transaction (state VARCHAR(50), year VARCHAR(5),quater INT(2),District VARCHAR(100),Transaction_count VARCHAR(255),Transaction_amount VARCHAR(255))")

path5 = "H:/Phone_Pulse/pulse/data/top/transaction/country/india/state/"
TOP_list = os.listdir(path5)

for i in TOP_list:
    p_i = path5 + i + "/"
    Agg_yr = os.listdir(p_i)

    for j in Agg_yr:
        p_j = p_i + j + "/"
        Agg_yr_list = os.listdir(p_j)

        for k in Agg_yr_list:
            p_k = p_j + k
            # print(p_k)
            Data = open(p_k, 'r')
            E = json.load(Data)
            for z in E['data']['districts']:
                Name = z['entityName']
                count = z['metric']['count']
                amount = z['metric']['amount']
                qtr=int(k.strip('.json'))
                combined_data=(i,j,qtr,Name,count,amount)
                insert_data.append(combined_data)

sql_toptrns="INSERT INTO top_transaction (state,year,quater,District,Transaction_count,Transaction_amount)  VALUES (%s, %s, %s, %s, %s,%s)"
mycursor.executemany(sql_toptrns, insert_data)
mydb.commit()  
print(mycursor.rowcount, "was inserted.")

      
#=======================================================================> TOP USER STATE LEVEL <=================================================================================
insert_data=[] 
#Run only one time to create table
mycursor.execute("CREATE TABLE top_user (state VARCHAR(50), year VARCHAR(5),quater INT(2),District VARCHAR(100),registeredUser VARCHAR(255))")

path6 = "H:/Phone_Pulse/pulse/data/top/user/country/india/state/"
USER_list = os.listdir(path6)

for i in USER_list:
    p_i = path6 + i + "/"
    Agg_yr = os.listdir(p_i)

    for j in Agg_yr:
        p_j = p_i + j + "/"
        Agg_yr_list = os.listdir(p_j)

        for k in Agg_yr_list:
            p_k = p_j + k
            # print(p_k)
            Data = open(p_k, 'r')
            F = json.load(Data)
            for t in F['data']['districts']:
                Name = t['name']
                registeredUser = t['registeredUsers']
                qtr=int(k.strip('.json'))
                combined_data=(i,j,qtr,Name,registeredUser)
                insert_data.append(combined_data)

sql_topuser="INSERT INTO top_user (state,year,quater,District,registeredUser)  VALUES (%s, %s, %s, %s, %s)"
mycursor.executemany(sql_topuser, insert_data)
mydb.commit()  
print(mycursor.rowcount, "was inserted.")

#==========> CLOSING DB CONNECTION <==================
mycursor.close()
mydb.close()

