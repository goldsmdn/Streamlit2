import streamlit as st
import numpy as np
import pandas as pd
from scipy.special import gamma

data_dict = {
    'Normal': {
        'setting': {'low':-10,
                    'high':10,
                    'steps':1000,
                    },
        'vars': {
                'sigma': {'low':0.1,
                        'high':10.0,
                        'default':1.0,
                        'text':'Standard Deviation',
                        },
                'mu':    {'low':-10.0,
                        'high':10.0,
                        'default':0.0,
                        'text':'Mean',
                        },
                }
            },    
    'Poisson': {
        'setting': {'low':0,
                    'high':20,
                    'steps':21,
                    },
        'vars': {
                'lambda': {'low':1,
                        'high':10,
                        'default':5,
                        'text':'Lambda',
                        },
                }
            },
    'Bernoulli': {
        'setting': {'low':0,
                    'high':1,
                    'steps':2,
                    },
        'vars': {
                'p': {'low':0.0,
                        'high':1.0,
                        'default':0.5,
                        'text':'Probability',
                        },
                'k': {'low':0,
                        'high':20,
                        'default':1,
                        'text':'Possible outcomes',
                        },
                }
            }        
        }     


st.write("# Probability Distributions Module")
st.write('This module allows the user to quickly generate and visualize various \
        probability distributions using Streamlit.')


model = st.selectbox("Please choose a model to work with:",
                    ('Normal', 'Poisson', 'Bernoulli', )
                    )

def get_settings(model:str)->tuple[float, float, float]:
    """read settings from dictionary"""
    low = data_dict[model]['setting']['low']
    high = data_dict[model]['setting']['high']
    steps = data_dict[model]['setting']['steps']
    return low, high, steps

def get_slider_vars(model:str, var:str)->tuple[float, float, float, str]:
    """find the variables for the slider from the dictionary"""
    print("model =", model)
    print("data_dict[model] =", data_dict.get(model, "NOT FOUND"))
    low = data_dict[model]['vars'][var]['low']
    high = data_dict[model]['vars'][var]['high']
    default = data_dict[model]['vars'][var]['default']
    text = data_dict[model]['vars'][var]['text']
    print(f'slider vars: {low=}, {high=}, {default=}, {text=}')
    return low, high, default, text

def set_up_slider(model:str, var:str)->float:
    """set up the slider using model specific values"""
    low, high, default, text = get_slider_vars(model, var,)
    value = st.slider(text, low, high, default)
    return value

if model == 'Normal':      
    sigma = set_up_slider(model, 'sigma')
    mu = set_up_slider(model, 'mu')
    low, high, steps = get_settings(model)
    x = np.linspace(low, high, steps)
    y = 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (x - mu)**2 / (2 * sigma**2))
    df = pd.DataFrame({'x': x, 'y': y}).set_index('x')
    st.line_chart(df, x_label='x', y_label='Probability Density')
elif model =='Poisson':
    my_lambda = set_up_slider(model, 'lambda')
    low, high, steps = get_settings(model)
    x = np.linspace(low, high, steps)
    y = my_lambda ** x * np.exp(-1*my_lambda) / gamma(x + 1)
    df = pd.DataFrame({'x': x, 'y': y}).set_index('x')
    st.scatter_chart(df, x_label='x', y_label='Probability Density')
elif model =='Bernoulli':
    p = set_up_slider(model, 'p')
    low, high, steps = get_settings(model)
    x = np.linspace(low, high, steps)
    y = p * x  + (1 - p) * (1 - x)
    df = pd.DataFrame({'x': x, 'y': y}).set_index('x')
    st.bar_chart(df, x_label='x', y_label='Probability Density')

else:
    raise Exception(f'{model=} is not coded for')