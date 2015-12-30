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

    def __init__(self, uuid, common_name, birth_date):
        super(PersonDAO, self).__init__(uuid)
        setattr(self, "common_name", common_name)
        setattr(self, "birth_date", birth_date)

    def addPersonnamepart(self, personnamepart):
        self.join_objects_list["PersontoPersonnamepart"].add(PersontoPersonnamepart(self.uuid, personnamepart.uuid))


class PersonnamepartDAO(DAO):
    data_fields = ["uuid", "namepart_role", "namepart_value"]


class PublicationDAO(DAO):
    data_fields = ["uuid", "date", "title", "url"]
    entity = "publication"
