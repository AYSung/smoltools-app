from bokeh.models.widgets.tables import NumberFormatter
import pandas as pd
import panel as pn
import panel.widgets as pnw


def make_distance_table(df: pd.DataFrame, cutoff: float) -> pnw.DataFrame:
    return pnw.DataFrame(
        value=df.loc[lambda x: x.delta_distance >= cutoff],
        titles={
            'atom_id_1': 'Res #1',
            'atom_id_2': 'Res #2',
            'distance_a': 'Distance in A (\u212B)',
            'distance_b': 'Distance in B (\u212B)',
            'delta_distance': '\u0394Distance (\u212B)',
        },
        formatters={
            'distance_a': NumberFormatter(format='0.0'),
            'distance_b': NumberFormatter(format='0.0'),
            'delta_distance': NumberFormatter(format='0.0'),
        },
        show_index=False,
        height=500,
        disabled=True,
    )


def make_distance_widget(df: pd.DataFrame):
    delta_distance_input = pnw.FloatInput(
        name='\u0394Distance cutoff (\u212B)', value=20
    )
    # sasa_input = pnw.FloatSlider(name='SASA cutoff', start=0, end=1.0)

    distance_table = pn.bind(make_distance_table, df=df, cutoff=delta_distance_input)

    return pn.Card(
        delta_distance_input,
        pn.Tabs(('Table', distance_table)),
        sizing_mode='stretch_both',
        title='Pairwise Distances',
        collapsible=False,
    )
