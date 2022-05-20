
from flask import Flask, Response, render_template
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import StringIO
import base64

app = Flask(__name__, instance_relative_config=True)


@app.route('/')
def plot_wheatprice():
    wheat_df = pd.read_csv('flaskcontr/wheat_df.csv')
    fig, ax = plt.subplots(figsize=(20,10))
    fig = sns.lineplot(ax=ax, x=wheat_df['date'], y=wheat_df['price'])
    fig.tick_params( axis='x', rotation=90)
    fig.set(title='Wheatprice development Chicago board of trade')
    
    plt.savefig(img, format='png')
    img.seek(0)
    output=base64.b64encode(img.getvalue())
    return render_template
