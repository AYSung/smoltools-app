from bokeh.models.widgets.tables import NumberFormatter
import pandas as pd
import panel.widgets as pnw


def data_table(
    data: pd.DataFrame, titles=dict[str, str], formatters=dict[str, NumberFormatter]
) -> pnw.DataFrame:
    formatters = {column: NumberFormatter(format=format) for column, format in formatters.items()}
    
    return pnw.DataFrame(
        value=data,
        titles=titles,
        formatters=formatters,
        show_index=False,
        height=500,
        row_height=30,
        disabled=True,
    )

