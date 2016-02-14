from predictor.model.DAO import DAO, VDAO
from predictor.model.DAOtoDAO import DAOtoDAO


class PersontoPersonname(DAOtoDAO):
    entity = "person_to_personname"
    primDAO_PK = "person_uuid"
    secDAO_PK = "personname_uuid"


class PersonDAO(DAO):
    data_fields = ["uuid", "common_name", "birth_date"]
    entity = "person"
    join_objects = {"PersontoPersonname": PersontoPersonname}

    def __init__(self, uuid, common_name=None, birth_date=None):
        super(PersonDAO, self).__init__(uuid)
        setattr(self, "common_name", common_name)
        setattr(self, "birth_date", birth_date)

    def add_personnamepart(self, personname):
        self.PersontoPersonname.add(PersontoPersonname(self.uuid, personname.uuid))


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

    #def __init__(self, uuid=None, row=None):
    #    super(PublicationDAO, self).__init__(uuid, row)

    def add_publicationtext(self, publicationtext):
        self.PublicationtoPublicationtext.add(PublicationtoPublicationtext(self.uuid, publicationtext.uuid))

    def get_publicationtext(self):
        publicationtext = None
        if len(self.PublicationtoPublicationtext) > 0:
            publication_to_publicationtext = list(self.PublicationtoPublicationtext)[0]
            publicationtext_uuid = publication_to_publicationtext.secDAO_uuid
            publicationtext = PublicationtextDAO(publicationtext_uuid)
            publicationtext.load()
        return publicationtext

    def add_publisher(self, publisher):
        self.PublicationtoPublisher.add(PublicationtoPublisher(self.uuid, publisher.uuid))

    def get_publisher(self):
        publisher = None
        if len(self.PublicationtoPublisher) > 0:
            publication_to_publisher = list(self.PublicationtoPublisher)[0]
            publisher_uuid = publication_to_publisher.secDAO_uuid
            publisher = PublisherDAO(publisher_uuid)
            publisher.load()
        return publisher


class PublisherDAO(DAO):
    data_fields = ["uuid", "commonname", "url"]
    entity = "publisher"


class PublicationtextDAO(DAO):
    data_fields = ["uuid", "text"]
    entity = "publicationtext"


class PredictiontoPublication(DAOtoDAO):
    entity = "prediction_to_publication"
    primDAO_PK = "prediction_uuid"
    secDAO_PK = "publication_uuid"


class PredictiontoTextmodel(DAOtoDAO):
    entity = "prediction_to_textmodel"
    primDAO_PK = "prediction_uuid"
    secDAO_PK = "textmodel_uuid"


class PredictionDAO(DAO):
    data_fields = ["uuid", "commonname", "short_description", "created_date"]
    entity = "prediction"
    join_objects = {"PredictiontoPublication": PredictiontoPublication,
                    "PredictiontoTextmodel": PredictiontoTextmodel}

    def add_publication(self, publication):
        self.PredictiontoPublication.add(PredictiontoPublication(self.uuid, publication.uuid))

    def remove_publication(self, publication):
        ptop = PredictiontoPublication(self.uuid, publication.uuid)
        if ptop in self.PredictiontoPublication:
            self.PredictiontoPublication.remove(ptop)
        else:
            print("publication %s is not dedicated to prediction %s", publication.uuid, self.uuid)

    def add_textmodel(self, textmodel):
        self.PredictiontoTextmodel.add(PredictiontoTextmodel(self.uuid, textmodel.uuid))

    def remove_textmodel(self, textmodel):
        self.PredictiontoTextmodel.remove(PredictiontoTextmodel(self.uuid, textmodel.uuid))


class PredictionPublisherV(VDAO):
    data_fields = ["uuid", "commonname", "title", "date", "url", "publication_uuid"]
    entity = "public.\"prediction_publication_V\""


class TextmodelToTmstatement(DAOtoDAO):
    entity = "textmodel_to_tmstatement"
    primDAO_PK = "textmodel_uuid"
    secDAO_PK = "tmstatement_uuid"


class TextmodelDAO(DAO):
    data_fields = ["uuid", "date", "short_description"]
    entity = "textmodel"
    join_objects = {"TextmodelToTmstatement": TextmodelToTmstatement}

    def __init__(self, uuid=None, date=None, short_description=None):
        super(TextmodelDAO, self).__init__(uuid)
        setattr(self, "date", date)
        setattr(self, "short_description", short_description)

    def add_tmstatement(self, tmstatement):
        self.TextmodelToTmstatement.add(TextmodelToTmstatement(self.uuid, tmstatement.uuid))

    def remove_tmstatement(self, tmstatement):
        self.TextmodelToTmstatement.remove(TextmodelToTmstatement(self.uuid, tmstatement.uuid))


class TmstatementDAO(DAO):
    data_fields = ["uuid", "text", "tmbegin", "tmend"]
    entity = "tmstatement"

    def __init__(self, uuid=None, text=None, tmbegin=None, tmend=None):
        super(TmstatementDAO, self).__init__(uuid)
        setattr(self, "text", text)
        setattr(self, "tmbegin", tmbegin)
        setattr(self, "tmend", tmend)


class OrganisationDAO(DAO):
    data_fields = ["uuid", "commonname"]
    entity = "organisation"

    def __init__(self, uuid=None, commonname=None):
        super(OrganisationDAO, self).__init__(uuid)
        setattr(self, "commonname", commonname)


class PredictionTextmodelV(VDAO):
    data_fields = ["uuid", "date", "short_description", "textmodel_uuid"]
    entity = "public.\"prediction_textmodel_V\""
