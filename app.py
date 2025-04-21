import dash
from dash import dcc, html, callback_context, Input, Output, State, no_update
import dash_bootstrap_components as dbc
#import dash_daq as daq 
from dash.dependencies import Input, Output, State
#import json
import pandas as pd 
#import geopandas as gpd
import plotly.express as px
#import plotly.graph_objects as go
#import dash_leaflet as dl
#import dash_leaflet.express as dlx
#from dash_extensions.javascript import arrow_function, assign, Namespace
import joblib
#import time
#import base64
from pdf_generator import create_report
from dash import ctx

####################################################################################
####################################################################################
unique_mahalla_olx = pd.read_csv('data/unique_mahalla_olx.csv')
uybor_cols=pd.read_csv('data/uybor_columns.csv')
mahalla_and_tuman=pd.read_csv('data\mahalla_tuman_codes.csv')
# df = pd.read_csv(r'data\olx_data.csv')
model1 = joblib.load('data/GBM_MODEL_WITHOUT_DISTANCE.pkl')
model2 = joblib.load('data/model2.pkl')
X = pd.read_csv(r'data/xcolumns.csv')
model = model1
from datetime import datetime

print(datetime)  # Should output: <class 'datetime.datetime'>

current_month = datetime.now().month
current_year = datetime.now().year

print(f"Current Month: {current_month}, Current Year: {current_year}")

# df['month_and_year'] = pd.to_datetime(df['month_and_year'], format='%b-%y').dt.strftime('%m-%Y')
# df['month_and_year'] = pd.to_datetime(df['month_and_year'], format='%m-%Y')
# df_sorted = df.sort_values(by='month_and_year')
# df_sorted['price_per_sq'] = df_sorted['price1']/df_sorted['sqrm1']

my_dict = {}

for key in X.columns:
    if key != 'Unnamed: 0':
        my_dict[key]=0
#########################
# my_dict_xls = pd.DataFrame().from_dict(my_dict)
# my_dict_xls.to_excel('my_dict_xls.xlsx')

importances = model1.feature_importance()
# print(len(importances))
feature_importances = pd.DataFrame({'Feature': my_dict.keys(), 'Importance': importances})
top_20_features = feature_importances.sort_values(by='Importance', ascending=False).head(50)

barh = px.bar(top_20_features, x='Importance', y = 'Feature', orientation='h')
barh.update_layout(
        xaxis_title="Muhimlik darajasi",
        xaxis_gridcolor='lightblue',
        yaxis_gridcolor='lightblue',
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
barh.update_xaxes(showgrid=True, gridcolor='lightblue', gridwidth=1, griddash='dash')
barh.update_yaxes(showgrid=True, gridcolor='lightblue', gridwidth=1, griddash='dash')

#########################

# avg_price = df_sorted.groupby(['month_and_year', 'Type of housing'])['price1'].mean().reset_index()
# countOfposting = df_sorted.groupby(['month_and_year', 'Type of housing']).size().reset_index(name='count')
# aggregated_df = df_sorted.groupby(['Количество комнат:', 'Type of housing']).size().reset_index(name='count')


####################################################################################
####################################################################################


app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP], 
    external_scripts=['./assets/dashExtensions_default.js'],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ]
)
# server = app.server
app.config.suppress_callback_exceptions = True

####################################################################################
####################################################################################

info_tab = html.Div([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.P(
                    "This platform is an online solution designed for the automatic valuation of homes. Its goal is to make the valuation process more efficient, transparent, and significantly more affordable. It enables fast and accurate asset valuation, eliminating many of the challenges associated with traditional appraisal methods.",
                    style={
                        'fontSize': '16px',
                        'marginBottom': '30px',
                        'lineHeight': '1.6'
                    }
                ),
                html.H3(
                    "Current challenges in the valuation process",
                    style={
                        'color': '#003049',
                        'fontSize': '24px',
                        'marginBottom': '20px',
                        'marginTop': '40px'
                    }
                ),
                html.P(
                    "Today, you may encounter the following challenges in the valuation process:",
                    style={
                        'fontSize': '16px',
                        'marginBottom': '15px'
                    }
                ),
                html.Ul([
                    html.Li("Time-consuming: The valuation can take several hours or even days.", 
                            style={'marginBottom': '10px'}),
                    html.Li("Subjectivity: The appraiser may give a subjective valuation based on assumptions or the client’s interests.", 
                            style={'marginBottom': '10px'}),
                    html.Li("Price uncertainty: Traditional valuation may lack precision due to the absence of consistent standards.", 
                            style={'marginBottom': '10px'})
                ], style={'marginBottom': '30px', 'paddingLeft': '20px'}),
                html.P(
                    "This platform offers an automated system to overcome these challenges, resulting in a faster valuation process and significantly reduced costs.",
                    style={
                        'fontSize': '16px',
                        'marginBottom': '40px'
                    }
                ),
                html.H3(
                    "Areas of Application",
                    style={
                        'color': '#003049',
                        'fontSize': '24px',
                        'marginBottom': '20px'
                    }
                ),
                html.Ul([
                    html.Li("Real estate market: Quick valuation for users and clients involved in property buying and selling.",
                            style={'marginBottom': '10px'}),
                    html.Li("For investors: Valuation of portfolio investments.",
                            style={'marginBottom': '10px'}),
                    html.Li("Public sector: Used in calculating property taxes and ensuring transparency.",
                            style={'marginBottom': '10px'}),                
                    html.Li("and many more",
                            style={'marginBottom': '10px'})
                    
                ], style={'marginBottom': '40px', 'paddingLeft': '20px'}),

            ], className='custom-opensauce', style={
                'maxWidth': '1200px',
                'margin': '0 auto',
                'padding': '40px',
                'backgroundColor': 'white',
                'borderRadius': '10px',
                'marginTop': '20px',
                'marginBottom': '40px'
            })
        ], xs=12, sm=12, md=12, lg=12)
    ])
], style={
    'backgroundColor': 'white',
    'minHeight': '100vh',
    'padding': '20px'
})


#####################################################################################

#---- dropdown for tumanlar----#
unique_dis = mahalla_and_tuman['district_str'].unique().tolist()
dropdown_tuman = [{'label': district, 'value': district} for district in unique_dis]

#---- prediction tab----#
prediction = dbc.Row([
    dbc.Col([
        html.Div(
            id='input-panel',
            className='custom-opensauce',
            style={
                'position': 'relative',
                'left': '0',
                'top': '50%',
                'transform': 'translateY(-50%)',
                'padding': '20px',
                'width': '100%',
                #'margin-top': '20px',
                'margin-bottom': '20px',
                'color': 'black',
                'font-weight': 'bold',
                'border': 'none'
            },            
            children=[


########################################################################################
                html.Label('Select district and neighborhood', style={'display': 'block', 'font-weight': 'bold', 'margin-bottom': '5px'}),
                html.Div(
                    style={
                        'background-color': '#ffffff',
                        #'padding': '10px',
                        'border-radius': '30px',
                        #'box-shadow': '2px 2px 5px rgba(0,0,0,0.1)',
                        'display': 'flex',  # Makes items align in a row
                        #'gap': '10px'  # Adds space between the dropdowns
                    },
                    children=[
                        html.Div([
                            dcc.Dropdown(
                                id='district-dropdown',
                                options=dropdown_tuman,
                                placeholder='Select district',
                                style={
                                'width': '100%',  
                                'border-radius': '30px 0px 0px 30px',  # Makes edges rounded
                                #'border': '1px solid #ccc',
                                #'padding': '8px'  # Optional: Adds spacing for better appearance
                                }
                            )
                        ], style={'flex': 1}),  # Makes both dropdowns take equal width
                        
                        html.Div([
                            dcc.Dropdown(
                                id='mahalla-dropdown',
                                placeholder='Select neighborhood',
                                style={
                                'width': '100%',  
                                'border-radius': '0px 30px 30px 0px',  # Makes edges rounded
                                #'border': '1px solid #ccc',
                                'border-left': '0px', #'border': '1px solid #ccc',  # Optional: Adjust border color
                                #'padding': '8px'  # Optional: Adds spacing for better appearance
                                }
                            )
                        ], style={'flex': 1})  # Equal width for mahalla dropdown
                    ]
                ),
################################################################################


                html.Label(
            'Total area and Number of rooms', style={'display': 'block', 'font-weight': 'bold', 'margin-top': '10px', 'margin-bottom': '5px'}
        ),
                html.Div(
                    style={
                        'background-color': '#ffffff',
                        #'padding': '15px',
                        'border-radius': '20px',
                        #'box-shadow': '2px 2px 5px rgba(0,0,0,0.1)',
                        'display': 'flex',  # Places inputs next to each other
                        #'gap': '10px',  # Adds space between them
                    },
                    children=[
                        html.Div(
                            style={'width': '50%'},  # Each input takes 50% of the width
                            children=[
                                #html.Label('Umumiy maydoni (m2) va Xonalar soni',
                                 #           style={'font-weight': 'bold','font-size': '13px'}),
                                dcc.Input(
                                    id='area-input', 
                                    type='number', 
                                    placeholder='Total area (m2)', 
                                      style={
                            'width': '100%',  
                            'border-radius': '30px 0px 0px 30px',  # Makes edges rounded
                            'border': '1px solid #ccc',
                            #'border': '1px solid #ccc',  # Optional: Adjust border color
                            'padding': '6px'  # Optional: Adds spacing for better appearance
                        }
                                ),
                            ]
                        ),
                        html.Div(
                            style={'width': '50%'},  
                            children=[
                                # html.Label('Xonalar soni', style={'font-weight': 'bold'}),
                                dcc.Input(
                                    id='rooms-input', 
                                    type='number', 
                                    placeholder='Number of rooms', 
                                    style={
                                'width': '100%',  
                                'border-radius': '0px 30px 30px 0px',
                                'border': '1px solid #ccc',
                                'border-left': '0px',  # Makes edges rounded
                                'padding': '6px'  # Optional: Adds spacing for better appearance
                                }
                                ),
                            ]
                        ),
                    ]
                ),

############################################################################################################
                html.Label(
        'Floor number and Total number of floors', style={'display': 'block', 'font-weight': 'bold', 'margin-top': '10px', 'margin-bottom': '5px'}
    ),

                html.Div(
                    style={
                        'background-color': '#ffffff',
                        #'padding': '15px',
                        'border-radius': '20px',
                        #'box-shadow': '2px 2px 5px rgba(0,0,0,0.1)',
                        'display': 'flex',  # Places inputs next to each other
                        #'gap': '10px',  # Adds space between them
                    },
                    children=[
                        dcc.Input(
                            id='floor-input', 
                            type='number', 
                            placeholder='Floor number', 
                            className='no-bold-placeholder',
                             style={
                            'width': '50%',  
                            'border-radius': '30px 0px 0px 30px',  # Makes edges rounded
                            'border': '1px solid #ccc', #'border': '1px solid #ccc',  # Optional: Adjust border color
                            'padding': '6px'  # Optional: Adds spacing for better appearance
                        }
                        ),
                        dcc.Input(
                            id='total-floors-input', 
                            type='number', 
                            placeholder='Total number of floors in the block', 
                                style={
                            'width': '50%',  
                            'border-radius': '0px 30px 30px 0px',
                            'border': '1px solid #ccc',
                            'border-left': '0px',   # Makes edges rounded
                            'padding': '6px'  # Optional: Adds spacing for better appearance
                        }
                        ),
                    ]
                ),

###############################################################################################################
            
                #----yaqin atrofda
                html.Label('Nearby amenities', style={'display': 'block', 'font-weight': 'bold', 'margin-top': '10px', 'margin-bottom': '5px'}),
                dcc.Dropdown(
                    id='atrofda-dropdown',
                    options = [
                        {'label': 'School', 'value': 'Maktab'},
                        {'label': 'Supermarket', 'value': 'Supermarket'},
                        {'label': 'Shop', 'value': "Do'kon"},
                        {'label': 'Parking', 'value': 'Avtoturargoh'},
                        {'label': 'Hospital', 'value': 'Shifoxona'},
                        {'label': 'Polyclinic', 'value': 'Poliklinika'},
                        {'label': 'Bus stop', 'value': 'Bekat'},
                        {'label': 'Playground', 'value': 'Bolalar maydonchasi'},
                        {'label': 'Restaurant', 'value': 'Restoran'},
                        {'label': 'Cafe', 'value': 'Kafe'},
                        {'label': 'Entertainment venues', 'value': "Ko'gilochar maskanlar"},
                        {'label': 'Kindergarten', 'value': "Bog'cha"},
                        {'label': 'Green area', 'value': 'Yashil hudud'},
                        {'label': 'Park', 'value': 'Park'}
                    ],
                    multi=True,
                    placeholder='Nearby amenities',
                    style={
                        'background-color': '#ffffff',
                        #'box-shadow': '2px 2px 5px rgba(0,0,0,0.1)',
                        #'padding': '10px',
                        'width': '100%',  # Make it full width
                        #'backgroundColor': '#f8f9fa',  # Light gray background
                        'border-radius': '30px',  # Rounded edges
                        #'border': '1px solid #ccc',  # Subtle border
                        #'fontSize': '16px'  # Bigger text
                        #'color': '#333'  # Darker text color
                    },
                ),

################################################################################################################

                #---- mebellimi yo'qmi
                html.Label('Furnished?', style={'display': 'block', 'font-weight': 'bold', 'margin-top': '10px', 'margin-bottom': '5px'}),
                dbc.RadioItems(
                    id='mebel-dropdown',
                    options=[
                        {'label': 'Yes', 'value': 'Ha'},
                        {'label': "No", 'value': "Yo'q"},
                    ],
                    value='Ha',  # Default selected
                    className="btn-group",
                    inputClassName="btn-check",
                    labelClassName="btn btn-outline-primary",
                    labelCheckedClassName="active"           
                ),
################################################################################################################              

                #----uydagi jihozlar
                html.Label('Available in the house:', style={'display': 'block', 'font-weight': 'bold', 'margin-bottom': '5px', 'margin-top': '10px'}),
                dcc.Dropdown(
                    id='uyda-dropdown',
                    options = [
                        {'label': 'Refrigerator', 'value': 'Sovutgich'},
                        {'label': 'Telephone', 'value': 'Telefon'},
                        {'label': 'Kitchen', 'value': 'Oshxona'},
                        {'label': 'Cable TV', 'value': 'Kabel TV'},
                        {'label': 'Internet', 'value': 'Internet'},
                        {'label': 'Balcony', 'value': 'Balkon'},
                        {'label': 'Washing machine', 'value': 'Kir yuvish mashinasi'},
                        {'label': 'Air conditioner', 'value': 'Konditsioner'},
                        {'label': 'Television', 'value': 'Televizor'}
                    ],
                    multi=True,
                    placeholder='Available in the house',
                    style={
                        'background-color': '#ffffff',
                        #'box-shadow': '2px 2px 5px rgba(0,0,0,0.1)',
                        #'padding': '10px',
                        'width': '100%',  # Make it full width
                        #'backgroundColor': '#f8f9fa',  # Light gray background
                        'border-radius': '30px',  # Rounded edges
                        #'border': '1px solid #ccc',  # Subtle border
                        #'fontSize': '16px'  # Bigger text
                        #'color': '#333'  # Darker text color
                    },
                ),
                #----qurilish turi
                html.Label("Construction type", style={'display': 'block', 'font-weight': 'bold', 'margin-bottom': '5px', 'margin-top': '10px'}),
                dcc.Dropdown(
                    id='qurilish-turi-dropdown',
                    options = [
                        {'label': 'Block', 'value': 'Blokli'},
                        {'label': 'Brick', 'value': 'G_ishtli'},
                        {'label': 'Monolithic', 'value': 'Monolitli'},
                        {'label': 'Panel', 'value': 'Panelli'},
                        {'label': 'Wooden', 'value': 'Yog_ochli'}
                    ],
                    placeholder='Construction type ',
                    style={
                        'background-color': '#ffffff',
                        #'box-shadow': '2px 2px 5px rgba(0,0,0,0.1)',
                        #'padding': '10px',
                        'width': '100%',  # Make it full width
                        #'backgroundColor': '#f8f9fa',  # Light gray background
                        'border-radius': '30px',  # Rounded edges
                        #'border': '1px solid #ccc',  # Subtle border
                        #'fontSize': '16px'  # Bigger text
                        #'color': '#333'  # Darker text color
                    },
                ),
                #---- planirovka turi
                html.Label('Apartment layout', style={'display': 'block', 'font-weight': 'bold', 'margin-bottom': '5px', 'margin-top': '10px'}),
                dcc.Dropdown(
                    id='planirovka-dropdown',
                    options = [
                        {'label': 'Separate layout', 'value': 'Alohida_ajratilgan'},
                        {'label': 'Mixed', 'value': 'Aralash'},
                        {'label': 'Mixed with separate areas', 'value': 'Aralash_alohida'},
                        {'label': 'For small families', 'value': 'Kichik_oilalar_uchun'},
                        {'label': 'Multi-level', 'value': 'Ko_p_darajali'},
                        {'label': 'Penthouse', 'value': 'Pentxaus'},
                        {'label': 'Studio', 'value': 'Studiya'}
                    ],
                    placeholder='Apartment layout',
                    style={
                        'background-color': '#ffffff',
                        #'box-shadow': '2px 2px 5px rgba(0,0,0,0.1)',
                        #'padding': '10px',
                        'width': '100%',  # Make it full width
                        #'backgroundColor': '#f8f9fa',  # Light gray background
                        'border-radius': '30px',  # Rounded edges
                        #'border': '1px solid #ccc',  # Subtle border
                        #'fontSize': '16px'  # Bigger text
                        #'color': '#333'  # Darker text color
                    },
                ),
                #---- sanuzel turi
                html.Label('Bathroom layout', style={'display': 'block', 'font-weight': 'bold', 'margin-bottom': '5px', 'margin-top': '10px'}),
                dcc.Dropdown(
                    id='sanuzel-dropdown',
                    options = [
                        {'label': '2 or more bathrooms', 'value': '2_va_undan_ko_p_sanuzel'},
                        {'label': 'Separate', 'value': 'Alohida'},
                        {'label': 'Combined', 'value': 'Aralash'}
                    ],
                    placeholder='Bathroom layout',
                    style={
                        'background-color': '#ffffff',
                        #'box-shadow': '2px 2px 5px rgba(0,0,0,0.1)',
                        #'padding': '10px',
                        'width': '100%',  # Make it full width
                        #'backgroundColor': '#f8f9fa',  # Light gray background
                        'border-radius': '30px',  # Rounded edges
                        #'border': '1px solid #ccc',  # Subtle border
                        #'fontSize': '16px'  # Bigger text
                        #'color': '#333'  # Darker text color
                    },
                ),
################################################################################
                html.Div(
                    #style={'display': 'flex', 'flex-direction': 'column', 'gap': '20px'},
                    children=[
                        html.Div(
                            style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start'},
                            children=[
                                html.Label('Ownership type', style={'display': 'block', 'font-weight': 'bold', 'margin-top': '10px', 'margin-bottom': '5px'}),
                                html.Div(
                                    style={'display': 'flex', 'gap': '10px'},  # Make buttons horizontal
                                    children=[
                                        dbc.RadioItems(
                                            id='owner-dropdown',
                                            options = [
                                                {'label': 'Business', 'value': 'Biznes'},
                                                {'label': 'Private', 'value': 'Xususiy'}
                                            ],
                                            value='Xususiy',
                                            className="btn-group",
                                            inputClassName="btn-check",
                                            labelClassName="btn btn-outline-primary",
                                            labelCheckedClassName="active",
                                        ),
                                    ]
                                ),
                            ]
                        ),

                        html.Div(
                            style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start'},
                            children=[
                                html.Label("Condition", style={'display': 'block', 'font-weight': 'bold', 'margin-top': '10px', 'margin-bottom': '5px'}),
                                html.Div(
                                    style={'display': 'flex', 'gap': '10px'},  # Make buttons horizontal
                                    children=[
                                        dbc.RadioItems(
                                            id='renovation-dropdown',
                                            options = [
                                                {'label': 'Excellent', 'value': 'Zo_r'},
                                                {'label': 'Good', 'value': 'Yaxshi'},
                                                {'label': 'Poor', 'value': 'Qoniqarsiz'}
                                            ],
                                            value='Yaxshi',
                                            className="btn-group",
                                            inputClassName="btn-check",
                                            labelClassName="btn btn-outline-primary",
                                            labelCheckedClassName="active",
                                        ),
                                    ]
                                ),
                            ]
                        )
                    ]
                ),


                #----bino turi
                html.Div(
                    #style={'display': 'flex', 'flex-direction': 'column', 'gap': '10px'},
                    children=[
                        # Bozor turi
                        html.Label('Market type', style={'display': 'block', 'font-weight': 'bold', 'margin-top': '10px', 'margin-bottom': '5px'}),
                        dbc.RadioItems(
                            id='bino-turi-dropdown',
                            options = [
                                {'label': 'Secondary', 'value': 'Ikkilamchi_bozor'},
                                {'label': 'Newly built', 'value': 'Yangi_qurilgan_uylar'}
                            ],
                            value='Ikkilamchi_bozor',  # Set a default value
                            className="btn-group",
                            inputClassName="btn-check",
                            labelClassName="btn btn-outline-primary",
                            labelCheckedClassName="active"
                        ),

                        # Kelishsa bo'ladimi
                        # html.Label("Price negotiable?", style={'display': 'block', 'font-weight': 'bold', 'margin-top': '10px', 'margin-bottom': '5px'}),
                        # dbc.RadioItems(
                        #     id='kelishsa-dropdown',
                        #     options=[
                        #         {'label': 'Yes', 'value': 'Yes'},
                        #         {'label': "No", 'value': 'No'}
                        #     ],
                        #     value='Yes',  # Set a default value
                        #     className="btn-group",
                        #     inputClassName="btn-check",
                        #     labelClassName="btn btn-outline-primary",
                        #     labelCheckedClassName="active"
                        # )
                    ]
                ),


                
                # #----komissiya bormi yo'qmi
                # html.Label('Komissiya bormi'),
                # dcc.Dropdown(
                #     id='komissiya-dropdown',
                #     options=[
                #         {'label': 'Ha', 'value': 'Yes'},
                #         {'label': "Yo'q", 'value': 'No'}
                #     ],
                #     placeholder="Komissiya bormi",
                #     style={'margin-bottom': '10px'}
                # ),
                #----oy
                html.Label(
            'Current month and year', 
            style={'font-weight': 'bold', 'font-size': '18px', 'margin-top': '10px', 'margin-bottom': '5px'}
        ),
                html.Div([
                    #html.Label('Qurilgan oy'),
                    dcc.Input(
                        id='oy-input', 
                        type='number', 
                        placeholder='Month', 
                        value=current_month,  
                        style={ 'width': '50%',  
                            'border-radius': '30px 0px 0px 30px',  # Makes edges rounded
                            'border': '1px solid #ccc',  # Optional: Adjust border color
                            'padding': '8px'}
                    ),
                    #html.Label('Yil'),
                    dcc.Input(
                        id='year-input', 
                        type='number', 
                        placeholder='Year', 
                        value=current_year,  
                        style={'width': '50%',  
                            'border-radius': '0px 30px 30px 0px',  # Makes edges rounded
                            'border': '1px solid #ccc',  # Optional: Adjust border color
                            'border-left': '0px',
                            'padding': '8px' })
                ], style={'display': 'flex', 'align-items': 'center'}),
            ]
        )
    ], xs=12, sm=12, md=6, lg=6, style={'padding': '10px'}),  
    
    
    dbc.Col([
        dbc.Row([
            # Details Card
            dbc.Card(
                [
                   dbc.CardBody(
                    [
                            html.Div([
                                html.Div([
                                    html.Span("District and neighborhood: ", id='selected-hudud-label', style={'font-weight': 'bold'}),
                                    html.Span(id='selected-hudud', style={'margin-left': 'auto'})
                                ], style={'display': 'flex', 'justify-content': 'space-between', 'width': '100%'}),
                                
                                html.Div([
                                    html.Span("Total area: ", id='selected-area-label', style={'font-weight': 'bold'}),
                                    html.Span(id='selected-area', style={'margin-left': 'auto'})
                                ], style={'display': 'flex', 'justify-content': 'space-between', 'width': '100%'}),

                                html.Div([
                                    html.Span("Number of rooms: ", id='selected-rooms-label', style={'font-weight': 'bold'}),
                                    html.Span(id='selected-rooms', style={'margin-left': 'auto'})
                                ], style={'display': 'flex', 'justify-content': 'space-between', 'width': '100%'}),

                                html.Div([
                                    html.Span("Floor: ", id='selected-floor-label', style={'font-weight': 'bold'}),
                                    html.Span(id='selected-floor', style={'margin-left': 'auto'})
                                ], style={'display': 'flex', 'justify-content': 'space-between', 'width': '100%'}),

                                html.Div([
                                    html.Span("Total number of floors: ", id='selected-total-floors-label', style={'font-weight': 'bold'}),
                                    html.Span(id='selected-total-floors', style={'margin-left': 'auto'})
                                ], style={'display': 'flex', 'justify-content': 'space-between', 'width': '100%'}),

                                html.Div([
                                    html.Span("Furnished: ", style={'font-weight': 'bold'}),
                                    html.Span(id='selected-mebel', style={'margin-left': 'auto'})
                                ], style={'display': 'flex', 'justify-content': 'space-between', 'width': '100%'}),

                                html.Div([
                                    html.Span("Nearby amenities: ", style={'font-weight': 'bold'}),
                                    html.Span(id='selected-atrofda', style={'margin-left': 'auto'})
                                ], style={'display': 'flex', 'justify-content': 'space-between', 'width': '100%'}),

                                html.Div([
                                    html.Span("Available in the house: ", style={'font-weight': 'bold'}),
                                    html.Span(id='selected-uyda', style={'margin-left': 'auto'})
                                ], style={'display': 'flex', 'justify-content': 'space-between', 'width': '100%'}),

                                html.Div([
                                    html.Span("Ownership type: ", style={'font-weight': 'bold'}),
                                    html.Span(id='selected-owner', style={'margin-left': 'auto'})
                                ], style={'display': 'flex', 'justify-content': 'space-between', 'width': '100%'}),

                                html.Div([
                                    html.Span("Apartment layout: ", id='selected-planirovka-label', style={'font-weight': 'bold'}),
                                    html.Span(id='selected-planirovka', style={'margin-left': 'auto'})
                                ], style={'display': 'flex', 'justify-content': 'space-between', 'width': '100%'}),

                                html.Div([
                                    html.Span("Condition: ", style={'font-weight': 'bold'}),
                                    html.Span(id='selected-renovation', style={'margin-left': 'auto'})
                                ], style={'display': 'flex', 'justify-content': 'space-between', 'width': '100%'}),

                                html.Div([
                                    html.Span("Bathroom layout: ", id='selected-sanuzel-label', style={'font-weight': 'bold'}),
                                    html.Span(id='selected-sanuzel', style={'margin-left': 'auto'})
                                ], style={'display': 'flex', 'justify-content': 'space-between', 'width': '100%'}),

                                html.Div([
                                    html.Span("Market type: ", style={'font-weight': 'bold'}),
                                    html.Span(id='selected-bino-turi', style={'margin-left': 'auto'})
                                ], style={'display': 'flex', 'justify-content': 'space-between', 'width': '100%'}),

                                html.Div([
                                    html.Span("Construction type: ", id='selected-qurilish-turi-label', style={'font-weight': 'bold'}),
                                    html.Span(id='selected-qurilish-turi', style={'margin-left': 'auto'})
                                ], style={'display': 'flex', 'justify-content': 'space-between', 'width': '100%'}),

                                # html.Div([
                                #     html.Span("Kelishsa bo'ladimi: ", style={'font-weight': 'bold'}),
                                #     html.Span(id='selected-kelishsa', style={'margin-left': 'auto'})
                                # ], style={'display': 'flex', 'justify-content': 'space-between', 'width': '100%'}),

                                html.Div([
                                    html.Span("Current month and year: ", style={'font-weight': 'bold'}),
                                    html.Span(id='selected-time', style={'margin-left': 'auto'})
                                ], style={'display': 'flex', 'justify-content': 'space-between', 'width': '100%'}),
                                html.Div(
                                    id='time-display',
                                    style={
                                        'position': 'relative',
                                        'margin-top': '10px',
                                        'text-align': 'right',
                                        'font-size': '12px',
                                        'color': 'black'
                                    }
                                ),
                                # Add Baholash button
                                html.Div([
                                    dbc.Button(
                                        'Predict', 
                                        id='submit-button', 
                                        n_clicks=0, 
                                        style={
                                            'width': '200px',
                                            'background-color': '#00264D',
                                            'color': 'white',
                                            'border': 'none',
                                            'border-radius': '30px',
                                            'padding': '8px',
                                            'margin': '20px auto 0 auto'
                                        }
                                    )
                                ], style={
                                    'display': 'flex',
                                    'justify-content': 'center',
                                    'width': '100%',
                                    'margin-top': '20px'
                                }),
                            ], id='all-detail', style={
                                'white-space': 'pre-line',
                                'display': 'flex',
                                'flex-direction': 'column',
                                'gap': '5px',
                                'padding-bottom': '20px'
                            }),
                        ]
                    ),
                ], 
                className='custom-opensauce',
                style={
                    'position': 'relative',
                    'width': '100%',
                    'border-radius': '10px',
                    'white-space': 'pre-line',
                    'height': 'fit-content',
                    'margin-top': '25px',
                    'padding': '20px'
                }
            ),

            # Price Card (moved below details card)
            dbc.Card([
                html.H4("Estimated market price of the apartment", 
                       className='text-center mb-4',
                       style={'fontSize': '24px', 'fontWeight': 'normal', 'marginTop': '15px'}),
                html.Div([
                    dbc.Spinner(
                        html.Div([
                            html.H2(id='house-price',
                                   className='text-center',
                                   style={'fontSize': '48px', 'fontWeight': 'bold', 'marginBottom': '10px'}),
                            html.P(id='price-range',
                                  className='text-center',
                                  style={'fontSize': '16px', 'color': '#666'})
                        ]),
                        color="#00264D",
                        size="lg",
                        type="border"
                    )
                ], style={'minHeight': '150px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
                dbc.Button(
                    "DOWNLOAD FULL REPORT",
                    id='download-button',
                    color="primary",
                    className="w-100 mt-3 mb-3",
                    disabled=True,
                    style={
                        'width': '200px',
                        'backgroundColor': '#00264D',
                        'borderRadius': '30px',
                        'border': 'none',
                        'padding': '8px',
                        'margin': '20px auto',
                        'display': 'block'
                    }
                ),
                dcc.Download(id="download-pdf"),
                dcc.Store(id="form-link-store-home", data=""),
                html.Div([
                    html.A(
                        dbc.Button("Give Feedback", color="secondary"),
                        id="form-link-home",
                        href="",  # updated dynamically
                        target="_blank"
                    )
                ], id='feedback-button-home', style={'display': 'none', 'textAlign': 'center'})
            
            ],
            className='mb-4',
            style={
                'border': '1px solid #ddd',
                'borderRadius': '15px',
                'padding': '20px',
                'marginTop': '20px',
                'backgroundColor': 'white'
            })
        ], style={'width': '100%', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'}),
    ], xs=12, sm=12, md=6, lg=6, style={'padding': '10px'})
])




####################################################################################################
####################################################################################################

# overview = dbc.Row([
#     html.Div([
#         html.Div([
#             html.Iframe(
#                 src="https://app.powerbi.com/view?r=eyJrIjoiZWUxMTBlNDYtN2E4NS00MmM3LTgwMTItZTBmMjcwNDMxYjI5IiwidCI6ImI1OGVhYjJiLTA1YzYtNDcxYi1hYWRhLWNiNjMwY2MyMDJkYyIsImMiOjEwfQ%3D%3D",
#                 style={
#                     'width': '100%',
#                     'height': '85vh',
#                     'border': 'none',
#                     'borderRadius': '10px',
#                     'backgroundColor': 'white'
#                 }
#             )
#         ], className='custom-opensauce', style={
#             'maxWidth': '1200px',
#             'margin': '0 auto',
#             'padding': '40px',
#             'backgroundColor': 'white',
#             'borderRadius': '10px',
#             'marginTop': '20px',
#             'marginBottom': '40px'
#         })
#     ], style={
#         'backgroundColor': 'white',
#         'minHeight': '100vh',
#         'padding': '20px',
#         'width': '100%'
#     })
# ])

####################################################################################################
####################################################################################################


#----app layout----#
app.layout = dbc.Container([
    #---- Header----#
    dbc.Row([
            dbc.Col([
                html.Div([  # Added wrapper div for centering
                html.A(
                href='https://github.com/Temurbek-stack',
                target='_blank',
                children=[
                    html.Img(
                        src='/assets/logo_tk.png',
                                style={'width': '200px'} #10px
                            )
                        ]
                    )
                ], style={
                    'maxWidth': '1400px',
                    'margin': '0 auto',
                    'paddingLeft': '40px',
                    'paddingRight': '0px',
                    'width': '100%'
                })
            ], width='auto', className='fixed-header', style={
                'position': 'fixed',
                'top': 0,
                'left': 0,
                'right': 0,
                'background': 'white',
                'zIndex': 1000,
                'padding': '10px 0',  # Changed padding to only top/bottom
                'margin': 0,
                'width': '100%',
                'border': 'none'
            }),
            
            # Add a spacer div to prevent content from hiding behind the fixed header
            html.Div(style={'height': '40px'}),
        ], justify='left'),

        html.Div([
            html.P(
                "House Price Predictor",
                className = 'custom-telegraf',
                style={'color': '#003049', 'textAlign': 'center', 'margin': '20px', 'fontSize': 50}
                )
        ]),

# Spacer div to prevent content from being hidden under the fixed header
html.Div(style={'height': '5px'}),

    #--- tabs uchun----#
    dbc.Row([
        html.Div([
            html.Div([
        dcc.Tabs(
            id='tabs-components',
            value ='prediction-tab',
            children=[
                dcc.Tab(
                    label='Prediction', 
                    value ='prediction-tab',
                    className = 'custom-tab',
                    selected_className = 'custom-tab--selected'
                ),
                dcc.Tab(
                    label='About the project', 
                    value ='info-tab',
                    className = 'custom-tab',
                    selected_className = 'custom-tab--selected'
                )
                # dcc.Tab(
                #     label='Bozor tahlili', 
                #     value ='overview-tab',
                #     className = 'custom-tab',
                #     selected_className = 'custom-tab--selected'
                # )
            ]
                )
            ], className='tabs-wrapper'),
        html.Div(id='tabs-output')
    ])
    ])
], fluid=True, style={
    'backgroundColor': 'white', 
    'minHeight': '100vh', 
    'padding': '0',
    'margin': '0 auto',
    'maxWidth': '1400px',
    'paddingLeft': '20px',  # Reduced padding for mobile
    'paddingRight': '20px',
    'overflowX': 'hidden'  # Prevent horizontal scrolling
})


######### callbacks ########################################################################################################


#---- app callbacks ----#


@app.callback(
    Output('tabs-output', 'children'),
    Input('tabs-components', 'value')
)

def render_content(tab):
    if tab == 'prediction-tab':
        return prediction
    # elif tab == 'overview-tab':
    #     return overview
    elif tab == 'info-tab':
        return info_tab
    return prediction  # Default to prediction if value is missing


######################### prediction tab callbacks ##########################################################################
##############################################################################################################################


#---- mahalla dropdown-----#
@app.callback(
    Output('mahalla-dropdown', 'options'),
    Input('district-dropdown', 'value')
)
def update_value_dropdown(selected_key):
    if selected_key is None:
        return []  # Return empty list if no district is selected
    
    # Filter the DataFrame
    filtered_df = mahalla_and_tuman[mahalla_and_tuman['district_str'] == selected_key]

    # Convert to dropdown format
    options = [{'label': name, 'value': name} for name in filtered_df['neighborhood_latin'].unique()]

    return options  # Return properly formatted dropdown options
  # Return an empty list if no key is selected
    
    # filtered = df[df['tumanlar']==selected_key]
    # unique_mahalla = filtered['Arentir'].unique().tolist()
    
    # Return the list of values as options for the value-dropdown
    # return [{'label': value, 'value': value} for value in unique_mahalla]
model_is=''
#----df ko'rinishida----#
@app.callback(
    [Output('house-price', 'children'),
     Output('price-range', 'children'),
     Output('time-display', 'children'),
     Output('district-dropdown', 'style'),
     Output('mahalla-dropdown', 'style'),
     Output('area-input', 'style'),
     Output('rooms-input', 'style'),
     Output('floor-input', 'style'),
     Output('total-floors-input', 'style'),
     Output('qurilish-turi-dropdown', 'style'),
     Output('planirovka-dropdown', 'style'),
     Output('sanuzel-dropdown', 'style')],
    [Input('submit-button', 'n_clicks'),
     Input('district-dropdown', 'value'),
     Input('mahalla-dropdown', 'value'),
     Input('area-input', 'value'),
     Input('rooms-input', 'value'),
     Input('floor-input', 'value'),
     Input('total-floors-input', 'value'),
     Input('qurilish-turi-dropdown', 'value'),
     Input('planirovka-dropdown', 'value'),
     Input('sanuzel-dropdown', 'value')],
    [State('mebel-dropdown', 'value'),
    State('atrofda-dropdown', 'value'),
    State('uyda-dropdown', 'value'),
    State('owner-dropdown', 'value'),
    State('renovation-dropdown', 'value'),
    State('bino-turi-dropdown', 'value'),
    #State('kelishsa-dropdown', 'value'),
    State('oy-input', 'value'),
     State('year-input', 'value')],
    prevent_initial_call=True
)
def predict_price(n_clicks, district, mahalla, area, rooms, floor, total_floors, qurilish_turi, planirovka, sanuzel,
                 mebel, atrofda, uyda, owner, renovation, bino_turi , month, year):
    ctx = callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None

    # Default styles for inputs
    default_left_dropdown_style = {
        'width': '100%',
        'border-radius': '30px 0px 0px 30px',
    }
    default_right_dropdown_style = {
        'width': '100%',
        'border-radius': '0px 30px 30px 0px',
        'border-left': '0px',
    }
    default_left_input_style = {
        'width': '100%',
        'border-radius': '30px 0px 0px 30px',
        'border': '1px solid #ccc',
        'padding': '6px'
    }
    default_right_input_style = {
        'width': '100%',
        'border-radius': '0px 30px 30px 0px',
        'border': '1px solid #ccc',
        'border-left': '0px',
        'padding': '6px'
    }
    default_single_dropdown_style = {
        'width': '100%',
        'border-radius': '30px',
    }

    error_left_dropdown_style = {
        'width': '100%',
        'border-radius': '30px 0px 0px 30px',
        'border': '1px solid #dc3545',
    }
    error_right_dropdown_style = {
        'width': '100%',
        'border-radius': '0px 30px 30px 0px',
        'border': '1px solid #dc3545',
        'border-left': '0px',
    }
    error_left_input_style = {
        'width': '100%',
        'border-radius': '30px 0px 0px 30px',
        'border': '1px solid #dc3545',
        'padding': '6px'
    }
    error_right_input_style = {
        'width': '100%',
        'border-radius': '0px 30px 30px 0px',
        'border': '1px solid #dc3545',
        'border-left': '0px',
        'padding': '6px'
    }
    error_single_dropdown_style = {
        'width': '100%',
        'border-radius': '30px',
        'border': '1px solid #dc3545',
    }

    # Initialize all styles as default
    styles = [
        default_left_dropdown_style.copy(),   # district
        default_right_dropdown_style.copy(),  # mahalla
        default_left_input_style.copy(),      # area
        default_right_input_style.copy(),     # rooms
        default_left_input_style.copy(),      # floor
        default_right_input_style.copy(),     # total_floors
        default_single_dropdown_style.copy(), # qurilish_turi
        default_single_dropdown_style.copy(), # planirovka
        default_single_dropdown_style.copy(), # sanuzel
    ]

    # If the callback was triggered by an input change (not the submit button), reset the display
    if trigger_id and trigger_id != 'submit-button':
        return (
            "Click the Predict button",
            "",
            "",
            *styles
        )

    # Only proceed with prediction if the submit button was clicked
    if n_clicks > 0 and trigger_id == 'submit-button':
        # Add 3-second delay
        #time.sleep(3)
        
        required_fields = {
            'hudud': (district is not None and mahalla is not None),
            'area': area is not None and area != '',
            'rooms': rooms is not None and rooms != '',
            'floor': floor is not None and floor != '',
            'total_floors': total_floors is not None and total_floors != '',
            'qurilish_turi': qurilish_turi is not None and qurilish_turi != '',
            'planirovka': planirovka is not None and planirovka != '',
            'sanuzel': sanuzel is not None and sanuzel != ''
        }
        
        # Update styles based on missing fields
        styles = [
            error_left_dropdown_style if not required_fields['hudud'] else default_left_dropdown_style.copy(),    # district
            error_right_dropdown_style if not required_fields['hudud'] else default_right_dropdown_style.copy(),  # mahalla
            error_left_input_style if not required_fields['area'] else default_left_input_style.copy(),          # area
            error_right_input_style if not required_fields['rooms'] else default_right_input_style.copy(),       # rooms
            error_left_input_style if not required_fields['floor'] else default_left_input_style.copy(),         # floor
            error_right_input_style if not required_fields['total_floors'] else default_right_input_style.copy(),# total_floors
            error_single_dropdown_style if not required_fields['qurilish_turi'] else default_single_dropdown_style.copy(), # qurilish_turi
            error_single_dropdown_style if not required_fields['planirovka'] else default_single_dropdown_style.copy(),    # planirovka
            error_single_dropdown_style if not required_fields['sanuzel'] else default_single_dropdown_style.copy(),       # sanuzel
        ]
        
        if not all(required_fields.values()):
            return (
                html.Div("Error", style={'color': '#dc3545'}),  # Red error message
                html.Div("Please fill the required fields.", style={'color': '#dc3545'}),  # Red error message
                "",
                *styles
            )

        updated_dict = my_dict.copy()
        for key in updated_dict.keys():
            updated_dict[key] = 0

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Update the dictionary with the inputs
        updated_dict["totalArea"] = area
        updated_dict["numberOfRooms"] = rooms
        updated_dict["floor"] = floor
        updated_dict["floorOfHouse"] = total_floors
        updated_dict["furnished"] = 1 if mebel == 'Ha' else 0
        updated_dict['handle'] = 1


        # Add in atrofda (multi-select)
        atrofda_keys = {
            "School": "shkola",
            "Supermarket": "supermarket",
            "Shop": "magazini",
            "Parking": "stoyanka",
            "Hospital": "bolnitsa",
            "Polyclinic": "poliklinika",
            "Bus stop": "ostonovki",
            "Playground": "detskaya_ploshatka",
            "Restaurant": "restorani",
            "Cafe": "kafe",
            "Entertainment venues": "razvlekatelnie_zavedeniya",
            "Kindergarten": "detskiy_sad",
            "Green area": "zelyonaya_zona",
            "Park": "park"
        }
        
        if atrofda is not None:
            for key, item in atrofda_keys.items():
                updated_dict[item] = 1 if key in atrofda else 0
        else:
            for item in atrofda_keys.values():
                updated_dict[item] = 0

        # Add in uyda (multi-select)
        uyda_keys = {
            "Refrigerator": "tv_wm_ac_fridge",
            "Telephone": "telefon_internet",
            "Kitchen": "kuxniya",
            "Cable TV": "kabelnoe_tv",
            "Internet": "telefon_internet",
            "Balcony": "balkon",
            "Washing machine": "tv_wm_ac_fridge",
            "Air conditioner": "tv_wm_ac_fridge",
            "Television": "tv_wm_ac_fridge"
        }
                
        if uyda is not None:
            for key, item in uyda_keys.items():
                updated_dict[item] = 1 if key in uyda else 0
        else:
            for item in uyda_keys.values():
                updated_dict[item] = 0

        if mahalla in set(unique_mahalla_olx['neighborhood_code']):
            model = model1
            model_is = 'model1'
        else:
            model = model2
            model_is = 'model2'

        if district:
            filtered_values = mahalla_and_tuman.loc[mahalla_and_tuman['district_str'] == district, 'district_code']
            updated_dict['district_code'] = next(iter(filtered_values), None)

        if mahalla:
            filtered_values = mahalla_and_tuman.loc[mahalla_and_tuman['neighborhood_latin'] == mahalla, 'neighborhood_code']
            updated_dict['neighborhood_code'] = next(iter(filtered_values), None)

        if owner:
            updated_dict[f"ownerType_{owner}"] = 1
        if planirovka:
            updated_dict[f"planType_{planirovka}"] = 1
        if renovation:
            updated_dict[f"repairType_{renovation}"] = 1
        if sanuzel:
            updated_dict[f"bathroomType_{sanuzel}"] = 1
        if bino_turi:
            updated_dict[f"marketType_{bino_turi}"] = 1
        if qurilish_turi:
            updated_dict[f"buildType_{qurilish_turi}"] = 1
        
        updated_dict["pricingMonth"] = month if month is not None else current_month
        updated_dict["pricingYear"] = year if year is not None else current_year

        df_gathrd = pd.DataFrame([updated_dict])
        if model_is == 'model1':
            df_gathrd = df_gathrd
        else:
            df_gathrd = df_gathrd[uybor_cols['Unnamed: 0'].tolist()]
        
        prediction = model.predict(df_gathrd)
        predicted_price = round(prediction[0])
        margin = round(prediction[0] * 0.0361)
        lower_bound = predicted_price - margin
        upper_bound = predicted_price + margin

        # Reset styles to default after successful prediction
        default_styles = [
            default_left_dropdown_style.copy(),   # district
            default_right_dropdown_style.copy(),  # mahalla
            default_left_input_style.copy(),      # area
            default_right_input_style.copy(),     # rooms
            default_left_input_style.copy(),      # floor
            default_right_input_style.copy(),     # total_floors
            default_single_dropdown_style.copy(), # qurilish_turi
            default_single_dropdown_style.copy(), # planirovka
            default_single_dropdown_style.copy(), # sanuzel
        ]

        return (
            f"${predicted_price:,}",
            f"The price might range between ${lower_bound:,} and ${upper_bound:,}",
            current_time,
            *default_styles
        )

    # Default return with initial styles
    return (
        "Click the Predict button",
        "",
        "",
        *styles
    )

@app.callback(
    Output('total-floors-input', 'min'),
    Input('floor-input', 'value'),
)
def update_min_total_floors(floor_value):
    # Ensure the total floors input minimum value is at least the floor number
    if floor_value is not None:
        return floor_value
    # Default min value when no floor value is provided
    return 1

@app.callback(
    Output('selected-hudud', 'children'),
    [Input('district-dropdown', 'value'),
     Input('mahalla-dropdown', 'value')]
)
def update_hudud(district, mahalla):
    if district and mahalla:
        return f"{district}, {mahalla}"
    elif district:
        return district
    return ""

@app.callback(
    Output('selected-area', 'children'),
    [Input('area-input', 'value')]
)
def update_area(area):
    if area:
        return f"{area}m²"
    return ""

@app.callback(
    Output('selected-rooms', 'children'),
    [Input('rooms-input', 'value')]
)
def update_rooms(rooms):
    if rooms:
        return str(rooms)
    return ""

@app.callback(
    Output('selected-floor', 'children'),
    [Input('floor-input', 'value')]
)
def update_floor(floor):
    if floor:
        return str(floor)
    return ""

@app.callback(
    Output('selected-total-floors', 'children'),
    [Input('total-floors-input', 'value')]
)
def update_total_floors(total_floors):
    if total_floors:
        return str(total_floors)
    return ""

@app.callback(
    Output('selected-mebel', 'children'),
    [Input('mebel-dropdown', 'value')]
)
def update_mebel(mebel):
    if mebel:
        return str(mebel)
    return ""

@app.callback(
    Output('selected-atrofda', 'children'),
    [Input('atrofda-dropdown', 'value')]
)
def update_atrofda(atrofda):
    if atrofda:
        return ", ".join(atrofda)
    return ""

@app.callback(
    Output('selected-uyda', 'children'),
    [Input('uyda-dropdown', 'value')]
)
def update_uyda(uyda):
    if uyda:
        return ", ".join(uyda)
    return ""

@app.callback(
    Output('selected-owner', 'children'),
    [Input('owner-dropdown', 'value')]
)
def update_owner(owner):
    if owner:
        return str(owner)
    return ""

@app.callback(
    Output('selected-planirovka', 'children'),
    [Input('planirovka-dropdown', 'value')]
)
def update_planirovka(planirovka):
    planirovka_labels = {
        'Alohida_ajratilgan': 'Separate layout',
        'Aralash': 'Mixed',
        'Aralash_alohida': 'Mixed with separate areas',
        'Kichik_oilalar_uchun': 'For small families',
        'Ko_p_darajali': 'Multi-level',
        'Pentxaus': 'Penthouse',
        'Studiya': 'Studio'
    }
    if planirovka:
        return planirovka_labels.get(planirovka, planirovka)
    return ""

@app.callback(
    Output('selected-renovation', 'children'),
    [Input('renovation-dropdown', 'value')]
)
def update_renovation(renovation):
    if renovation:
        return str(renovation)
    return ""

@app.callback(
    Output('selected-sanuzel', 'children'),
    [Input('sanuzel-dropdown', 'value')]
)
def update_sanuzel(sanuzel):
    sanuzel_labels = {
        '2_va_undan_ko_p_sanuzel': '2 or more bathrooms',
        'Alohida': 'Separate',
        'Aralash': 'Combined'
    }
    if sanuzel:
        return sanuzel_labels.get(sanuzel, sanuzel)
    return ""

@app.callback(
    Output('selected-bino-turi', 'children'),
    [Input('bino-turi-dropdown', 'value')]
)
def update_bino_turi(bino_turi):
    bino_turi_labels = {
        'Ikkilamchi_bozor': 'Secondary',
        'Yangi_qurilgan_uylar': 'Newly built'
    }
    if bino_turi:
        return bino_turi_labels.get(bino_turi, bino_turi)
    return ""

@app.callback(
    Output('selected-qurilish-turi', 'children'),
    [Input('qurilish-turi-dropdown', 'value')]
)
def update_qurilish_turi(qurilish_turi):
    qurilish_turi_labels = {
        'Blokli': 'Block',
        'G_ishtli': 'Brick',
        'Monolitli': 'Monolithic',
        'Panelli': 'Panel',
        'Yog_ochli': 'Wooden'
    }
    if qurilish_turi:
        return qurilish_turi_labels.get(qurilish_turi, qurilish_turi)
    return ""

# @app.callback(
#     Output('selected-kelishsa', 'children'),
#     [Input('kelishsa-dropdown', 'value')]
# )
# def update_kelishsa(kelishsa):
#     kelishsa_labels = {
#         'Yes': 'Yes',
#         'No': 'No'
#     }
#     if kelishsa:
#         return kelishsa_labels.get(kelishsa, kelishsa)
#     return ""

@app.callback(
    Output('selected-time', 'children'),
    [Input('oy-input', 'value'),
     Input('year-input', 'value')]
)
def update_time(month, year):
    if month and year:
        return f"{month}-{year}"
    return ""

@app.callback(
    Output('download-button', 'disabled'),
    [Input('house-price', 'children')]
)
def toggle_download_button(price):
    if price and price != "Click the Predict button" and not isinstance(price, dict):
        return False
    return True

@app.callback(
    Output("download-pdf", "data"),
    Input("download-button", "n_clicks"),
    [State('selected-hudud', 'children'),
     State('selected-area', 'children'),
     State('selected-rooms', 'children'),
     State('selected-floor', 'children'),
     State('selected-total-floors', 'children'),
     State('selected-mebel', 'children'),
     State('selected-atrofda', 'children'),
     State('selected-uyda', 'children'),
     State('selected-owner', 'children'),
     State('selected-planirovka', 'children'),
     State('selected-renovation', 'children'),
     State('selected-sanuzel', 'children'),
     State('selected-bino-turi', 'children'),
     State('selected-qurilish-turi', 'children'),
     #State('selected-kelishsa', 'children'),
     State('selected-time', 'children'),
     State('house-price', 'children'),
     State('price-range', 'children')],
    prevent_initial_call=True
)
def generate_pdf(n_clicks, hudud, area, rooms, floor, total_floors, mebel, atrofda, uyda, 
                owner, planirovka, renovation, sanuzel, bino_turi, qurilish_turi, 
                time_value, price, price_range):
    if not n_clicks:
        return no_update
        
    # Create a dictionary of property details
    property_details = {
        'Region': hudud,
        'Area': area,
        'Number of rooms': rooms,
        'Floor': floor,
        'Total number of floors': total_floors,
        'Furnished': mebel,
        'Nearby': atrofda,
        'Available in the house': uyda,
        'Ownership type': owner,
        'Layout': planirovka,
        'Renovation type': renovation,
        'Bathroom': sanuzel,
        'Market type': bino_turi,
        'Construction type': qurilish_turi,
        #'Negotiable': kelishsa,
        'Evaluation time': time_value
    }
    
    # Generate PDF
    try:
        pdf_bytes = create_report(property_details, price.replace('$', '').replace(',', ''), price_range)
        
        # Return the PDF as a download
        return dcc.send_bytes(pdf_bytes, f"linkhome_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return no_update


@app.callback(
    Output('feedback-button-home', 'style'),
    [
        Input('submit-button', 'n_clicks'),
        Input('area-input', 'value'),
        Input('rooms-input', 'value'),
        Input('district-dropdown', 'value'),
        Input('mahalla-dropdown', 'value'),
        Input('floor-input', 'value'),
        Input('total-floors-input', 'value'),
        Input('atrofda-dropdown', 'value'),
        Input('mebel-dropdown', 'value'),
        Input('uyda-dropdown', 'value'),
        Input('qurilish-turi-dropdown', 'value'),
        Input('planirovka-dropdown', 'value'),
        Input('sanuzel-dropdown', 'value'),
        Input('owner-dropdown', 'value'),
        Input('renovation-dropdown', 'value'),
        Input('bino-turi-dropdown', 'value'),
        #Input('kelishsa-dropdown', 'value'),
        Input('oy-input', 'value'),
        Input('year-input', 'value'),
    ],
    prevent_initial_call=True
)
def toggle_feedback_button_home(*args):
    trigger_id = ctx.triggered_id

    if trigger_id and trigger_id == 'submit-button':
        return {'display': 'block', 'textAlign': 'center'}
    return {'display': 'none'}

@app.callback(
    Output('form-link-home', 'href'),
    Input('price-range', 'children'),
    prevent_initial_call=True
)
def update_form_link_home(price_range):
    if isinstance(price_range, dict):
        clean_range = price_range['label'].split(" baholanishi")[0].strip()
    else:
        clean_range = price_range.split(" baholanishi")[0].strip()
    #clean_range = price_range.split(" baholanishi")[0].strip()
    form_base = "https://docs.google.com/forms/d/e/1FAIpQLSf_MZZeVhJc9uqd9dAB6fKtcAUMaWFEIyM8ZX_Qysi1Ja1plw/viewform?usp=pp_url"
    field_id = "entry.2124633396"  # Replace with your field's actual entry ID
    return f"{form_base}&{field_id}={clean_range.replace(' ', '+')}"




if __name__ == '__main__':
    app.run(debug=True)