from predictor.model.DAO import DAO, VDAO
from predictor.model.DAOtoDAO import DAOtoDAO


class PersonnamepartDAO(DAO):
    entity = "personnamepart"
    data_fields = ["uuid", "namepart_role", "namepart_value"]


class PersonnametoPersonnamepart(DAOtoDAO):
    entity = "personname_to_personnamepart"
    primDAO_PK = "personname_uuid"
    secDAO_PK = "personnamepart_uuid"


class PersonnameDAO(DAO):
    entity = "personname"
    data_fields = ["uuid", "personname_role"]
    join_objects = {"PersonnametoPersonnamepart": PersonnametoPersonnamepart}

    def add_personnamepart(self, personnamepart):
        self.PersonnametoPersonnamepart.add(PersonnametoPersonnamepart(self.uuid, personnamepart.uuid))


class PersontoPersonname(DAOtoDAO):
    entity = "person_to_personname"
    primDAO_PK = "person_uuid"
    secDAO_PK = "personname_uuid"


class PersonDAO(DAO):
    data_fields = ["uuid", "commonname", "birth_date"]
    entity = "person"
    join_objects = {"PersontoPersonname": PersontoPersonname}
    sortkey = "commonname"

    def add_personname(self, personname):
        self.PersontoPersonname.add(PersontoPersonname(self.uuid, personname.uuid))


class OrganisationtoCountry(DAOtoDAO):
    entity = "organisation_to_country"
    primDAO_PK = "organisation_uuid"
    secDAO_PK = "country_uuid"


class OrganisationDAO(DAO):
    data_fields = ["uuid", "commonname"]
    entity = "organisation"
    sortkey = "commonname"
    join_objects = {"OrganisationtoCountry": OrganisationtoCountry}

    def add_country(self, country):
        self.OrganisationtoCountry.add(OrganisationtoCountry(self.uuid, country.uuid))

    def get_country(self):
        return self.get_joined_dao("OrganisationtoCountry", CountryDAO)


class PublicationtoPublisher(DAOtoDAO):
    entity = "publication_to_publisher"
    primDAO_PK = "publication_uuid"
    secDAO_PK = "publisher_uuid"


class PublicationtoPublicationtext(DAOtoDAO):
    entity = "publication_to_publicationtext"
    primDAO_PK = "publication_uuid"
    secDAO_PK = "publicationtext_uuid"


class PublicationtoBinaryfile(DAOtoDAO):
    entity = "publication_to_binaryfile"
    primDAO_PK = "publication_uuid"
    secDAO_PK = "binaryfile_uuid"


class PublicationtoLanguage(DAOtoDAO):
    entity = "publication_to_language"
    primDAO_PK = "publication_uuid"
    secDAO_PK = "language_uuid"


class BinaryfileDAO(DAO):
    data_fields = ["uuid", "filecontent", "filetype", "filename"]
    entity = "binaryfile"
    binary_fields = ["filecontent"]


class PublicationDAO(DAO):
    data_fields = ["uuid", "date", "title", "url"]
    entity = "publication"
    join_objects = {"PublicationtoPublisher": PublicationtoPublisher,
                    "PublicationtoPublicationtext": PublicationtoPublicationtext,
                    "PublicationtoBinaryfile": PublicationtoBinaryfile,
                    "PublicationtoLanguage": PublicationtoLanguage}

    sortkey = "date"

    def add_publicationtext(self, publicationtext):
        self.PublicationtoPublicationtext.add(PublicationtoPublicationtext(self.uuid, publicationtext.uuid))

    def get_publicationtext(self):
        return self.get_joined_dao("PublicationtoPublicationtext", PublicationtextDAO)

    def add_publisher(self, publisher):
        self.PublicationtoPublisher.add(PublicationtoPublisher(self.uuid, publisher.uuid))

    def get_publisher(self):
        return self.get_joined_dao("PublicationtoPublisher", PublisherDAO)

    def add_binaryfile(self, binaryfile):
        self.PublicationtoBinaryfile.add(PublicationtoBinaryfile(self.uuid, binaryfile.uuid))

    def get_binaryfile(self):
        return self.get_joined_dao("PublicationtoBinaryfile", BinaryfileDAO)

    def add_language(self, language):
        self.PublicationtoLanguage.add(PublicationtoLanguage(self.uuid, language.uuid))

    def get_language(self):
        return self.get_joined_dao("PublicationtoLanguage", LanguageDAO)


class PublishertoCountry(DAOtoDAO):
    entity = "publisher_to_country"
    primDAO_PK = "publisher_uuid"
    secDAO_PK = "country_uuid"


class PublisherDAO(DAO):
    data_fields = ["uuid", "commonname", "url"]
    entity = "publisher"
    join_objects = {"PublishertoCountry":PublishertoCountry}

    def add_country(self, country):
        self.PublishertoCountry.add(PublishertoCountry(self.uuid, country.uuid))


class PublicationtextDAO(DAO):
    data_fields = ["uuid", "text"]
    entity = "publicationtext"


class PublicationPublisherV(VDAO):
    data_fields = ["uuid", "publication_title", "publication_date", "publisher_commonname"]
    entity = "public.\"publication_publisher_V\""


class PredictiontoPublication(DAOtoDAO):
    entity = "prediction_to_publication"
    primDAO_PK = "prediction_uuid"
    secDAO_PK = "publication_uuid"


class PredictiontoTextmodel(DAOtoDAO):
    entity = "prediction_to_textmodel"
    primDAO_PK = "prediction_uuid"
    secDAO_PK = "textmodel_uuid"


class PredictiontoTmstatement(DAOtoDAO):
    entity = "prediction_to_tmstatement"
    primDAO_PK = "prediction_uuid"
    secDAO_PK = "tmstatement_uuid"


class OriginatortoPerson(DAOtoDAO):
    entity = "originator_to_person"
    primDAO_PK = "originator_uuid"
    secDAO_PK = "person_uuid"


class OriginatortoOrganisation(DAOtoDAO):
    entity = "originator_to_organisation"
    primDAO_PK = "originator_uuid"
    secDAO_PK = "organisation_uuid"


class OriginatorDAO(DAO):
    data_fields = ["uuid", "short_description"]
    entity = "originator"
    join_objects = {"OriginatortoPerson": OriginatortoPerson,
                    "OriginatortoOrganisation": OriginatortoOrganisation}

    def add_person(self, person):
        self.OriginatortoPerson.add(OriginatortoPerson(self.uuid, person.uuid))

    def remove_person(self, person):
        self.OriginatortoPerson.remove(OriginatortoPerson(self.uuid, person.uuid))

    def add_organisation(self, organisation):
        self.OriginatortoOrganisation.add(OriginatortoOrganisation(self.uuid, organisation.uuid))

    def remove_originator(self, organisation):
        self.OriginatortoOrganisation.remove(OriginatortoOrganisation(self.uuid, organisation.uuid))


class PredictiontoOriginator(DAOtoDAO):
    entity = "prediction_to_originator"
    primDAO_PK = "prediction_uuid"
    secDAO_PK = "originator_uuid"


class PredictionDAO(DAO):
    data_fields = ["uuid", "commonname", "short_description", "created_date"]
    entity = "prediction"
    join_objects = {"PredictiontoPublication": PredictiontoPublication,
                    "PredictiontoTmstatement": PredictiontoTmstatement,
                    "PredictiontoOriginator": PredictiontoOriginator }
    sortkey = "commonname"

    def add_publication(self, publication):
        self.PredictiontoPublication.add(PredictiontoPublication(self.uuid, publication.uuid))

    def remove_publication(self, publication):
        ptop = PredictiontoPublication(self.uuid, publication.uuid)
        if ptop in self.PredictiontoPublication:
            self.PredictiontoPublication.remove(ptop)
        else:
            print("publication %s is not dedicated to prediction %s" %  (publication.uuid, self.uuid))

    def add_tmstatement(self, tmstatement):
        self.PredictiontoTmstatement.add(PredictiontoTmstatement(self.uuid, tmstatement.uuid))

    def remove_tmstatement(self, tmstatement):
        self.PredictiontoTmstatement.remove(PredictiontoTmstatement(self.uuid, tmstatement.uuid))

    def add_originator(self, originator):
        self.PredictiontoOriginator.add(PredictiontoOriginator(self.uuid, originator.uuid))

    def remove_originator(self, originator):
        self.PredictiontoOriginator.remove(PredictiontoOriginator(self.uuid, originator.uuid))


class PredictionPublisherV(VDAO):
    data_fields = ["uuid", "commonname", "title", "date", "url", "publication_uuid"]
    entity = "public.\"prediction_publication_V\""


class PredictionOriginatorV(VDAO):
    data_fields = ["uuid", "originator_uuid", "concrete_uuid", "common_name", "is_person", "is_organisation"]
    entity = "public.\"prediction_originator_V\""


class TextmodelToTmstatement(DAOtoDAO):
    entity = "textmodel_to_tmstatement"
    primDAO_PK = "textmodel_uuid"
    secDAO_PK = "tmstatement_uuid"


class TextmodelDAO(DAO):
    data_fields = ["uuid", "date", "short_description"]
    entity = "textmodel"
    join_objects = {"TextmodelToTmstatement": TextmodelToTmstatement}

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


class PredictionStatementV(VDAO):
    data_fields = ["uuid", "tmstatement_uuid", "tmbegin", "tmend", "text"]
    entity = "public.\"prediction_tmstatement_V\""


class PredictionTextmodelV(VDAO):
    data_fields = ["uuid", "date", "short_description", "textmodel_uuid"]
    entity = "public.\"prediction_textmodel_V\""


class CountryDAO(DAO):
    data_fields = ["uuid", "commonname"]
    entity = "country"
    sortkey = "commonname"


class PredictionPublicationPublisherV(VDAO):
    data_fields = ["uuid", "commonname", "created_date", "publication_title", "publication_date", "publisher_commonname"]
    entity = "public.\"prediction_publication_publisher_V\""


class LanguageDAO(DAO):
    data_fields = ["uuid", "commonname"]
    entity = "language"
    sortkey = "commonname"