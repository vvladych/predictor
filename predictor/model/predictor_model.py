from predictor.model.DAO import DAO, DAOList
from predictor.model.DAOtoDAO import DAOtoDAO, DAOtoDAOList


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
    join_objects_list = dict(PersontoPersonnamepart=DAOtoDAOList(PersontoPersonnamepart))

    def __init__(self, uuid, common_name=None, birth_date=None):
        super(PersonDAO, self).__init__(uuid)
        setattr(self, "common_name", common_name)
        setattr(self, "birth_date", birth_date)

    def add_personnamepart(self, personnamepart):
        self.join_objects_list["PersontoPersonnamepart"].add(PersontoPersonnamepart(self.uuid, personnamepart.uuid))


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
    join_objects_list = dict(PublicationtoPublisher=DAOtoDAOList(PublicationtoPublisher),
                             PublicationtoPublicationtext=DAOtoDAOList(PublicationtoPublicationtext))

    def __init__(self, uuid=None, date=None, title=None, url=None):
        super(PublicationDAO, self).__init__(uuid)
        setattr(self, "date", date)
        setattr(self, "title", title)
        setattr(self, "url", url)

    def add_publicationtext(self, publicationtext):
        self.join_objects_list["PublicationtoPublicationtext"].add(PublicationtoPublicationtext(self.uuid, publicationtext.uuid))

    def get_publicationtext(self):
        publicationtext = None
        if len(self.join_objects_list["PublicationtoPublicationtext"])>0:
            publication_to_publicationtext = next(iter(self.join_objects_list["PublicationtoPublicationtext"]))
            publicationtext_uuid = publication_to_publicationtext.secDAO_uuid
            publicationtext = PublicationtextDAO(publicationtext_uuid)
        return publicationtext


class PublisherDAO(DAO):
    data_fields = ["uuid", "commonname", "url"]
    entity = "publisher"


class PublicationtextDAO(DAO):
    data_fields = ["uuid", "text"]
    entity = "publicationtext"
