import panel as pn
import altair as alt


def configure_panel_extensions():
    css = '''
        .sidenav {
        background: #f0f0f0;
        }
        '''

    pn.extension('vega', raw_css=[css])


def configure_plotting_libraries():
    alt.data_transformers.enable('default')
    alt.data_transformers.disable_max_rows()
