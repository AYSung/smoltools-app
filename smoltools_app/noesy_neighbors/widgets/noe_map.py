import pandas as pd
import panel as pn
import panel.widgets as pnw
import param

from smoltools import noesy_neighbors

from common.widgets import table
from common.widgets.containers import centered_row


def make_monomer_noe_widget(data: dict[str, pd.DataFrame]) -> pn.Card:
    combined_distances = noesy_neighbors.splice_conformation_tables(
        data['a'],
        data['b'],
        chain_a_id=data['chain_a_id'],
        chain_b_id=data['chain_b_id'],
    )

    noe_map_a = pn.pane.Vega(noesy_neighbors.plots.noe_map(data['a']))
    noe_map_b = pn.pane.Vega(noesy_neighbors.plots.noe_map(data['b']))
    combined_noe_map = pn.pane.Vega(
        noesy_neighbors.plots.spliced_noe_map(combined_distances)
    )

    chain_a_table_data = filter_table_data(data['a'], symmetric=True)
    chain_b_table_data = filter_table_data(data['b'], symmetric=True)

    return pn.Card(
        pn.Tabs(
            ('Combined', centered_row(combined_noe_map)),
            ('Conformation A', centered_row(noe_map_a)),
            ('Conformation B', centered_row(noe_map_b)),
            ('NOE table A', centered_row(NOETable(chain_a_table_data).view)),
            ('NOE table B', centered_row(NOETable(chain_b_table_data).view)),
        ),
        title='NOE Maps',
        collapsible=False,
        width=900,
    )


def make_dimer_noe_widget(data: dict[str, pd.DataFrame]) -> pn.Card:
    combined_distances = noesy_neighbors.splice_conformation_tables(
        data['a'],
        data['b'],
        chain_a_id=data['chain_a_id'],
        chain_b_id=data['chain_b_id'],
    )
    intra_chain_noe_map = pn.pane.Vega(
        noesy_neighbors.plots.spliced_noe_map(combined_distances)
    )
    chain_a_noe_map = pn.pane.Vega(noesy_neighbors.plots.noe_map(data['a']))
    chain_b_noe_map = pn.pane.Vega(noesy_neighbors.plots.noe_map(data['b']))

    inter_chain_noe_map = pn.pane.Vega(
        noesy_neighbors.plots.interchain_noe_map(
            data['delta'],
            x_title=data['chain_a_id'],
            y_title=data['chain_b_id'],
        )
    )

    chain_a_table_data = filter_table_data(data['a'], symmetric=True)
    chain_b_table_data = filter_table_data(data['b'], symmetric=True)
    delta_table_data = filter_table_data(data['delta'], symmetric=False)

    return pn.FlexBox(
        pn.Tabs(
            ('Intra-chain NOEs', centered_row(intra_chain_noe_map)),
            ('Chain A NOEs', centered_row(chain_a_noe_map)),
            ('Chain B NOEs', centered_row(chain_b_noe_map)),
            ('Inter-chain NOEs', centered_row(inter_chain_noe_map)),
            ('NOE table A', centered_row(NOETable(chain_a_table_data).view)),
            ('NOE table B', centered_row(NOETable(chain_b_table_data).view)),
            ('NOE table A-B', centered_row(NOETable(delta_table_data).view)),
            align='center',
            width=800,
        ),
        justify_content='center',
        min_width=900,
    )


def filter_table_data(df: pd.DataFrame, symmetric: bool) -> pd.DataFrame:
    data = (
        df.pipe(noesy_neighbors.add_noe_bins)
        .loc[
            lambda x: x.noe_strength != 'none',
            ['id_1', 'id_2', 'distance', 'noe_strength'],
        ]
        .sort_values('noe_strength')
    )
    if symmetric:
        return data.loc[lambda x: noesy_neighbors.lower_triangle(x)]
    else:
        return data


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
