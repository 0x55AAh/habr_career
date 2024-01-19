import math
from typing import Iterable

from rich import box
from rich.table import Table
from rich.text import Text


UNITS = ["", "K", "M", "B", "T"]
TICK = "▇"


def to_readable(num: float, round_: int | None = None) -> str:
    """
    Return the number in a human-readable format.

    Eg:
    125000 -> 125.0K
    12550 -> 12.55K
    19561100 -> 19.561M
    """

    # Find the degree of the number like if it is in thousands
    # or millions, etc.
    index = int(num and math.log(num) / math.log(1000))

    new_num = round(num / (1000 ** index), round_)
    degree = UNITS[index]

    return f"{new_num}{degree}"


class Chart:
    def __init__(
            self,
            data,
            labels,
            categories,
            category_styles=None,
            label_styles=None,
            width=50,
            title=None,
            captions: Iterable | None = None,
    ):
        category_styles = category_styles or [None] * len(categories)
        label_styles = label_styles or [None] * len(labels)

        self.width = width

        title = Text("\n").join(x for x in [
            Text(title) if isinstance(title, str) else title,
            Text("  ").join(
                Text(f"{TICK} {category}", style=style)
                for category, style in zip(categories, category_styles)
            ),
            Text(" "),
        ] if x)

        self._table = Table(
            title=title,
            box=box.HORIZONTALS,
            pad_edge=False,
            show_edge=False,
            show_header=False,
            caption=captions and Text("\n").join([
                Text(" "),
                *[Text(c, style="bright_black") for c in captions]
            ]),
        )

        data = list(data)
        normal_data = self._normalize(data)

        row = zip(data, normal_data, labels, label_styles)
        for item, normal_item, label, label_style in row:
            if all([i is None for i in item]):
                continue
            t = Text("\n").join(
                Text(" ").join([
                    Text(f"{TICK * int(nd)}", style=label_style or style),
                    Text(f"{to_readable(d)}"),
                ]) for d, nd, style
                in zip(item, normal_item, category_styles) if d is not None
            )
            self._table.add_row(label, t)

    def _normalize(self, data) -> list[list[float]]:
        """Normalize the data and return it."""

        # We offset by the minimum if there's a negative.
        min_datum = min([
            min([s or 0 for s in sublist])
            for sublist in data
        ])

        if min_datum < 0:
            min_datum = abs(min_datum)
            data_offset = [
                [d + min_datum for d in datum]
                for datum in data
            ]
        else:
            data_offset = data

        max_datum = max([
            max([s or 0 for s in sublist])
            for sublist in data_offset
        ])

        # max_dat / width is the value for a single tick. norm_factor is the
        # inverse of this value
        # If you divide a number to the value of single tick, you will find how
        # many ticks it does contain basically.
        norm_factor = self.width / float(max_datum)
        normal_data = [
            [(v or 0) * norm_factor for v in datum]
            for datum in data_offset
        ]

        return normal_data

    def __rich__(self):
        return self._table
