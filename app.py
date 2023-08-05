import streamlit as st
from backend import generate_words, load_model 
import numpy as np
import json

st.set_page_config(
    page_title="Word Generator",
    layout="centered",
    initial_sidebar_state="collapsed"
)

hide_menu_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

models = {
    'Italian': load_model('italian'),
#    'Parolacce': load_model('parolacce'),
    'Names' : load_model('names')
}

datasets = {
    'Italian': open('italian.txt').read().splitlines(),
#    'Parolacce': open('parolacce.txt').read().splitlines(),
    'Names': open('names.txt').read().splitlines()
}

page = st.sidebar.selectbox('Generate new words or explore the datasets', ['Generator', 'Explore the training dataset', 'Rate the words'])

######################################################################################################################################################################################
if page == 'Generator':
    st.title('AI Words Generator')
    st.write('''
    This **Neural Network** has been trained on a dataset of actual words, learning the complex patterns and relations among letters and is now able to generate **similar words**.
    ''')

    model = st.radio('What **model** would you like to use?', models.keys())
    n = st.slider('How **many** words would you like to generate?', 0, 50, 10)

    generate = None
    if model == 'Parolacce':
        st.write("""
        #### !! Disclaimer
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
        
        col1, col2 = st.columns(2)
        
        st.write('''
        Some of the generated words might be actual words, those marked with "True" are present in the training dataset.
        ''')
        
        with col1:
            st.write(out)

        with col2:
            check = [word in datasets[model] for word in out]
            st.write(check)

###########################################################################################################################
if page == 'Explore the training dataset':
    st.title('Training Datasets')
    st.write('In this section you can explore the datasets used to train the models.')
    data = st.selectbox('Which dataset would you like to explore?', datasets.keys())
    n = st.slider('How many words would you like to sample from the dataset?', 0, len(datasets[data]), 10)
    st.write(f'Here\'s a sample of {n} words from the "{data.lower()}" training dataset')
    st.write(np.random.choice(datasets[data], n))


###########################################################################################################################
if page =='Rate the words':

    st.write('''
1. **Random Jumble**: The generated word is a random mix of characters with no apparent meaning.  
2. **Confused Nonsense**: The word seems to lack coherence and doesn't resemble any recognizable language.  
3. **Semi-Sensical**: The word has some semblance of meaning or structure, but it's not entirely convincing as a genuine word.  
4. **Almost Authentic**: The word closely resembles a real word and might be mistaken for one, but it's not quite there yet.  
5. **Fluent Creation**: The word is a fluent and natural creation, indistinguishable from a genuine word in the language.  
    ''')
    
    with open('rating_batch.json', 'r') as file:
        rating_batch = json.load(file)
    
    ratings = [
    '1 - Random Jumble',
    '2 - Confused Nonsense',
    '3 - Semi-Sensical',
    '4 - Almost Authentic',
    '5 - Fluent Creation'
    ]
    ratings = {int(rating[0]):rating for rating in ratings}

    if "user" not in st.session_state:
        with st.form("login"):
            user = st.text_input("USERNAME:")
            submit = st.form_submit_button("Login")
            if submit:
                st.write(f'Successfully logged in as **{user}**')
                st.session_state["user"] = user
        
    if "user" in st.session_state:
        user = st.session_state["user"]
        st.write(f"<h2 style='text-align:center'> {user} is now rating </h2>", unsafe_allow_html=True)

    if "current" not in st.session_state:
        st.session_state["current"] = np.random.choice(list(rating_batch.keys()), 1).item()
    
    def change_current():
        st.session_state["current"] = np.random.choice(list(rating_batch.keys()), 1).item()
        return

    st.button("Rate another word", on_click=change_current)
    with st.form('Ratings', clear_on_submit=False):
        current = st.session_state["current"]
        st.write(f"<h1 style='text-align:center'> {current} </h1>", unsafe_allow_html=True)
        rating = st.slider('Rate', min_value=1, max_value=5)
        submit = st.form_submit_button('Submit!')
    if submit:
        with open('ratings.csv', 'a') as file:
            try:
                user = st.session_state["user"]
            except:
                user = ''
            file.write(f'{current},{rating},{user}\n')
        st.write(f"You\'ve successfully rated the word \"**{current}**\" as \"**{ratings[rating]}**\" [logged in as \"**{user}**\"]")
