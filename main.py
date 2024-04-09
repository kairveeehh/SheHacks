import streamlit as st
from streamlit_option_menu import option_menu
import pickle
import warnings
import pandas as pd
import plotly.express as px
from io import StringIO
import requests

maternal_model = pickle.load(open("model/finalized_maternal_model.sav", 'rb'))

# sidebar for navigation
with st.sidebar:
    st.title("PregCare")
    st.write("Welcome to the PregPredict")
    st.write("Choose an option below:")

    selected = option_menu('MedPredict',
                           ['About us',
                            'Pregnancy Risk Prediction'
                            ],
                           icons=['chat-square-text', 'hospital', 'capsule-pill', 'clipboard-data'],
                           default_index=0)

if (selected == 'About us'):

    st.title("Welcome to PregPredict")
    st.write("With PregPredict we align our mission to deliver the best possible care forHER. "
             "Our platform is specifically designed to address the intricate aspects of maternal health, providing accurate "
             "predictions and proactive risk management.")

    col1, col2 = st.columns(2)
    with col1:
        # Section 1: Pregnancy Risk Prediction
        st.header("Pregnancy Risk Prediction")
        st.write("Our Pregnancy Risk Prediction feature utilizes advanced algorithms to analyze various parameters, including age, "
                 "body sugar levels, blood pressure, and more. By processing this information, we provide accurate predictions of "
                 "potential risks during pregnancy.")
        # Add an image for Pregnancy Risk Prediction
        st.image("graphics/final.jpg", caption="Pregnancy Risk Prediction", use_column_width=True)

    # Closing note
    st.write("Thank you for choosing PregPredict. We are committed to advancing healthcare through technology and predictive analytics. "
             "Feel free to explore our features and take advantage of the insights we provide.")
    st.write("Made with love by Kairvee.")

if (selected == 'Pregnancy Risk Prediction'):

    # page title
    st.title('Pregnancy Risk Prediction')
    content = "Predicting the risk in pregnancy involves analyzing several parameters, including age, blood sugar levels, blood pressure, and other relevant factors. By evaluating these parameters, we can assess potential risks and make informed predictions regarding the pregnancy's health"
    st.markdown(f"<div style='white-space: pre-wrap;'><b>{content}</b></div></br>", unsafe_allow_html=True)

    # getting the input data from the user
    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.text_input('Age of the Person', key="age")

    with col2:
        diastolicBP = st.text_input('DiastolicBP in mmHg')

    with col3:
        BS = st.text_input('Blood glucose in mmol/L')

    with col1:
        bodyTemp = st.text_input('Body Temperature in Celsius')

    with col2:
        heartRate = st.text_input('Heart rate in beats per minute')

    riskLevel = ""
    predicted_risk = [0]
    # creating a button for Prediction
    with col1:
        if st.button('Predict Pregnancy Risk'):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                predicted_risk = maternal_model.predict([[age, diastolicBP, BS, bodyTemp, heartRate]])
            # st
            st.subheader("Risk Level:")
            if predicted_risk[0] == 0:
                st.markdown('<bold><p style="font-weight: bold; font-size: 20px; color: green;">Low Risk</p></bold>', unsafe_allow_html=True)
            elif predicted_risk[0] == 1:
                if (int(age) == 26 and int(diastolicBP) == 110 and int(heartRate) == 90 and float(BS) == 4 and float(bodyTemp) == 29):
                    st.markdown('<bold><p style="font-weight: bold; font-size: 20px; color: orange;">Medium Risk</p></Bold>', unsafe_allow_html=True)
                else:
                    st.markdown('<bold><p style="font-weight: bold; font-size: 20px; color: orange;">Medium Risk</p></Bold>', unsafe_allow_html=True)
            else:
                st.markdown('<bold><p style="font-weight: bold; font-size: 20px; color: red;">High Risk. Do consult a doctor as early as possible.</p><bold>', unsafe_allow_html=True)
