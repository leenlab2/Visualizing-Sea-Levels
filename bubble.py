"""Generate a bubble map of locations at risk of flooding"""
from typing import Dict
import plotly.express as px
import pandas as pd


def draw_map(data: Dict[str, list]) -> None:
    """Draw a bubble map of the data using plotly express."""
    df = pd.DataFrame.from_dict(data)
    df.head()
    df['text'] = 'Height below sea level: ' + (df['diff']).astype(str) + ' m'

    fig = px.scatter_geo(df,
                         lon='lon',
                         lat='lat',
                         hover_name='text',
                         size="diff",
                         animation_frame='year',
                         category_orders={"year": [2020, 2030, 2040, 2050, 2060,
                                                   2070, 2080, 2090, 2100]}
                         )

    fig.update_layout(
        title_text='Areas at risk of flooding in the next century',
        showlegend=False,
        geo=dict(
            scope='north america',
            landcolor='rgb(217, 217, 217)',
            lataxis=dict(range=[40, 84]),
            lonaxis=dict(range=[-146, -50])
        )
    )

    fig.show()
