# import streamlit as st
# from backend import generate_words, load_model 

# st.title('AI Words Generator')
# st.write('''
# This **Neural Network** has been trained on a dataset of words, has learned the realations between letters and is now able to generate similar words
# ''')

# italian_model, italian_itos = load_model('italian')

# models = {
#     'Italian': load_model('italian'),
#     'Parolacce': load_model('parolacce'),
#     'Names' : load_model('names')
# }

# model = st.radio('What model would you like to use?', ['Italian', 'Parolacce', 'Names'])
# n = st.slider('How many words would you like to generate?', 0, 50, 10)
# generate = st.button('Generate')

# if generate:
#     out = generate_words(models[model][0], models[model][1], n = n)
#     st.write(out)

# st.write('***Some of the generated words might be actual words')

import streamlit as st
from backend import generate_words, load_model 
import numpy as np

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
    This **Neural Network** has been trained on a dataset of words, has learned the realations between letters and is now able to generate similar words
    ''')

    model = st.radio('What model would you like to use?', models.keys())
    n = st.slider('How many words would you like to generate?', 0, 50, 10)
    generate = st.button('Generate')

    if generate:
        out = generate_words(models[model][0], models[model][1], n = n)
        if model == 'Names': out = [name.capitalize() for name in out]
        st.write(out)

        st.write('''
        Some of the generated words might be actual words.  
        The words in the list below marked with "True" are present in the training dataset of actual italian words.
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
