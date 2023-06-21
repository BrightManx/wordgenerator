import streamlit as st
import torch
import torch.nn.functional as F
import json

def load_model(model = None, neurons = 256, embedding_dim = 24, context_size = 3):
    
    if model is None: raise Exception('load_model: "model" attribute is empty')

    # Itos
    with open(f'{model}_itos.json', 'r') as file:
        itos = json.load(file)
    vocab_size = len(itos)

    # Instance
    loaded_model = torch.nn.Sequential(
        torch.nn.Embedding(vocab_size, embedding_dim),
        torch.nn.Flatten(),
        torch.nn.Linear(context_size*embedding_dim, neurons),
        torch.nn.Tanh(),
        torch.nn.Linear(neurons, vocab_size))

    # Load weights
    path = f'{model}_{neurons}_{embedding_dim}_{vocab_size}_{context_size}.pth'
    loaded_model.load_state_dict(torch.load(path))

    return loaded_model, itos


def generate_words(model, itos, n = 1, neurons = 256, embedding_dim = 24, vocab_size = 38, context_size = 3):
    
    words = []
    
    for _ in range(n):
        word = []
        context = [0] * context_size
        while True:
            logits = model(torch.tensor(context).view(1, -1))
            out = F.softmax(logits, dim = 1)
            ix = torch.multinomial(out, num_samples=1).item()
            word.append(ix)
            context = context[1:] + [ix]
            if ix == 0:
                break
        words.append(''.join(itos[str(i)] for i in word[:-1]))
    
    return words
