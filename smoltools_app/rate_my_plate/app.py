from io import BytesIO
from pathlib import Path

import altair as alt
import panel as pn
import panel.widgets as pnw

from utils import colors, config
from rate_my_plate.widgets.excel_loader import (
    ExcelLoader,
    NoFileSelected,
    BadFileFormat,
)
from smoltools.rate_my_plate import read_data_from_bytes, rate_plate, convert_to_wide
from smoltools.rate_my_plate import consumption_curve, kinetics_curves
from rate_my_plate.widgets.excel_download import excel_file_download


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

        self._lower_percent = pnw.FloatInput(
            name='lower percent cutoff', value=-0.05, step=0.05, start=-0.2, end=0.5
        )
        self._upper_percent = pnw.FloatInput(
            name='upper percent cutoff', value=0.8, step=0.05, start=0.5, end=1
        )
        self._redo_filter_button = pnw.Button(name='Set new thresholds')
        self._redo_filter_button.on_click(self.preview_data)

        self._continue_button = pnw.Button(name='Continue', button_type='success')
        self._continue_button.on_click(self.analyze_data)

        self.main.append(
            pn.FlexBox(
                pn.Row(
                    self.excel_loader,
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
        except KeyError:
            self.excel_loader.show_error(BadFileFormat())
        else:
            self.excel_loader.upload_success()
            self.preview_data()

    def plot_consumption_curves(self) -> alt.Chart():
        return consumption_curve(
            self.data,
            lower_percent=self._lower_percent.value,
            upper_percent=self._upper_percent.value,
        )

    def preview_data(self, event=None) -> None:
        plots = self.plot_consumption_curves()
        self.main[0].objects = [
            pn.FlexBox(
                pn.Column(
                    pn.pane.Vega(plots),
                    pn.Row(
                        self._lower_percent,
                        self._upper_percent,
                        align='center',
                    ),
                    self._redo_filter_button,
                    pn.layout.Divider(),
                    self._continue_button,
                ),
                justify_content='center',
            )
        ]

    def analyze_data(self, event=None) -> None:
        self.analyzed_data = rate_plate(
            self.data,
            lower_percent=self._lower_percent.value,
            upper_percent=self._upper_percent.value,
        )
        filename = Path(self.excel_loader.input_filename).stem
        self.main[0].objects = [
            pn.FlexBox(
                pn.Column(
                    pn.pane.Vega(kinetics_curves(self.analyzed_data)),
                    excel_file_download(
                        self._download_callback,
                        f'{filename}-rated.xlsx',
                    ),
                ),
                justify_content='center',
            ),
        ]

    def _download_callback(self) -> BytesIO:
        bytes_io = BytesIO()
        self.analyzed_data.pipe(convert_to_wide).to_excel(bytes_io, index=False)
        bytes_io.seek(0)
        return bytes_io


def app() -> pn.pane:
    # configure external libraries
    config.configure_panel_extensions()
    config.configure_plotting_libraries()

    return Dashboard().servable()
