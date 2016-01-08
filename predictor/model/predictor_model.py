from predictor.model.DAO import DAO
from predictor.model.DAOtoDAO import DAOtoDAO


class PredictionDAO(DAO):
    data_fields = ["uuid", "common_name", "short_description", "created_date"]
    entity = "prediction"


class PersontoPersonnamepart(DAOtoDAO):
    entity = "person_to_personnamepart"
    primDAO_PK = "person_uuid"
    secDAO_PK = "personnamepart_uuid"


class PersonDAO(DAO):
    data_fields = ["uuid", "common_name", "birth_date"]
    entity = "person"
    join_objects = {"PersontoPersonnamepart": PersontoPersonnamepart}

    def __init__(self, uuid, common_name=None, birth_date=None):
        super(PersonDAO, self).__init__(uuid)
        setattr(self, "common_name", common_name)
        setattr(self, "birth_date", birth_date)

    def add_personnamepart(self, personnamepart):
        self.PersontoPersonnamepart.add(PersontoPersonnamepart(self.uuid, personnamepart.uuid))


class PersonnamepartDAO(DAO):
    data_fields = ["uuid", "namepart_role", "namepart_value"]


class PublicationtoPublisher(DAOtoDAO):
    entity = "publication_to_publisher"
    primDAO_PK = "publication_uuid"
    secDAO_PK = "publisher_uuid"


class PublicationtoPublicationtext(DAOtoDAO):
    entity = "publication_to_publicationtext"
    primDAO_PK = "publication_uuid"
    secDAO_PK = "publicationtext_uuid"


class PublicationDAO(DAO):
    data_fields = ["uuid", "date", "title", "url"]
    entity = "publication"
    join_objects = {"PublicationtoPublisher": PublicationtoPublisher,
                    "PublicationtoPublicationtext": PublicationtoPublicationtext}

    def __init__(self, uuid=None, date=None, title=None, url=None):
        super(PublicationDAO, self).__init__(uuid)
        setattr(self, "date", date)
        setattr(self, "title", title)
        setattr(self, "url", url)

    def add_publicationtext(self, publicationtext):
        self.PublicationtoPublicationtext.add(PublicationtoPublicationtext(self.uuid, publicationtext.uuid))

    def get_publicationtext(self):
        publicationtext = None
        if len(self.PublicationtoPublicationtext)>0:
            publication_to_publicationtext = next(iter(self.PublicationtoPublicationtext))
            publicationtext_uuid = publication_to_publicationtext.secDAO_uuid
            publicationtext = PublicationtextDAO(publicationtext_uuid)
        return publicationtext

    def add_publisher(self, publisher):
        self.PublicationtoPublisher.add(PublicationtoPublisher(self.uuid, publisher.uuid))

    def get_publisher(self):
        publisher = None
        if len(self.PublicationtoPublisher)>0:
            publication_to_publisher = next(iter(self.PublicationtoPublisher))
            publisher_uuid = publication_to_publisher.secDAO_uuid
            publisher = PublisherDAO(publisher_uuid)
        return publisher


class PublisherDAO(DAO):
    data_fields = ["uuid", "commonname", "url"]
    entity = "publisher"

    def __init__(self, uuid=None, commonname=None, url=None):
        super(PublisherDAO, self).__init__(uuid)
        setattr(self, "commonname", commonname)
        setattr(self, "url", url)


class PublicationtextDAO(DAO):
    data_fields = ["uuid", "text"]
    entity = "publicationtext"


class PredictiontoPublication(DAOtoDAO):
    entity = "prediction_to_publication"
    primDAO_PK = "publication_uuid"
    secDAO_PK = "prediction_uuid"


class PredictionDAO(DAO):
    data_fields = ["uuid", "commonname", "short_description", "created_date"]
    entity = "prediction"
    join_objects = {"PredictiontoPublication": PredictiontoPublication}

    def __init__(self, uuid=None, commonname=None, short_description=None, created_date=None):
        super(PredictionDAO, self).__init__(uuid)
        setattr(self, "commonname", commonname)
        setattr(self, "short_description", short_description)
        setattr(self, "created_date", created_date)

    def add_publication(self, publication):
        self.PredictiontoPublication.add(publication)