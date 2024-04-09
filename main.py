import streamlit as st  # Import Streamlit library for building web applications
from streamlit_option_menu import option_menu  # Custom option menu for Streamlit
import pickle  # Import pickle for loading the pre-trained model
import warnings  # Import warnings to suppress potential warnings
import pandas as pd  # Import pandas for data manipulation
import plotly.express as px  # Import Plotly Express for interactive plots
from io import StringIO  # Import StringIO for string I/O operations
import requests  # Import requests for making HTTP requests

# Load the pre-trained maternal health risk prediction model
maternal_model = pickle.load(open("model/finalized_maternal_model.sav", 'rb'))

# Create a sidebar for navigation
with st.sidebar:
    st.title("PregCare")  # Sidebar title
    st.write("Welcome to the PregPredict")  # Welcome message
    st.write("Choose an option below:")  # Instructions for choosing an option

    # Option menu for selecting different features
    selected = option_menu('MedPredict',
                           ['About us',
                            'Pregnancy Risk Prediction'
                            ],
                           icons=['chat-square-text', 'hospital', 'capsule-pill', 'clipboard-data'],
                           default_index=0)  # Default selection is 'About us'

# If 'About us' is selected from the sidebar
if (selected == 'About us'):
    # Display information about the platform
    st.title("Welcome to PregPredict")  # Title
    st.write("With PregPredict we align our mission to deliver the best possible care forHER. "
             "Our platform is specifically designed to address the intricate aspects of maternal health, providing accurate "
             "predictions and proactive risk management.")  # Description

    # Create two columns for layout
    col1, col2 = st.columns(2)

    with col1:
        # Section 1: Pregnancy Risk Prediction
        st.header("Pregnancy Risk Prediction")  # Subtitle
        st.write("Our Pregnancy Risk Prediction feature utilizes advanced algorithms to analyze various parameters, including age, "
                 "body sugar levels, blood pressure, and more. By processing this information, we provide accurate predictions of "
                 "potential risks during pregnancy.")  # Description
        # Add an image for Pregnancy Risk Prediction
        st.image("graphics/final.jpg", caption="Pregnancy Risk Prediction", use_column_width=True)  # Image

    # Closing note
    st.write("Thank you for choosing PregPredict. We are committed to advancing healthcare through technology and predictive analytics. "
             "Feel free to explore our features and take advantage of the insights we provide.")  # Closing note
    st.write("Made with love by Kairvee.")  # Developer attribution

# If 'Pregnancy Risk Prediction' is selected from the sidebar
if (selected == 'Pregnancy Risk Prediction'):
    # Page title
    st.title('Pregnancy Risk Prediction')

    # Description of pregnancy risk prediction
    content = "Predicting the risk in pregnancy involves analyzing several parameters, including age, blood sugar levels, blood pressure, and other relevant factors. By evaluating these parameters, we can assess potential risks and make informed predictions regarding the pregnancy's health"
    st.markdown(f"<div style='white-space: pre-wrap;'><b>{content}</b></div></br>", unsafe_allow_html=True)

    # Getting input data from the user
    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.text_input('Age of the Person', key="age")  # Input field for age

    with col2:
        diastolicBP = st.text_input('DiastolicBP in mmHg')  # Input field for diastolic blood pressure

    with col3:
        BS = st.text_input('Blood glucose in mmol/L')  # Input field for blood glucose level

    with col1:
        bodyTemp = st.text_input('Body Temperature in Celsius')  # Input field for body temperature

    with col2:
        heartRate = st.text_input('Heart rate in beats per minute')  # Input field for heart rate

    riskLevel = ""  # Initialize risk level
    predicted_risk = [0]  # Initialize predicted risk

    # Create a button for predicting pregnancy risk
    with col1:
        if st.button('Predict Pregnancy Risk'):
            with warnings.catch_warnings():  # Suppress potential warnings
                warnings.simplefilter("ignore")
                # Predict the risk using the maternal health model
                predicted_risk = maternal_model.predict([[age, diastolicBP, BS, bodyTemp, heartRate]])

            # Display the predicted risk level
            st.subheader("Risk Level:")  # Subtitle
            if predicted_risk[0] == 0:
                # Display low risk message
                st.markdown('<bold><p style="font-weight: bold; font-size: 20px; color: green;">Low Risk</p></bold>', unsafe_allow_html=True)
            elif predicted_risk[0] == 1:
                # Display medium risk message
                if (int(age) == 26 and int(diastolicBP) == 110 and int(heartRate) == 90 and float(BS) == 4 and float(bodyTemp) == 29):
                    st.markdown('<bold><p style="font-weight: bold; font-size: 20px; color: orange;">Medium Risk</p></Bold>', unsafe_allow_html=True)
                else:
                    st.markdown('<bold><p style="font-weight: bold; font-size: 20px; color: orange;">Medium Risk</p></Bold>', unsafe_allow_html=True)
            else:
                # Display high risk message
                st.markdown('<bold><p style="font-weight: bold; font-size: 20px; color: red;">High Risk. Do consult a doctor as early as possible.</p><bold>', unsafe_allow_html=True)
