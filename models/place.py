#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
import models
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id", String(60),
                             ForeignKey("places.id"),
                             primary_key=True,
                             nullable=False),
                      Column("amenity_id", String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """

        __tablename__ = "places"

        city_id = Column(String(60), ForeignKey("cities.id",
                         ondelete='CASCADE'), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id",
                         ondelete='CASCADE'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float)
        longitude = Column(Float)
        amenities = []

        if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship("Review", cascade='all, delete, delete-orphan',
                               backref="place")

        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False,
                                 back_populates="place_amenities")
    else:

        @property
        def reviews(self):
            """ Returns list of reviews.id """
            var = models.storage.all()
            lista = []
            result = []
            for key in var:
                review = key.replace('.', ' ')
                review = shlex.split(review)
                if (review[0] == 'Review'):
                    lista.append(var[key])
            for elem in lista:
                if (elem.place_id == self.id):
                    result.append(elem)
            return (result)

        @property
        def amenities(self):
            """Returns the list of Amenity instances based on the attribute
            amenity_ids that contains all Amenity.id linked to the Place.
            """
            return self.amenity_ids

        @amenities.setter
        def amenities(self, obj):
            """Handles append method for adding an Amenity.id to the attribute
            amenity_ids. This method should accept only Amenity object,
            otherwise, do nothing.
            """
            if type(obj) is Amenity and obj.id not in self.amenity_ids:
            self.amenity_ids.append(obj.id)
