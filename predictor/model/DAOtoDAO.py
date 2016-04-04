from predictor.helpers.db_connection import dbcursor_wrapper
from predictor.helpers.transaction_broker import transactional
from predictor.helpers.type_guard import consistcheck


class DAOtoDAO(object):

    __INSERT_OBJECT = "insert"
    __DELETE_OBJECT = "delete"

    entity = None

    sql_dict = {
                __INSERT_OBJECT: "INSERT INTO %s(%s,%s) VALUES( %%s, %%s );",
                __DELETE_OBJECT: "DELETE FROM %s WHERE %s"
              }

    def __str__(self):
        return "primDAO.uuid: %s secDAO.uuid: %s" % (self.primDAO_uuid, self.secDAO_uuid)

    def __init__(self, primDAO_uuid, secDAO_uuid):
        self.primDAO_uuid = primDAO_uuid
        self.secDAO_uuid = secDAO_uuid

    def __eq__(self, other, verbose=False):
        if other is not None and isinstance(other, self.__class__):
            if not verbose or self.__dict__ == other.__dict__:
                return self.__dict__ == other.__dict__
            else:
                if verbose:
                    msg = u"{0:s}".format ^ other.__dict__
                    print(msg)
        return False

    def __hash__(self):
        return hash(str(self))

    @transactional
    @consistcheck("insert")
    def save(self):
        sql_save = self.sql_dict[DAOtoDAO.__INSERT_OBJECT] % (self.entity, self.primDAO_PK, self.secDAO_PK)
        with dbcursor_wrapper(sql_save, [self.primDAO_uuid, self.secDAO_uuid]) as cursor:
            pass

    @transactional
    @consistcheck("delete")
    def delete(self):
        delete_condition = "%s='%s' AND %s='%s'" % (self.primDAO_PK, self.primDAO_uuid, self.secDAO_PK, self.secDAO_uuid)
        sql_delete = self.sql_dict[DAOtoDAO.__DELETE_OBJECT] % (self.entity, delete_condition)
        with dbcursor_wrapper(sql_delete) as cursor:
            pass


class DAOtoDAOList(set):

    __LOAD_LIST_SQL_KEY_NAME = "load"
    __DELETE_SQL_KEY_NAME = "delete"

    sql_dict = {__LOAD_LIST_SQL_KEY_NAME: "SELECT %s,%s FROM %s WHERE %s='%s'",
                __DELETE_SQL_KEY_NAME: "DELETE FROM %s WHERE %s='%s' AND %s='%s'"
                }

    def __str__(self):
        elem = []
        for e in self:
            elem.append("%s" % e)
        return ",".join(elem)

    def __init__(self, DAOtoDAO):
        super(DAOtoDAOList, self).__init__()
        self.prim_dao_to_dao = DAOtoDAO
        self.entity = DAOtoDAO.entity

    @consistcheck("load")
    def load(self, primDAO_uuid):
        query = DAOtoDAOList.sql_dict[DAOtoDAOList.__LOAD_LIST_SQL_KEY_NAME] % (self.prim_dao_to_dao.primDAO_PK,
                                                                                self.prim_dao_to_dao.secDAO_PK,
                                                                                self.entity,
                                                                                self.prim_dao_to_dao.primDAO_PK,
                                                                                primDAO_uuid)
        with dbcursor_wrapper(query) as cursor:
            rows = cursor.fetchall()
            for row in rows:
                self.add(self.prim_dao_to_dao(getattr(row, self.prim_dao_to_dao.primDAO_PK),
                                              getattr(row, self.prim_dao_to_dao.secDAO_PK)))

    @transactional
    def deleteall(self):
        for e in self:
            query = DAOtoDAOList.sql_dict[DAOtoDAOList.__DELETE_SQL_KEY_NAME] % (self.entity,
                                                                                 e.primDAO_PK,
                                                                                 e.primDAO_uuid,
                                                                                 e.secDAO_PK,
                                                                                 e.secDAO_uuid)
            with dbcursor_wrapper(query) as cursor:
                pass
            e.delete()

    @transactional
    def save(self):
        for e in self:
            e.save()
