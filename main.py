import pandas as pd
import streamlit as st
import plotly.express as px
import sqlconnect
import warnings
warnings.filterwarnings("ignore")

#Comfiguring Streamlit GUI
st.set_page_config(page_title='Phonepe 2018-2022',
                   page_icon=':hash:',layout='wide')

#===============================================================>CONNECTING TO DATABASE<==============================================================
mydb = sqlconnect.db_connection()

mycursor = mydb.cursor()

st.markdown("<h1 style='text-align: center;color:#8000ff'>Phonepe 2018-2022 Data Analysis (INDIA)</h1>",
            unsafe_allow_html=True)
#=================================================================>TRANSACTIONS ANALYSIS<=============================================================
st.subheader('TRANSACTION ANALYSIS')
tab1, tab2, tab3 = st.tabs(["STATE ANALYSIS", "DISTRICT ANALYSIS","INDIA  ANALYSIS"])

with tab1:
     st.info('Payment mode wise Transaction count is shown for each Quarter of a Year', 
             icon="ℹ️")
     col1, col2, col3= st.columns(3)
     
     with col1:
        mode = st.selectbox('Please select the Payment Mode',
                            ('Recharge & bill payments',
                            'Peer-to-peer payments',
                            'Merchant payments', 
                            'Financial Services',
                            'Others'),key='a')
     with col2:
        state = st.selectbox('Please select the State',
                            ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                            'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                            'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                            'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
                            'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
                            'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                            'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
                            'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                            'uttarakhand', 'west-bengal'),key='b')
     with col3:
         year = st.selectbox('Please select the Year',
                             ('From 2018-2022','2018', '2019', '2020','2021','2022'),
                             key='y1')
     col1, col2= st.columns([1,2])
     with col1:
        State = state
        Mode = mode
        Year = year
        if Year=='From 2018-2022':
          mycursor.execute(f"select year,quater,Transaction_count from aggregated_transaction where Transaction_type='{Mode}' and state='{State}' ")
        else:
          mycursor.execute(f"select year,quater,Transaction_count from aggregated_transaction where Transaction_type='{Mode}' and state='{State}'and year='{Year}' ")
        df = pd.DataFrame(mycursor.fetchall(),columns=['Year','Quarter','Transaction_count'])
        st.dataframe(df)
     with col2:
         df = df.sort_values(by=['Year'])
         df["Quarter"] = "Q"+df['Quarter'].astype(str)
         df['Year_Quarter']=df['Year'].astype(str) +"-"+ df["Quarter"].astype(str)
         df['Transaction_count']=df['Transaction_count'].astype(int)
         fig = px.bar(df, x='Year_Quarter', y='Transaction_count',
                      color='Transaction_count',color_continuous_scale="thermal")
         st.plotly_chart(fig,use_container_width=True)
with tab2:
     st.info('District wise Transaction count is shown for each Quarter of a Year',
             icon="ℹ️")
     col1, col2, col3 = st.columns(3)
     with col1:
         Year_map = st.selectbox('Please select the Year',
                            ('2018', '2019', '2020','2021','2022'),key='y2')
     with col2:
         state_map = st.selectbox('Please select the State',
                                 ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                                  'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                                  'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                                  'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
                                  'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
                                  'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                                  'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
                                  'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                  'uttarakhand', 'west-bengal'),key='dk')
     with col3:
         mycursor.execute(f"select state,year,quater,District,count from map_transaction where state='{state_map}' and year='{Year_map}'")
         df = pd.DataFrame(mycursor.fetchall(),columns=['State','Year','Quarter','District','Transaction_count'])
         district_map = st.selectbox('Please select the District',
                                   df['District'].sort_values().unique())
     col1,col2=st.columns(2)
     with col1:
        
         selected_df = df.loc[(df['District'] == district_map )]
         st.dataframe(selected_df)
     with col2:
         selected_df['Quarter']='Quarter-'+selected_df['Quarter'].astype(str)
         selected_df['Transaction_count'] = selected_df['Transaction_count'].astype(int)
         fig = px.bar(selected_df, x='Quarter', y='Transaction_count',
                      color='Transaction_count',color_continuous_scale="Viridis")
         st.plotly_chart(fig,use_container_width=True)
with tab3:
     st.info('Total Transaction for each year in INDIA', icon="ℹ️")
     col1, col2=st.columns(2)
     with col1:
        Group_year = st.selectbox('Please select Group by',
                                 ('Group by Year','Group by Year and Quarter'),key='overall')
        if Group_year=='Group by Year':
          mycursor.execute("select year,sum(count),sum(amount) from map_transaction group by year")
          df = pd.DataFrame(mycursor.fetchall(),columns=['Year','Transaction_count','Transaction_amount'])
        else:
          mycursor.execute("select year,quater,sum(count),sum(amount) from map_transaction group by year,quater")
          df = pd.DataFrame(mycursor.fetchall(),columns=['Year','Quarter','Transaction_count','Transaction_amount'])

        st.dataframe(df)
     with col2:
        if Group_year=='Group by Year':
          fig1 = px.pie(df, values='Transaction_count', names='Year',
                        color_discrete_sequence=px.colors.sequential.Viridis,
                        title='TOTAL TRANSACTIONS (2018 TO 2022)')
          fig1.update_traces(textposition='inside', textinfo='percent+label') 
        else:
          df['Year_Quarter']=df['Year'].astype(str)+"-Q"+df['Quarter'].astype(str)
          fig1 = px.pie(df, values='Transaction_count', names='Year_Quarter',
                        color_discrete_sequence=px.colors.sequential.Viridis,
                        title ='TOTAL TRANSACTIONS (2018 TO 2022) DIVIDED BY QUARTER')
          fig1.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig1)
#=================================================================>USER BASE ANALYSIS<=============================================================
st.subheader('USER BASE ANALYSIS')
tab1, tab2, tab3 = st.tabs(["STATE ANALYSIS", "DISTRICT ANALYSIS","INDIA  ANALYSIS"])      

with tab1:
      st.info('State wise Registered user count is shown for each Quarter of a Year', icon="ℹ️")
      col1, col2, col3= st.columns(3)
      with col1:
        User_state = st.selectbox('Please select the State',
                                  ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                                  'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                                  'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                                  'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
                                  'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
                                  'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                                  'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
                                  'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                  'uttarakhand', 'west-bengal'),key='ub')
      with col2:
         User_year = st.selectbox('Please select the Year',
                                 ('From 2018-2022','2018', '2019', '2020','2021','2022'),
                                 key='uy1')
      col1, col2=st.columns(2)
      with col1:
         if User_year =='From 2018-2022':
           mycursor.execute(f"select year,quater,sum(registereduser) from map_user where state='{User_state}' group by year,quater")
         else:
           mycursor.execute(f"select year,quater,sum(registereduser) from map_user where state='{User_state}'and year='{User_year}' group by quater")
           
         df_u = pd.DataFrame(mycursor.fetchall(),columns=['Year','Quarter','Registereduser'])
         st.dataframe(df_u)
      with col2:
         df_u = df_u.sort_values(by=['Year'])
         df_u["Quarter"] = "Q"+df_u['Quarter'].astype(str)
         df_u['Year_Quarter']=df_u['Year'].astype(str) +"-"+ df_u["Quarter"].astype(str)
         df_u['Registereduser']=df_u['Registereduser'].astype(int)
         fig = px.bar(df_u, x='Year_Quarter', y='Registereduser',color='Registereduser',color_continuous_scale="Viridis")
         st.plotly_chart(fig,use_container_width=True)
with tab2:
      st.info('District wise Registered user count is shown for each Quarter of a Year', icon="ℹ️")
      col1, col2, col3 = st.columns(3)
      with col1:
         Dis_year = st.selectbox('Please select the Year',
                                ('2018', '2019', '2020','2021','2022'),key='yu2')
      with col2:
         Dis_state = st.selectbox('Please select the State',
                                 ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                                 'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                                 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                                 'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
                                 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
                                 'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                                 'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
                                 'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                 'uttarakhand', 'west-bengal'),key='dk1')
      with col3:
         mycursor.execute(f"select year,quater,district,registereduser  from map_user where state='{Dis_state}' and year='{Dis_year}'")
         df_u1 = pd.DataFrame(mycursor.fetchall(),columns=['Year','Quarter','District','Registereduser'])
         Dis_district=st.selectbox('Please select the District',
                                   df_u1['District'].sort_values().unique(),key='dis1')
      col1,col2=st.columns(2)
      with col1:
        
         selected_df= df_u1.loc[(df_u1['District'] == Dis_district )]
         st.dataframe(selected_df)
      with col2:
         selected_df['Quarter']='Quarter-'+selected_df['Quarter'].astype(str)
         selected_df['Registereduser']=selected_df['Registereduser'].astype(int)
         fig = px.bar(selected_df, x='Quarter', y='Registereduser',
                      color='Registereduser',color_continuous_scale="oranges")
         st.plotly_chart(fig,use_container_width=True)
with tab3:
      
      mycursor.execute("select year,SUM(registereduser) from map_user group by year" )
      df = pd.DataFrame(mycursor.fetchall(),columns=['year','registereduser'])
      col_1,col_2=st.columns(2)
      
      with col_1:
        
         st.info('Year wise total user registered count', icon="ℹ️")
         col1,col2=st.columns(2)
         with col1:
            st.write("")
            st.write("")
            st.dataframe(df)
         with col2:
            fig = px.pie(df, values='registereduser', names='year',
                         color_discrete_sequence=px.colors.sequential.Viridis,
                         title='TOTAL REGISTERED USER (2018 TO 2022)')
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)  
      with col_2:
         st.info('Phone brand wise user registered count for each year', icon="ℹ️")
         st.write("")
         col1,col2=st.columns([1,2])
         with col1:
            brand_year = st.selectbox('Please select the Year',
                                     ('2018', '2019', '2020','2021','2022'),key='bru2')
            mycursor.execute(f"select brand_type,SUM(count) from aggregated_user where year='{brand_year}' group by brand_type order by SUM(count) Desc ")
            
            df_b = pd.DataFrame(mycursor.fetchall(),columns=['Brand_type','UserCount'])
            st.dataframe(df_b) 
         with col2:
            fig = px.pie(df_b, values='UserCount', names='Brand_type',
                         color_discrete_sequence=px.colors.sequential.Viridis,
                         title='BRAND WISE REGISTERED USER (2018 TO 2022)')
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)  


#=================================================================>TOP TRANSACTION & USER ANALYSIS<=============================================================
st.subheader('TOP TRANSACTION & USER ANALYSIS')
tab1, tab2 = st.tabs(["STATE ANALYSIS", "DISTRICT ANALYSIS"])      

with tab1:
   
   
   Top_year = st.selectbox('Please select the Year',
                          ('2018', '2019', '2020','2021','2022'),key='topu2')
   col1, col2 = st.columns(2)
   with col1:
      st.info('TOP 3 STATE BY TRANSACTION',icon="ℹ️")
      mycursor.execute(f"select state,SUM(count),SUM(amount) from map_transaction where year='{Top_year}' group by state order by SUM(count) Desc LIMIT 3")
      df_ty = pd.DataFrame(mycursor.fetchall(),columns=['state','Total_Transaction_count','Total_Transaction_amount'])
      st.dataframe(df_ty) 
      fig = px.pie(df_ty, values='Total_Transaction_count',
                   names='state',color_discrete_sequence=px.colors.sequential.Rainbow,
                   title=f"TOP 3 STATE BY REGISTERED USER COUNT- '{int(Top_year)}'")
      fig.update_traces(textposition='inside', textinfo='percent+label')
      st.plotly_chart(fig,use_container_width=True) 
   with col2:
      st.info('TOP 3 STATE BY REGISTERED USER COUNT',icon="ℹ️")
      mycursor.execute(f"select state,SUM(registeredUser) from map_user  where year='{Top_year}' group by state order by SUM(registeredUser) Desc LIMIT 3")
      df_tu = pd.DataFrame(mycursor.fetchall(),columns=['state','Total_RegisteredUser'])
      st.dataframe(df_tu)
      fig = px.pie(df_tu, values='Total_RegisteredUser',
                   names='state',color_discrete_sequence=px.colors.sequential.Rainbow,
                   title=f"TOP 3 STATE BY REGISTERED USER COUNT- '{int(Top_year)}'")
      fig.update_traces(textposition='inside', textinfo='percent+label')
      st.plotly_chart(fig,use_container_width=True) 
with tab2:
   col1, col2=st.columns(2)
   with col1:
      Top_Dis_year = st.selectbox('Please select the Year',
                                 ('2018', '2019', '2020','2021','2022'),key='topdu2')
   with col2:
      Top_Dis_state = st.selectbox('Please select the State',
                                  ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                                  'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                                  'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                                  'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
                                  'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
                                  'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                                  'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
                                  'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                  'uttarakhand', 'west-bengal'),key='tdk1')
   col1, col2 = st.columns(2)
   with col1:
      st.info('TOP 3 DISTRICT BY TRANSACTION', icon="ℹ️")
      mycursor.execute(f"select District,sum(Transaction_count),Transaction_amount from top_transaction where year='{Top_Dis_year}' and state='{Top_Dis_state}' group by District order by sum(Transaction_count) Desc LIMIT 3")
      df_dt = pd.DataFrame(mycursor.fetchall(),columns=['District','Total_Transaction_count','Total_Transaction_amount'])
      st.dataframe(df_dt) 
      fig = px.pie(df_dt, values='Total_Transaction_count',
                   names='District',color_discrete_sequence=px.colors.sequential.Rainbow,
                   title=f"TOP 3 DISTRICT BY TRANSACTION - '{int(Top_Dis_year)}'")
      fig.update_traces(textposition='inside', textinfo='percent+label')
      st.plotly_chart(fig,use_container_width=True)  
   with col2:
      st.info('TOP 3 DISTRICT BY REGISTERED USER COUNT', icon="ℹ️")
      mycursor.execute(f"select District,sum(registeredUser) from top_user  where year='{Top_Dis_year}' and state='{Top_Dis_state}'group by District order by sum(registeredUser) Desc LIMIT 3")
      df_ut = pd.DataFrame(mycursor.fetchall(),columns=['District','Total_RegisteredUser'])
      st.dataframe(df_ut)
      fig = px.pie(df_ut, values='Total_RegisteredUser',
                   names='District',color_discrete_sequence=px.colors.sequential.Rainbow,
                   title=f"TOP 3 DISTRICT BY REGISTERED USER COUNT- '{int(Top_Dis_year)}'")
      fig.update_traces(textposition='inside', textinfo='percent+label')
      st.plotly_chart(fig,use_container_width=True) 


