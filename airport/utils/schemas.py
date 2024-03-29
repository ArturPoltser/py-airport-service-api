from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema


def route_list_schema():
    return extend_schema(
        parameters=[
            OpenApiParameter(
                "source",
                type=OpenApiTypes.STR,
                description="Filtering by source (ex. ?source=Rome)"
            ),
            OpenApiParameter(
                "destination",
                type=OpenApiTypes.STR,
                description="Filtering by destination (ex. ?destination=Paris)"
            )
        ]
    )


def flight_list_schema():
    return extend_schema(
        parameters=[
            OpenApiParameter(
                "from",
                type=OpenApiTypes.STR,
                description="Filtering by source (ex. ?from=Rome)"
            ),
            OpenApiParameter(
                "to",
                type=OpenApiTypes.STR,
                description="Filtering by destination (ex. ?to=Paris)"
            ),
            OpenApiParameter(
                "departure_date",
                type=OpenApiTypes.DATE,
                description="Filtering by departure date "
                            "(ex. ?departure_date=2024-03-25)"
            ),
            OpenApiParameter(
                "arrival_date",
                type=OpenApiTypes.DATE,
                description="Filtering by arrival date "
                            "(ex. ?arrival_date=2024-03-26)"
            )
        ]
    )
