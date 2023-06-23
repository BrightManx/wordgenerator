import streamlit as st
from backend import generate_words, load_model 
import numpy as np

hide_menu_style = """
<style>
#MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.set_page_config(
    page_title="Word Generator",
    layout="centered"
)

models = {
    'Italian': load_model('italian'),
    'Parolacce': load_model('parolacce'),
    'Names' : load_model('names')
}

datasets = {
    'Italian': open('italian.txt').read().splitlines(),
    'Parolacce': open('parolacce.txt').read().splitlines(),
    'Names': open('names.txt').read().splitlines()
}

page = st.sidebar.selectbox('Generate new words or explore the datasets', ['Generator', 'Explore the training dataset'])

if page == 'Generator':
    st.title('AI Words Generator')
    st.write('''
    This **Neural Network** has been trained on a dataset of words, learning the probability of each letter in a word given the three before and is now able to generate similar words.
    ''')

    model = st.radio('What model would you like to use?', models.keys())
    n = st.slider('How many words would you like to generate?', 0, 50, 10)

    generate = None
    if model == 'Parolacce':
        st.write("""
        By using this AI model that generates swear words, insults, or potentially offensive content, you acknowledge and agree to the following:  
        1. This AI model is intended for entertainment purposes only. It generates random and fictional content, including swear words, insults, or offensive language.
        2. As a user, you are solely responsible for how you choose to use the generated content. You understand that any offensive or inappropriate use of the generated content is strictly prohibited. You must exercise caution and discretion when sharing or disseminating the output from this AI model.
        3. It is important to understand that the generated content may not align with your personal morals, beliefs, or values. I, the creator of this model, do not endorse or promote any offensive or harmful content generated through its use.
        4. I, the creator, shall not be held liable for any direct, indirect, incidental, special, or consequential damages arising out of or in connection with the use or misuse of the generated content.
        """)
        age = st.checkbox("""
        I confirm to be at least 18 years old
        """)
        if age == True:
            generate = st.button('Generate')

    else:
        generate = st.button('Generate')

    if generate:
        out = generate_words(models[model][0], models[model][1], n = n)
        if model == 'Names': out = [name.capitalize() for name in out]
        st.write(out)

        st.write('''
        Some of the generated words might be actual words.  
        The words in the list below marked with "True" are present in the training dataset.
        ''')

        check = [f'{word}, {word in datasets[model]}' for word in out]
        st.write(check)

if page == 'Explore the training dataset':
    st.title('Training Datasets')
    st.write('In this section you can explore the datasets used to train the models.')
    data = st.selectbox('Which dataset would you like to explore?', datasets.keys())
    n = st.slider('How many words would you like to sample from the dataset?', 0, len(datasets[data]), 10)
    st.write(f'Here\'s a sample of {n} words from the "{data.lower()}" training dataset')
    st.write(np.random.choice(datasets[data], n))
