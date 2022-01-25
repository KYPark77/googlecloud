
#dataset1 국내발생현황dataset(신규발생)
from datetime import datetime
import pandas as pd
from urllib.request import urlopen
import plotly.express as px
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.colors import DEFAULT_PLOTLY_COLORS
import numpy as np
from plotly.figure_factory import create_table
import plotly.figure_factory as ff
from dash import dash_table
from collections import OrderedDict

sdate ='20200101'
edate = datetime.today().strftime('%Y%m%d')

key = 'V59JmNTE9hQe%2BX8dhNSZ0BSt%2Bs0EKifIFGOq%2BB44QQY1EqpEJ0nv7HSVnIVjNdX5t9YgPA%2B2tZso2E9MlMBQ8Q%3D%3D'
sdate ='20200101'
edate = datetime.today().strftime('%Y%m%d')
url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson?serviceKey='+key+'&pageNo=1&numOfRows=10&startCreateDt='+sdate+'&endCreateDt='+edate
df = pd.read_xml(url, xpath = './/item')
df['Year']=df['stdDay'].str[:4]
df['month']=df['stdDay'].str[6:8]
df['day']=df['stdDay'].str[10:12]
df['date']=df['Year']+df['month']+df['day']
df['date'] = pd.to_datetime(df['date'])
df = df[df.date!='20210104']
df = df[df.date!='20210901']
df = df[df.date!='20210902']
now = df['date'].unique()
now=max(now)
now1 = pd.to_datetime(str(now))
now1 = now1.strftime('%Y-%m-%d')
day1 = now - pd.Timedelta(1, unit='days')
day31 = now - pd.Timedelta(31, unit='days')

days=[now,day1]
df1 = df[df['date'].isin(days)]
new_case = df.pivot(index='gubun', columns = 'date', values = 'incDec')
new_case1 = new_case.transpose()
new_case1.reset_index(inplace=True)
reg = ['합계','서울','경기','충남','세종']

df['createDt'] = pd.to_datetime(df['createDt'])
df = df.rename(columns={'incDec':'신규확진자(명)','gubun':'지역', 'date':'일자'})
df = df.loc[df['createDt']>day31]

new_df = df[df['지역'] != '합계']
new_df1 = df[df['지역'] == '합계']


new_bar = px.bar(new_df, x='일자', y='신규확진자(명)', hover_data=['지역'], color='지역', text = '지역')
new_bar.update_layout(title='<b>최근 30일 신규확진자 지역별 발생 추이</b>',template = 'simple_white')
new_bar.add_trace(
    go.Scatter(x=new_df1["일자"], y = new_df1["신규확진자(명)"],
               name = "합계",
               mode = "lines+text"))
new_bar.update_traces(textfont_size=7)
new_bar.update_xaxes(title=None)
new_bar.update_yaxes(title=None)
Max = max(new_df1['신규확진자(명)'])
Min = min(new_df1['신규확진자(명)'])
new_bar.add_annotation(x=(new_df1[new_df1['신규확진자(명)'] == max(new_df1['신규확진자(명)'])]['일자'].iloc[0]),
                       y=Max,
                       text="Max:"+ f'{Max:,.0f}',
                       showarrow=True,
                       arrowhead=1)
new_bar.add_annotation(x=(new_df1[new_df1['신규확진자(명)'] == min(new_df1['신규확진자(명)'])]['일자'].iloc[0]),
                       y=Min,
                       text="Min:"+ f'{Min:,.0f}',
                       showarrow=True,
                       arrowhead=1)


#국내발생현황_Table(사망/백신접종)

target_url = 'https://ncv.kdca.go.kr/mainStatus.es?mid=a11702000000'
df2 = pd.read_html(target_url, encoding = "utf-8", header = 0)[0]
pop=51305184
df2=df2.transpose()
df2 = df2.rename(columns=df2.iloc[0])
df2 = df2.drop(['구분'])
df2['비율'] = ((df2['당일 누적A + B']/pop).apply('{:.1%}'.format))
df2.reset_index(inplace=True)
df2 = df2.drop(['전일 누적B','당일 실적A','당일 누적A + B'], axis=1)
df2 = df2.rename(columns={'index':'백신접종현황'})

url2 = 'http://ncov.mohw.go.kr/'
df3 = pd.read_html(url2, encoding = "utf-8",header = 0)[0]
df3 = df3.drop(['확진'], axis=1)
df3 = df3.transpose()
df3 = df3.rename(columns=df3.iloc[0])
df3 = df3.drop(['구분'])
df3.reset_index(inplace=True)
df3 = df3.rename(columns={'index':'사망/재원 위중증/신규 입원','일일':'전일','최근 7일간일평균':'직전7일 평균'})


#국내발생현황_연령별,성별
key3 = "V59JmNTE9hQe%2BX8dhNSZ0BSt%2Bs0EKifIFGOq%2BB44QQY1EqpEJ0nv7HSVnIVjNdX5t9YgPA%2B2tZso2E9MlMBQ8Q%3D%3D"
url3 = "http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19GenAgeCaseInfJson?serviceKey="+key3+'&pageNo=1&numOfRows=10&startCreateDt='+sdate+'&endCreateDt='+edate
df4 = pd.read_xml(url3, xpath = './/item')
age = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69',
       '70-79', '80 이상']
age_df = df4[df4['gubun'].isin(age)]
sex_df = df4[df4['gubun'].isin(['남성','여성'])]
age_df = age_df.rename(columns={'confCase':'확진자','createDt':'일자','gubun':'연령대'})
age_df['date'] = pd.to_datetime(age_df['일자'])
now = age_df['date'].unique()
now=max(now)

day31 = now - pd.Timedelta(31, unit='days')
age_df = age_df.loc[age_df['date']>day31]

age_df['date'] = age_df['date'].dt.date
age_df1 = pd.pivot_table(age_df, index = ['date'], aggfunc='sum')
age_df1 = age_df1.reset_index()

age_bar = px.bar(age_df, x='date', y='확진자', hover_data=['연령대'], color='연령대')
age_bar.update_layout(title='<b>최근 30일 누적확진자 연령별 발생 추이</b>',template = 'simple_white')
age_bar.add_trace(
    go.Scatter(x=age_df1['date'], y = age_df1["확진자"],
               name = "합계"))
age_bar.update_xaxes(title=None)
age_bar.update_yaxes(title=None)
Max1 = max(age_df1['확진자'])
Min1 = min(age_df1['확진자'])
age_bar.add_annotation(x=(age_df1[age_df1['확진자'] == max(age_df1['확진자'])]['date'].iloc[0]),
                       y=Max1,
                       text="Max:"+ f'{Max1:,.0f}',
                       showarrow=True,
                       arrowhead=1)
age_bar.add_annotation(x=(age_df1[age_df1['확진자'] == min(age_df1['확진자'])]['date'].iloc[0]),
                       y=Min1,
                       text="Min:"+ f'{Min1:,.0f}',
                       showarrow=True,
                       arrowhead=1)


#국내발생현황_기초자치단체

key = 'V59JmNTE9hQe%2BX8dhNSZ0BSt%2Bs0EKifIFGOq%2BB44QQY1EqpEJ0nv7HSVnIVjNdX5t9YgPA%2B2tZso2E9MlMBQ8Q%3D%3D'
url11 = 'http://apis.data.go.kr/1741000/DisasterMsg3/getDisasterMsg1List?serviceKey='+key+'&pageNo=1&numOfRows=1000'
url12 = 'http://apis.data.go.kr/1741000/DisasterMsg3/getDisasterMsg1List?serviceKey='+key+'&pageNo=2&numOfRows=1000'
url13 = 'http://apis.data.go.kr/1741000/DisasterMsg3/getDisasterMsg1List?serviceKey='+key+'&pageNo=3&numOfRows=1000'
df41 = pd.read_xml(url11, xpath = './/row')
df42 = pd.read_xml(url12, xpath = './/row')
df43 = pd.read_xml(url13, xpath = './/row')


df6=pd.concat([df41,df42,df43],ignore_index=True)
new_local = df6[df6['location_name'].isin(['충청남도 공주시','경기도 성남시','경기도 파주시','경기도 안성시'])]
new_local =new_local[new_local['msg'].str.contains('확진자')]
new_local['new'] = new_local["msg"].str.extract('(\d+명)')
new_local['new'] = new_local['new'].str.extract('(\d+)')
new_local['new'] = pd.to_numeric(new_local['new'])
new_local['date2'] = pd.to_datetime(new_local['create_date'], infer_datetime_format=True)
new_local['date'] = new_local["date2"].dt.strftime("%Y-%m-%d")
date =new_local['date2'].unique()

now = max(date)
day7 = now - pd.Timedelta(7, unit='days')
day7 = day7.strftime('%Y-%m-%d')
new_local = new_local.loc[new_local['date2']>day7]

#세계정보
covid_data = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv')
covid_data['date1'] = pd.to_datetime(covid_data['date'])
covid_data = covid_data.sort_values(by='date1', ascending=True)
covid_data = covid_data.rename(columns={'location': 'Index'})
covid_data['Index'] = covid_data['Index'].str.replace(" ", "_")
nation = covid_data['Index'].unique()
covid_data1 = covid_data[['continent', 'Index', 'date', 'total_cases', 'total_deaths', 'people_vaccinated',
                          'people_fully_vaccinated', 'total_boosters', 'population', 'new_cases', 'new_deaths']]
days = pd.DataFrame(covid_data['date'].unique(), columns=['date'])
for i in nation:
    vars()[i] = pd.DataFrame()
    vars()[i] = covid_data1[covid_data1['Index'] == i]
    vars()[i] = pd.merge(days, vars()[i], how='outer', on='date')
    vars()[i][['new_cases', 'new_deaths']] = vars()[i][['new_cases', 'new_deaths']].fillna(0)
    vars()[i] = vars()[i].fillna(method='pad')
    vars()[i] = vars()[i].fillna(0)
    vars()[i] = vars()[i].drop_duplicates(['date'], keep='first')
covid_total = pd.DataFrame()

for c in nation:
    covid_total = pd.concat([covid_total, vars()[c]])
covid_total = covid_total.drop_duplicates()
covid_total = covid_total.copy()
covid_total['누적확진자'] = covid_total['total_cases'].astype(float).map('{:,.0f}'.format)
covid_total['누적사망자'] = covid_total['total_deaths'].astype(float).map('{:,.0f}'.format)
covid_total['신규확진자'] = covid_total['new_cases'].astype(float).map('{:,.0f}'.format)
covid_total['신규사망자'] = covid_total['new_deaths'].astype(float).map('{:,.0f}'.format)
covid_total['총인구'] = (covid_total['population'] / 1000000).map('{:,.1f}M'.format)
covid_total['확진율'] = ((covid_total['total_cases'] / covid_total['population']).apply('{:.1%}'.format))
covid_total['치사율'] = ((covid_total['total_deaths'] / covid_total['total_cases']).apply('{:.1%}'.format))
covid_total['백신접종율'] = ((covid_total['people_vaccinated'] / covid_total['population']).apply('{:.1%}'.format))
covid_total['백신접종완료율'] = ((covid_total['people_fully_vaccinated'] / covid_total['population']).apply('{:.1%}'.format))
covid_total['백신3차접종율'] = ((covid_total['total_boosters'] / covid_total['population']).apply('{:.1%}'.format))
covid_total['date1'] = pd.to_datetime(covid_total['date'])
today = max(covid_total['date1'].unique())
covid_today = covid_total[covid_total['date1'] == today]
soul = ['South_Korea', 'United_States', 'China', 'Malaysia', 'Hungary']
soul_world = covid_today[covid_today['Index'].isin(soul)]
soul_world = soul_world[
    ['Index', '총인구', '신규확진자', '누적확진자', '확진율',
     '신규사망자', '누적사망자', '치사율', '백신접종율', '백신접종완료율', '백신3차접종율']]
soul_world1 = soul_world.transpose()
soul_world1 = soul_world1.reset_index()
headers = soul_world1.iloc[0]
soul_world2  = pd.DataFrame(soul_world1.values[1:], columns=headers)
list = ['World', 'High_income', 'Europe',
        'European_Union', 'North_America', 'Upper_middle_income',
        'Asia', 'Lower_middle_income', 'South_America', 'Africa','Low_income', 'Oceania','International']

for i in list:
    covid_total = covid_total[covid_total['Index'] != i]

covid_today = covid_total[covid_total['date1'] == today]
covid_today1 = covid_today.sort_values(by='new_cases', ascending=False)
covid_today1['Rank'] = covid_today1['new_cases'].rank(method='min', ascending=False)
covid_today1['Rank'] = covid_today1['Rank'].astype(float).map('{:,.0f}'.format)
covid_today1= covid_today1[['Index','신규확진자','누적확진자','확진율','신규사망자','누적사망자','치사율','총인구','백신접종율','백신접종완료율','백신3차접종율']]
covid_today2 = covid_today.sort_values(by = 'population', ascending = False)

wtoday = max(covid_total['date'].unique())
covid_today3 = pd.DataFrame(
    OrderedDict([(name, col_covid_today1) for (name, col_covid_today1) in covid_today1.items()])
)

continent = ['Asia','North America', 'Europe','Africa','South America','Oceania']

# Layout
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash import html


app = dash.Dash(title="Covid19 DashBoard", external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

Title = dbc.Row(
    dbc.Alert(
        [
            html.H4('코로나19 발생현황(국내)', style={"font_family":"Malgun Gothic", 'font-weight': 'bold',"text-align":"center", 'margin-top':'0', 'margin-boottom':'0'}),
            html.P("Updated(0시 기준) : " + str(now1), style={"font_family":"Malgun Gothic", "text-align":"center",'margin-top':'0', 'margin-boottom':'0'})
         ],id = "id_date",style = {'margin-top':'0', 'margin-boottom':'0'}), style = {'margin-top':'0', 'margin-boottom':'0'})


Indicator = dbc.Row([
    dbc.Col([dcc.Graph(id="합계",style={"width":"100%"})]),
    dbc.Col([dcc.Graph(id="서울", style={"width": "100%"})]),
    dbc.Col([dcc.Graph(id="경기",style={"width":"100%"})]),
    dbc.Col([dcc.Graph(id="충남", style={"width": "100%"})]),
    dbc.Col([dcc.Graph(id="세종", style={"width": "100%"})]),
    ])

subplot = dbc.Row(
    children = [
    dbc.Col([dcc.Graph(id="local", style={"width": "100%"})])
])

Table = dbc.Row([
    dbc.Col([dbc.Table.from_dataframe(df3, striped=True, bordered=True, hover=True,style = {"font_family":"Malgun Gothic", 'font-weight': 'bold',"text-align":"center"})],width=6),
    dbc.Col([dbc.Table.from_dataframe(df2, striped=True, bordered=True, hover=True,style = {"font_family":"Malgun Gothic", 'font-weight': 'bold',"text-align":"center"})],width=6)
    ])

Line = dbc.Row(
    children =[
    dbc.Col([dcc.Graph(figure=new_bar,style={"width":"100%"})],width=6),
    dbc.Col([dcc.Graph(figure=age_bar,style={"width":"100%"})],width=6),
    ])

Title2 = dbc.Row(
    dbc.Alert(
        [
            html.H4('코로나19 발생현황(세계)', style={"font_family":"Malgun Gothic", 'font-weight': 'bold',"text-align":"center", 'margin-top':'0', 'margin-boottom':'0'}),
            html.P("Updated : " + str(wtoday), style={"font_family":"Malgun Gothic", "text-align":"center",'margin-top':'0', 'margin-boottom':'0'})
         ],style = {'margin-top':'0', 'margin-boottom':'0'}), style = {'margin-top':'0', 'margin-boottom':'0'})

Wline = dbc.Row([
    dbc.Col([dcc.Graph(id = 'wtable',style={"width":"100%",'height':"400"})],width=6),
    dbc.Col([dash_table.DataTable(
        data=covid_today3.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in covid_today3.columns],
        page_size=12,
        style_cell={'font-weight': 'bold',"text-align":"center", 'font-family':'Malgun Gothic','fontSize':'5'},
        style_table={'overflowX': 'auto'})
    ],width = 6)
])

select_countries = dbc.Row([
    dbc.Col([
        dbc.Row([
            dcc.Dropdown(id = '대륙',
                         options=[{'label':c,'value':c} for c in continent],
                         placeholder="Select a Continent",
                         value='Asia'),

        ]),
        dbc.Row([
            dcc.Dropdown(id = "countries", placeholder="Select a Country", value="Japan")
        ]),
        dbc.Row([dcc.Graph(id = "new_cases")]),
        dbc.Row([dcc.Graph(id = "new_deaths")]),
        dbc.Row([dcc.Graph(id="vac")])
    ], width = 3),
    dbc.Col([dcc.Graph(id = "country_new")],width=9)
])

app.layout = dbc.Container([
    Title,
    Indicator,
    subplot,
    Table,
    Line,
    Title2,
    Wline,
    select_countries
])

#Dropdown 설정

@app.callback(
    Output("countries", "options"),
    Input("대륙", "value")
)
def update_options(selected_country):
    return [{'label': o, 'value':o} for o in (covid_today2[covid_today2['continent'] == selected_country]['Index'].unique())]

#Select_country

@app.callback(
    Output('new_cases', 'figure'),
    Input('countries', 'value'))
def update_output(value):
    figure = []

    W_value = covid_total[covid_total['Index'] == value]['new_cases'].iloc[-1]
    W_delta = covid_total[covid_total['Index'] == value]['new_cases'].iloc[-2]

    fig = go.Figure(go.Indicator(
        mode='number+delta',
        value=W_value,
        number=dict(font_size=25, valueformat=","),
        delta=dict(reference=W_delta,
                   font_size=20,
                   relative=False,
                   valueformat=",",
                   increasing_color='Red',
                   decreasing_color='Blue',
                   position='top'),
        title=dict(text="<b>New Cases</b>", font_size=20)))
    fig.update_layout(height=100)

    return fig

@app.callback(
    Output('new_deaths', 'figure'),
    Input('countries', 'value'))
def update_output(value):
    figure = []

    W_value = covid_total[covid_total['Index'] == value]['new_deaths'].iloc[-1]
    W_delta = covid_total[covid_total['Index'] == value]['new_deaths'].iloc[-2]

    fig = go.Figure(go.Indicator(
        mode='number+delta',
        value=W_value,
        number=dict(font_size=25, valueformat=","),
        delta=dict(reference=W_delta,
                   font_size=20,
                   relative=False,
                   valueformat=",",
                   increasing_color='Red',
                   decreasing_color='Blue',
                   position='top'),
        title=dict(text="<b>New deaths</b>", font_size=20)))
    fig.update_layout(height=100)

    return fig

@app.callback(
    Output('vac', 'figure'),
    Input('countries', 'value'))

def update_output(value):
    figure = []

    firstvac = (covid_total[covid_total['Index'] == value]['백신접종율'].iloc[-1])
    secondvac = (covid_total[covid_total['Index'] == value]['백신접종완료율'].iloc[-1])
    thirdvac = (covid_total[covid_total['Index'] == value]['백신3차접종율'].iloc[-1])


    x= ['1차','2차','3차']
    y= [firstvac,secondvac,thirdvac]

    vac_df = pd.DataFrame([x for x in zip(x, y)])
    vac_df = vac_df.rename(columns = {0:'구분',1:'백신접종율'})


    fig = ff.create_table(vac_df)


    return fig

#국가별 발생추이

@app.callback(
    Output('country_new', 'figure'),
    Input('countries', 'value'))

def update_output(value):

    figure = []

    country_newdf = covid_total[covid_total['Index'] == value].tail(30)

    fig = px.bar(country_newdf,x='date',y= 'new_cases',template="simple_white", title ="<b>최근 30일간 신규확진자 발생추이</b>")
    fig.update_xaxes(title=None)
    fig.update_yaxes(title=None)
    Max = max(country_newdf['new_cases'])
    fig.add_annotation(x=(country_newdf[country_newdf['new_cases'] == max(country_newdf['new_cases'])]['date'].iloc[0]),
                       y=Max,
                       text="Max:" + f'{Max:,.0f}',
                       showarrow=True,
                       arrowhead=1)
    return fig

#indicator

@app.callback([Output('합계',  'figure'),
               Output('서울', 'figure'),
               Output('경기',    'figure'),
               Output('충남',  'figure'),
               Output('세종', 'figure')],
              [Input('id_date', now1)])

def update_output(val):

    figures = []
    # data by Region
    for i in range(len(reg)):
        df_fig = new_case1[['date', reg[i]]]
        df_fig1 = df_fig[df_fig['date'] == now1]
        df_fig2 = df_fig[df_fig['date'] == day1]
        values = df_fig1[reg[i]].values[0]
        deltas = df_fig2[reg[i]].values[0]

        trace = go.Indicator(mode='number+delta',
                             value=values,
                             number=dict(font_size=25,
                                         valueformat=","),
                             delta=dict(reference=deltas,
                                        font_size=20,
                                        relative=False,
                                        valueformat=",",
                                        increasing_color='Red',
                                        decreasing_color='Blue',
                                        position='top'),
                             title=dict(text=reg[i], font_size=20)
                             )
        data = [trace]
        layout = go.Layout(height=100)
        figure = go.Figure(data, layout)
        figures.append(figure)

    return figures[0], figures[1], figures[2], figures[3], figures[4]

#local

@app.callback(
    Output('local', 'figure'),
    Input('id_date', now1))

def update_output(val):

    fig = make_subplots(
        rows=1, cols=4, subplot_titles=("성남시", "공주시", "파주시", "안성시")
    )

    # Subplot 1
    fig.add_trace(
        go.Bar(
            x=new_local[new_local['location_name'] == '경기도 성남시']['date'],
            y=new_local[new_local['location_name'] == '경기도 성남시']['new'],
            name='경기도 성남시'), row=1, col=1)

    fig.add_trace(
        go.Bar(
            x=new_local[new_local['location_name'] == '충청남도 공주시']['date'],
            y=new_local[new_local['location_name'] == '충청남도 공주시']['new'],
            name='충청남도 공주시'), row=1, col=2)

    fig.add_trace(
        go.Bar(
            x=new_local[new_local['location_name'] == '경기도 파주시']['date'],
            y=new_local[new_local['location_name'] == '경기도 파주시']['new'],
            name='경기도 파주시'), row=1, col=3)

    fig.add_trace(
        go.Bar(
            x=new_local[new_local['location_name'] == '경기도 안성시']['date'],
            y=new_local[new_local['location_name'] == '경기도 안성시']['new'],
            name='경기도 안성시'), row=1, col=4)
    fig.update_traces(texttemplate='<b>%{y}</b>', textposition='auto')
    fig.update_layout(title_text="<b>솔브레인그룹 소재지역 발생현황(최근 7일)</b>", height = 300,showlegend=False)

    return fig

#세계정보Table1 : 솔브레인그룹 진출국가

@app.callback(
    Output('wtable', 'figure'),
    Input('id_date', now1))

def update_output(val):

    fig = ff.create_table(soul_world2)
    return fig

#세계정보 : W-country 코로나정보





if __name__ == "__main__":
    app.run_server(debug=Ture, host="0.0.0.0", port=8080)
