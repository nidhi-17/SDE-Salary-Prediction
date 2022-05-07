import imp
import streamlit as st
import numpy as np
import pickle as pkl
import pandas as pd
import matplotlib.pyplot as plt
from Explore import load_data


df = load_data()
##**********Prediction****************##
def load():
    with open('save_model.pkl', 'rb') as file:
        data = pkl.load(file)
    return data

data=load()

regressor_loaded = data["model"]
le_emp = data["le_emp"]
le_country = data["le_country"]
le_education = data["le_education"]

def show_predict():
    st.title("Software Developer Salary Prediction")

    st.write("""### We need some information to predict the salary""")

    emps=(
        'Employed full-time', 'prefer not to say',
       'self-employed',
       'Employed part-time', 'Retired'
    )

    countries=(
        "United States",
        "India",
        "United Kingdom",
        "Germany",
        "Canada",
        "Brazil",
        "France",
        "Spain",
        "Australia",
        "Netherlands",
        "Poland",
        "Italy",
        "Russian Federation",
        "Sweden",
    )

    edlevel=(
        "Less than a Bachelors",
        "Bachelor’s degree",
        "Master’s degree",
        "Post grad",
    )

    emp=st.selectbox("Employment",emps)
    education=st.selectbox("Education Level",edlevel)
    country=st.selectbox("Country",countries)    
    experience=st.slider("Years of Experience",0,50,3)

    ok=st.button("Calculate Salary")

    if ok:
        X=np.array([[emp,education,country,experience]])

        X[:,0]=le_emp.transform(X[:,0])
        X[:,1]=le_education.transform(X[:,1])
        X[:,2]=le_country.transform(X[:,2])
        
        X=X.astype(float)
        sal_pred=regressor_loaded.predict(X)

        st.subheader(f"The estimated salary is ${sal_pred[0]:.2f}")

        #cmp=df[df['Salary']>=sal_pred[0]]
        #cmp=cmp[cmp['EdLevel']==education]
        filtered_df = df[((df['Salary']>=sal_pred[0]) & (df['EdLevel']==education)) & ((df['YearsCodePro']==experience) & (df['Employment']==emp))]
        #cmp['Country']=le_country.transform(cmp['Country'])
        st.subheader("Countries offering higher pay(Salary)")
        filtered_df=filtered_df.sort_values(by="Salary")
        cnt=np.unique(np.array(filtered_df['Country'].head(5)))

        for j in cnt:
            if(j!=country):
                st.subheader(j)
    
    
        