from os import name
from typing import Dict, List
from pydantic import BaseModel


class AlbumBase(BaseModel):
    title: str
    artist: str
    track_list: List[Dict[str,str]]
    genre: str
    descriptors: List[str]
    rating: str

    @classmethod
    def from_soup(cls, souped):
        title = [i.text for i in souped.find_all("div", class_="album_title")][0]
        title = title.split("\n")[0].strip()
        artist = [i.text for i in souped.find_all("a", class_="artist")][0]
        genre = [i.text for i in souped.find_all("a", class_="genre")][0]
        descriptor_str = [i.text for i in souped.find_all("span", class_="release_pri_descriptors")][0]
        descriptors = [i.strip() for i in descriptor_str.split(",")]
        tracks  = souped.find("ul", class_="tracks tracklisting")
        track_list = []
        for i in tracks.find_all("li"):
            name = i.find("span", class_="rendered_text")
            duration = i.find("span", class_="tracklist_duration")
            if name and duration:
                track_list.append(
                    {"title": f"{name.text}", "duration": f"{duration.text}"}
                )
        avg_rating = [i for i in souped.find_all("span", class_="avg_rating")][0].text.strip()
        max_rating = [i for i in souped.find_all("span", class_="max_rating")][0].span.text.strip()
        num_ratings = [i for i in souped.find_all("span", class_="num_ratings")][0].b.span.text.strip()
        return cls(
            title=title,
            artist=artist,
            track_list=track_list,
            genre=genre,
            descriptors=descriptors,
            rating=f"{avg_rating}/{max_rating} from {num_ratings} ratings"
        )