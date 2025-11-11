"""
Request Models for Pattern Engine API

This module defines Pydantic models for API request validation and data transfer.
These models enforce type safety and data validation for incoming pattern generation requests.
"""

from pydantic import BaseModel, Field


class Gauge(BaseModel):
    """
    Gauge specification for crochet patterns.

    Gauge determines the relationship between physical dimensions and stitch/row counts.
    Typically measured by creating a swatch and counting stitches and rows over a 10cm square.

    Attributes:
        sts_per_10cm: Number of stitches per 10 centimeters (horizontal)
        rows_per_10cm: Number of rows per 10 centimeters (vertical)

    Examples:
        >>> gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)
        >>> gauge.sts_per_10cm
        14.0

        >>> # Fine gauge with DK yarn
        >>> gauge_fine = Gauge(sts_per_10cm=18, rows_per_10cm=20)

        >>> # Coarse gauge with bulky yarn
        >>> gauge_coarse = Gauge(sts_per_10cm=10, rows_per_10cm=12)

    Notes:
        - Standard worsted weight yarn typically yields 14-16 sts/10cm
        - DK weight yarn typically yields 16-20 sts/10cm
        - Bulky yarn typically yields 10-12 sts/10cm
        - Gauge must be measured accurately for proper pattern sizing
    """

    sts_per_10cm: float = Field(
        ...,
        gt=0,
        description="Stitches per 10 centimeters (horizontal gauge)",
        examples=[14.0, 18.0, 10.0]
    )
    rows_per_10cm: float = Field(
        ...,
        gt=0,
        description="Rows per 10 centimeters (vertical gauge)",
        examples=[16.0, 20.0, 12.0]
    )
