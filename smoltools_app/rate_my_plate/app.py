import panel as pn

from utils import colors, config
from rate_my_plate.widgets.excel_loader import ExcelLoader, NoFileSelected
from smoltools.rate_my_plate import read_data_from_bytes, rate_plate
from smoltools.rate_my_plate import kinetics_curves


class Dashboard(pn.template.BootstrapTemplate):
    def __init__(self, **params):
        super().__init__(
            site='SmolTools',
            title='Rate My Plate',
            header_background=colors.PURPLE,
            **params,
            # TODO: logo and favicon
        )
        self.excel_loader = ExcelLoader()
        self.excel_loader.bind_button(self.load_excel_file)

        self.main.append(
            pn.FlexBox(
                pn.Row(
                    self.excel_loader,
                    # pn.Spacer(width=20),
                    # pn.Column('**OR**', align='center'),
                    # pn.Spacer(width=20),
                    # self.pdb_loader_2,
                    align='center',
                ),
                justify_content='center',
            )
        )

    def load_excel_file(self, event=None) -> None:
        try:
            byte_file = self.excel_loader.input_value
            self.data = read_data_from_bytes(byte_file)
        except (ValueError, TypeError, AttributeError):
            self.excel_loader.show_error(NoFileSelected())
        else:
            self.excel_loader.upload_success()
            self.analyze_data()

    def analyze_data(self) -> None:
        self.analyzed_data = rate_plate(self.data)
        self.main[0].objects = [pn.Card(kinetics_curves(self.analyzed_data))]

    # def _upload_files(self, pdb_loader: PDBLoader, analysis_function: Callable):
    #     try:
    #         chain_a = pdb_loader.chain_a
    #         chain_b = pdb_loader.chain_b
    #         mode = pdb_loader.options_value

    #         analyses = analysis_function(chain_a, chain_b, mode)
    #     except (NoFileSelected, ChainNotFound, NoResiduesFound, NoAtomsFound) as e:
    #         pdb_loader.show_error(e)
    #     else:
    #         pdb_loader.upload_success()
    #         self.show_analyses(analyses)

    # def upload_conformation_files(self, event=None) -> Callable:
    #     self._upload_files(
    #         pdb_loader=self.pdb_loader_1,
    #         analysis_function=run_conformation_analysis,
    #     )

    # def upload_interchain_files(self, event=None) -> Callable:
    #     self._upload_files(
    #         pdb_loader=self.pdb_loader_2,
    #         analysis_function=run_interchain_analysis,
    #     )

    # def show_analyses(self, analyses: list[pn.Card]) -> None:
    #     self.main[0].objects = analyses


def app() -> pn.pane:
    # configure external libraries
    config.configure_panel_extensions()
    config.configure_plotting_libraries()

    return Dashboard().servable()
