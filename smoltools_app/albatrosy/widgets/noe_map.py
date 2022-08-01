import pandas as pd
import panel as pn
import panel.widgets as pnw
import param

from smoltools import albatrosy

from common.widgets import table
from common.widgets.containers import centered_row


def make_monomer_noe_widget(data: dict[str, pd.DataFrame]) -> pn.Card:
    combined_distances = albatrosy.splice_conformation_tables(
        data['a'],
        data['b'],
        chain_a_id=data['chain_a_id'],
        chain_b_id=data['chain_b_id'],
    )

    noe_map_a = pn.pane.Vega(albatrosy.plots.noe_map(data['a']))
    noe_map_b = pn.pane.Vega(albatrosy.plots.noe_map(data['b']))
    combined_noe_map = pn.pane.Vega(albatrosy.plots.spliced_noe_map(combined_distances))

    return pn.Card(
        pn.Tabs(
            ('Combined', centered_row(combined_noe_map)),
            ('Conformation A', centered_row(noe_map_a)),
            ('Conformation B', centered_row(noe_map_b)),
            align='center',
        ),
        title='NOE Maps',
        collapsible=False,
        width=900,
    )


def make_dimer_noe_widget(data: dict[str, pd.DataFrame]) -> pn.Card:
    combined_distances = albatrosy.splice_conformation_tables(
        data['a'],
        data['b'],
        chain_a_id=data['chain_a_id'],
        chain_b_id=data['chain_b_id'],
    )
    intra_chain_noe_map = pn.pane.Vega(
        albatrosy.plots.spliced_noe_map(combined_distances)
    )
    inter_chain_noe_map = pn.pane.Vega(
        albatrosy.plots.interchain_noe_map(
            data['delta'],
            x_title=data['chain_a_id'],
            y_title=data['chain_b_id'],
        )
    )

    chain_a_table_data = (
        data['a']
        .pipe(albatrosy.add_noe_bins)
        .loc[
            lambda x: albatrosy.lower_triangle(x) & (x.noe_strength != 'none'),
            ['id_1', 'id_2', 'distance', 'noe_strength'],
        ]
        .sort_values('noe_strength')
    )
    chain_b_table_data = (
        data['b']
        .pipe(albatrosy.add_noe_bins)
        .loc[
            lambda x: albatrosy.lower_triangle(x) & (x.noe_strength != 'none'),
            ['id_1', 'id_2', 'distance', 'noe_strength'],
        ]
        .sort_values('noe_strength')
    )
    delta_table_data = (
        data['delta']
        .pipe(albatrosy.add_noe_bins)
        .loc[
            lambda x: (x.noe_strength != 'none'),
            ['id_1', 'id_2', 'distance', 'noe_strength'],
        ]
        .sort_values('noe_strength')
    )

    return pn.FlexBox(
        pn.Tabs(
            ('Intra-chain NOEs', centered_row(intra_chain_noe_map)),
            ('Inter-chain NOEs', centered_row(inter_chain_noe_map)),
            ('NOE table A', centered_row(NOETable(chain_a_table_data).view)),
            ('NOE table B', centered_row(NOETable(chain_b_table_data).view)),
            ('NOE table A-B', centered_row(NOETable(delta_table_data).view)),
            align='center',
            min_width=800,
        ),
        align='center',
        justify_content='center',
        min_width=1000,
    )


def make_noe_table(df: pd.DataFrame) -> pnw.DataFrame:
    return table.data_table(
        data=df,
        titles={
            'id_1': 'Atom #1',
            'id_2': 'Atom #2',
            'distance': 'Distance (\u212B)',
            'noe_strength': 'NOE',
        },
        formatters={
            'distance': '0.0',
        },
    )


class NOETable(param.Parameterized):
    def __init__(self, data: pd.DataFrame, **params) -> None:
        super().__init__(**params)
        self._data = data
        self._search_bar = pnw.TextInput(
            placeholder='Search for atom id...',
        )

    @property
    def search_term(self) -> str:
        value = self._search_bar.value.upper()
        return value if len(value) >= 3 else None

    @pn.depends('_search_bar.value')
    def view(self):
        if self.search_term is None:
            df = self._data
        else:
            df = self._data.loc[
                lambda x: x.id_1.str.contains(self.search_term)
                | x.id_2.str.contains(self.search_term)
            ]

        return pn.Column(
            self._search_bar,
            make_noe_table(df),
        )
