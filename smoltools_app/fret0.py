import panel as pn
import pandas as pd

# from templates import template
from utils import colors, config
from widgets import r0_finder, distance, e_fret, pdb_loader
import fret0


class Dashboard(pn.template.BootstrapTemplate):
    def __init__(self):
        super().__init__(
            title='fret0',
            header_background=colors.DARK_GREY,
        )
        self.data = pd.DataFrame()
        self.analyses = pn.Column()

        self.main.append(
            pn.Row(
                self.analyses,
                r0_finder.make_widget(),
            )
        )
        self.sidebar.append(
            pdb_loader.make_widget(self),
        )

    def load_analyses(self) -> None:
        self.analyses.extend(
            [
                distance.make_distance_widget(self.data),
                e_fret.make_e_fret_widget(self.data),
            ]
        )

    def load_pdb_files(self, structure_a, chain_a, structure_b, chain_b) -> None:
        self.data = fret0.pairwise_distances(structure_a, chain_a, structure_b, chain_b)

        self.load_analyses()


def app() -> pn.pane:
    # configure external libraries
    config.configure_panel_extensions()
    config.configure_plotting_libraries()

    # load datasets

    # mitocarta = data.load_mitocarta_gene_set()

    # make widgets

    # compose widgets
    # outlier_dash = pn.Column(
    #     width_policy='max',
    # )

    # TODO:
    # create dashboard template and populate with widgets
    # dashboard = template.smoltools_template(title='Outlier Analysis')
    # dashboard.main.append(outlier_dash)

    # return dashboard.servable()

    return Dashboard().servable()


app()

# TODO: SASA import
# TODO: altair heatmaps
