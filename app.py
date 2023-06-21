import streamlit as st
from backend import generate_words, load_model 

st.title('AI Words Generator')
st.write('''
This **Neural Network** has been trained on a dataset of words, has learned the realations between letters and is now able to generate similar words
''')

italian_model, italian_itos = load_model('italian')

models = {
    'Italian': load_model('italian'),
    'Parolacce': load_model('parolacce'),
    'Names' : load_model('names')
}

model = st.radio('What model would you like to use?', ['Italian', 'Parolacce', 'Names'])
n = st.slider('How many words would you like to generate?', 0, 50, 10)
generate = st.button('Generate')

if generate:
    out = generate_words(models[model][0], models[model][1], n = n)
    st.write(out)

st.write('***Some of the generated words might be actual words')