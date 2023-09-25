# # # # # # # app.py
# # # # # from flask import Flask, render_template, request, url_for
# # # # #
# # # # # app = Flask(__name__)
# # # # #
# # # # # @app.route('/', methods=['GET', 'POST'])
# # # # # def index():
# # # # #     video_url = None
# # # # #     if request.method == 'POST' and 'video' in request.files:
# # # # #         video = request.files['video']
# # # # #         video_path = "static/" + video.filename
# # # # #         video.save(video_path)
# # # # #         video_url = url_for('static', filename=video.filename)
# # # # #     return render_template('dashboard.py', video_url=video_url)
# # # # #
# # # # # if __name__ == "__main__":
# # # # #     app.run(debug=True)
# # # # # from flask import Flask, render_template
# # # # #
# # # # # app = Flask(__name__)
# # # # #
# # # # # @app.route('/')
# # # # # def index():
# # # # #     return render_template('dashboard.py')
# # # # #
# # # # # if __name__ == "__main__":
# # # # #     app.run(debug=True)
# # # # #
# # # # # from flask import Flask, render_template
# # # # #
# # # # # app = Flask(__name__)
# # # # #
# # # # # @app.route('/')
# # # # # def index():
# # # # #     return render_template('dashboard.py')
# # # # #
# # # # #
# # # # # if __name__ == "__main__":
# # # # #     # Listen on all network interfaces (0.0.0.0) instead of just localhost (127.0.0.1)
# # # # #     app.run(host='0.0.0.0', debug=True)
# # # # import dash
# # # # from dash import dcc, html
# # # # import plotly.express as px
# # # # import pandas as pd
# # # # from flask import Flask
# # # #
# # # # # Sample data with positive and negative words
# # # # word_data = pd.DataFrame({
# # # #     'Word': ['Word1', 'Word2', 'Word3', 'Word4', 'Word5'],
# # # #     'Positive': [10, 15, 12, 8, 14],
# # # #     'Negative': [5, 7, 9, 4, 6]
# # # # })
# # # #
# # # # # Create a Flask web application
# # # # server = Flask(__name__)
# # # #
# # # # # Create a Dash web application
# # # # app = dash.Dash(__name__, server=server)
# # # #
# # # # # Define the layout of the dashboard using Dash components
# # # # app.layout = html.Div([
# # # #     # Header Section
# # # #     html.Header([
# # # #         html.Nav([
# # # #             html.Ul([
# # # #                 html.Li(html.A('Home', href='#')),
# # # #                 html.Li(html.A('About', href='#')),
# # # #                 html.Li(html.A('Contact', href='#')),
# # # #             ])
# # # #         ])
# # # #     ]),
# # # #
# # # #     # Hero Section
# # # #     html.Section([
# # # #         html.H1('Welcome to Your Dashboard'),
# # # #     ], className="hero"),
# # # #
# # # #     # Main Content Section
# # # #     html.Section([
# # # #         # Bubble Chart Section
# # # #         html.Div([
# # # #             html.H2('Bubble Chart - Positive vs. Negative Words'),
# # # #             dcc.Graph(
# # # #                 id='bubble-chart',
# # # #                 figure=px.scatter(
# # # #                     word_data, x='Positive', y='Negative',
# # # #                     size='Positive', text='Word', title='Bubble Chart'
# # # #                 )
# # # #             ),
# # # #         ], className="bubble-chart"),
# # # #     ], className="main-content"),
# # # # ])
# # # #
# # # # if __name__ == '__main__':
# # # #     app.run_server(debug=True)
# # # import dash
# # # from dash import dcc, html
# # # import plotly.express as px
# # # import pandas as pd
# # # from flask import Flask
# # #
# # # # Sample data with positive and negative words
# # # word_data = pd.DataFrame({
# # #     'Word': ['Word1', 'Word2', 'Word3', 'Word4', 'Word5'],
# # #     'Positive': [10, 15, 12, 8, 14],
# # #     'Negative': [5, 7, 9, 4, 6]
# # # })
# # #
# # # # Create a Flask web application
# # # server = Flask(__name__)
# # #
# # # # Create a Dash web application
# # # app = dash.Dash(__name__, server=server)
# # #
# # # # Define the layout of the dashboard using Dash components
# # # app.layout = html.Div([
# # #     # Left Sidebar
# # #     html.Div([
# # #         html.Ul([
# # #             html.Li(html.A('Setup Community', href='#')),
# # #             html.Li(html.A('Adjust Keyword Sensitivity', href='#')),
# # #             html.Li(html.A('Call a Lawyer Now', href='#')),
# # #             html.Li(html.A('Call a Bondsman Now', href='#')),
# # #             html.Li(html.A('Call the US Embassy Now', href='#')),
# # #         ], className='sidebar'),
# # #     ], className='left-sidebar'),
# # #
# # #     # Main Content Section
# # #     html.Div([
# # #         # Header Section
# # #         html.Header([
# # #             html.Nav([
# # #                 html.Ul([
# # #                     html.Li(html.A('Home', href='#')),
# # #                     html.Li(html.A('About', href='#')),
# # #                     html.Li(html.A('Contact', href='#')),
# # #                 ])
# # #             ])
# # #         ]),
# # #
# # #         # Hero Section
# # #         html.Section([
# # #             html.H1('Welcome to Your Dashboard'),
# # #         ], className="hero"),
# # #
# # #         # Bubble Chart Section
# # #         html.Div([
# # #             html.H2('Bubble Chart - Positive vs. Negative Words'),
# # #             dcc.Graph(
# # #                 id='bubble-chart',
# # #                 figure=px.scatter(
# # #                     word_data, x='Positive', y='Negative',
# # #                     size='Positive', text='Word', title='Bubble Chart'
# # #                 )
# # #             ),
# # #         ], className="bubble-chart"),
# # #     ], className="main-content"),
# # # ])
# # #
# # # if __name__ == '__main__':
# # #     app.run_server(debug=True)
# # import dash
# # from dash import dcc, html
# # import plotly.express as px
# # import pandas as pd
# # from flask import Flask
# #
# # # Sample data with positive and negative words
# # word_data = pd.DataFrame({
# #     'Word': ['Word1', 'Word2', 'Word3', 'Word4', 'Word5'],
# #     'Positive': [10, 15, 12, 8, 14],
# #     'Negative': [5, 7, 9, 4, 6]
# # })
# #
# # # Create a Flask web application
# # server = Flask(__name__)
# #
# # # Create a Dash web application
# # app = dash.Dash(__name__, server=server)
# #
# # # Define the layout of the dashboard using Dash components
# # app.layout = html.Div([
# #     # Horizontal Line
# #     html.Div(className='horizontal-line'),
# #
# #     # Left Sidebar
# #     html.Div([
# #         html.Ul([
# #             html.Li(html.A('Setup Community', href='#')),
# #             html.Li(html.A('Adjust Keyword Sensitivity', href='#')),
# #             html.Li(html.A('Call a Lawyer Now', href='#')),
# #             html.Li(html.A('Call a Bondsman Now', href='#')),
# #             html.Li(html.A('Call the US Embassy Now', href='#')),
# #         ], className='sidebar'),
# #     ], className='left-sidebar'),
# #
# #     # Main Content Section
# #     html.Div([
# #         # Header Section
# #         html.Header([
# #             html.Nav([
# #                 html.Ul([
# #                     html.Li(html.A('Home', href='#')),
# #                     html.Li(html.A('About', href='#')),
# #                     html.Li(html.A('Contact', href='#')),
# #                 ])
# #             ])
# #         ]),
# #
# #         # Hero Section
# #         html.Section([
# #             html.H1('Welcome to Your Dashboard'),
# #         ], className="hero"),
# #
# #         # Bubble Chart Section
# #         html.Div([
# #             html.H2('Bubble Chart - Positive vs. Negative Words'),
# #             dcc.Graph(
# #                 id='bubble-chart',
# #                 figure=px.scatter(
# #                     word_data, x='Positive', y='Negative',
# #                     size='Positive', text='Word', title='Bubble Chart'
# #                 ),
# #                 config={'displayModeBar': False}
# #             ),
# #         ], className="bubble-chart"),
# #     ], className="main-content"),
# # ])
# #
# # if __name__ == '__main__':
# #     app.run_server(debug=True)
# import dash
# from dash import dcc, html
# import plotly.express as px
# import pandas as pd
# from flask import Flask
#
# # Sample data with positive and negative words
# word_data = pd.DataFrame({
#     'Word': ['Word1', 'Word2', 'Word3', 'Word4', 'Word5'],
#     'Positive': [10, 15, 12, 8, 14],
#     'Negative': [5, 7, 9, 4, 6]
# })
#
# # Create a Flask web application
# server = Flask(__name__)
#
# # Create a Dash web application
# app = dash.Dash(__name__, server=server)
#
# # Define the layout of the dashboard using Dash components
# app.layout = html.Div([
#     # Left Sidebar
#     html.Div([
#         html.Ul([
#             html.Li(html.A('Setup Community', href='#')),
#             html.Li(html.A('Adjust Keyword Sensitivity', href='#')),
#             html.Li(html.A('Call a Lawyer Now', href='#')),
#             html.Li(html.A('Call a Bondsman Now', href='#')),
#             html.Li(html.A('Call the US Embassy Now', href='#')),
#         ], className='sidebar'),
#     ], className='left-sidebar'),
#
#     # Main Content Section
#     html.Div([
#         # Header Section
#         html.Header([
#             html.Nav([
#                 html.Ul([
#                     html.Li(html.A('Home', href='#')),
#                     html.Li(html.A('About', href='#')),
#                     html.Li(html.A('Contact', href='#')),
#                 ])
#             ])
#         ]),
#
#         # Hero Section
#         html.Section([
#             html.H1('Welcome to Your Dashboard'),
#         ], className="hero"),
#
#         # Bubble Chart Section
#         html.Div([
#             html.H2('Bubble Chart - Positive vs. Negative Words'),
#             dcc.Graph(
#                 id='bubble-chart',
#                 figure=px.scatter(
#                     word_data, x='Positive', y='Negative',
#                     size='Positive', text='Word', title='Bubble Chart'
#                 ),
#                 config={'displayModeBar': False}
#             ),
#         ], className="bubble-chart"),
#     ], className="main-content"),
# ])
#
# if __name__ == '__main__':
#     app.run_server(debug=True)
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.py')

if __name__ == '__main__':
    app.run(debug=True)
