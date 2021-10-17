from typing import List
from pydantic import BaseModel


class MovieBase(BaseModel):
    title: str
    summary: str
    directors: List[str]
    writers: List[str]
    actors: List[str]
    release: str
    budget: str
    rating: str
    runtime: str
    gross_world: str
    aspect_ratio: str

    @classmethod
    def from_soup(cls, souped):
        title = souped.h1.text
        summary = [i.text for i in souped.find_all("span", class_="GenresAndPlot__TextContainerBreakpointXL-cum89p-2 gCtawA")][0]
        raw_data1 = [i.text for i in souped.find_all("li", class_="ipc-metadata-list__item")]
        clean_directors = [i.replace("Director", "") for i in raw_data1 if i.startswith("Director")]
        clean_writers = [i.replace("Writer", "") for i in raw_data1 if i.startswith("Writer")]
        directors = list(set(clean_directors))
        writer = list(set(clean_writers))
        actors = [i.text for i in souped.find_all("a", class_="StyledComponents__ActorName-y9ygcu-1 eyqFnv")]
        detail_data = [i.text for i in souped.find_all("span", class_="ipc-metadata-list-item__list-content-item")]
        return cls(
            title=title,
            summary=summary,
            directors=directors,
            writers=writer,
            actors=actors,
            release=detail_data[7],
            budget=detail_data[4],
            rating=detail_data[2],
            runtime=detail_data[-2],
            gross_world=detail_data[-3],
            aspect_ratio=detail_data[-1]
        )