import psycopg2.extras
from predictor.helpers.db_connection import dbcursor_wrapper, get_uuid_from_database
from predictor.helpers.transaction_broker import transactional
from predictor.helpers.type_guard import typecheck, consistcheck
from predictor.model.DAOtoDAO import DAOtoDAOList


class DAO(object):

    __LOAD_OBJECT_BY_UUID = "load"
    __DELETE_OBJECT_BY_UUID = "delete"
    __INSERT_OBJECT = "insert"
    __UPDATE_OBJECT = "update"

    sql_dict={__LOAD_OBJECT_BY_UUID: "SELECT %s FROM %s WHERE uuid='%s'",
              __DELETE_OBJECT_BY_UUID: "DELETE FROM %s WHERE uuid='%s'",
              __UPDATE_OBJECT: "UPDATE %s SET %s WHERE uuid='%s'",
              __INSERT_OBJECT: "INSERT INTO %s(%s) VALUES( %s );"
              }

    entity = None
    data_fields = ["uuid"]
    join_objects = {}
    sortkey = "uuid"

    def __init__(self, uuid=None, *initial_data):
        self.__is_persisted = False
        for key in self.join_objects.keys():
            setattr(self, key, DAOtoDAOList(self.join_objects[key]))

        if uuid is not None:
            self.uuid = uuid
        else:
            self.uuid = get_uuid_from_database()

        if initial_data is not None:
            for dictionary in initial_data:
                if dictionary is not None:
                    for key in self.__class__.data_fields:
                        if isinstance(dictionary, dict):
                            if key in dictionary:
                                setattr(self, key, dictionary[key])
                        else:
                            if hasattr(dictionary, key):
                                setattr(self, key, getattr(dictionary, key))
                        if not hasattr(self, key):
                            setattr(self, key, None)
        else:
            if uuid is not None:
                self.load()

    def __str__(self):
        ret_a = " ".join(list(map(lambda x: "%s:%s" % (x, getattr(self, x)), self.data_fields)))
        dao_to_dao_list = []
        for join_object_list in self.join_objects.keys():
            list_to_append = getattr(self, join_object_list)
            dao_to_dao_list.append("%s: {%s}" % (join_object_list, list_to_append))
        return "{ %s %s }" % (ret_a, " ".join(dao_to_dao_list))

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other, verbose=False):
        if other is not None and isinstance(other, self.__class__):
            if not verbose or self.__dict__ == other.__dict__:
                return self.__dict__ == other.__dict__
            else:
                if verbose:
                    msg = u"{0:s}".format ^ other.__dict__
                    print(msg)
        return False

    def __ne__(self, other):
        return not self == other

    @consistcheck("load")
    def load(self):
        sql_query_load = self.sql_dict[DAO.__LOAD_OBJECT_BY_UUID] % (",".join(self.__class__.data_fields), self.__class__.entity, self.uuid)
        order_by_clause = "ORDER BY %s" % self.__class__.sortkey
        sql_query_load = "%s %s" % (sql_query_load, order_by_clause)

        with dbcursor_wrapper(sql_query_load) as cursor:
            row = cursor.fetchone()
            if row is not None:
                for data_field in self.__class__.data_fields:
                    setattr(self, data_field, getattr(row, data_field))
                self.__is_persisted = True
            else:
                raise BaseException("row with uuid %s doesn't exist" % self.uuid)
        # load daotodao objects
        for join_object in self.join_objects.keys():
            join_object_list = getattr(self, join_object)
            join_object_list.load(self.uuid)

    @transactional
    def save(self):
        if self.__exists():
            self.__update()
        else:
            self.__insert()

    def __exists(self):
        sql_exists = "SELECT count(*) as counter FROM %s WHERE uuid='%s'" % (self.entity, self.uuid)
        counter = 0
        with dbcursor_wrapper(sql_exists) as cursor:
            row = cursor.fetchone()
            if row is not None:
                counter = getattr(row, "counter")
        if counter > 0:
            return True
        else:
            return False


    @consistcheck("insert")
    def __insert(self):
        fieldlist = []
        data = []
        for key in self.data_fields:
            fieldlist.append(key)
            data.append(getattr(self, key))
        sql_save = self.sql_dict[DAO.__INSERT_OBJECT] % (self.entity, ",".join(fieldlist), ",".join(list(map(lambda x: "%s", data))))
        with dbcursor_wrapper(sql_save, data) as cursor:
            pass
        self.__is_persisted = True
        for join_object in self.join_objects.keys():
            join_object_list = getattr(self, join_object)
            for elem in join_object_list:
                elem.save()

    @consistcheck("update")
    def __update(self):
        psycopg2.extras.register_uuid()
        setstr = ",".join(list(map(lambda x: x + "=%("+x+")s", filter(lambda x: x != "uuid", self.data_fields))))
        sql_update = self.sql_dict[DAO.__UPDATE_OBJECT] % (self.entity, setstr, self.uuid)
        h = dict()
        for f in self.data_fields:
            if f != 'uuid':
                h[f] = getattr(self,f)
        with dbcursor_wrapper(sql_update, h) as cursor:
            pass
        for join_object in self.join_objects.keys():
            join_object_list_to_compare = DAOtoDAOList(self.join_objects[join_object])
            join_object_list_to_compare.load(self.uuid)
            current_join_object_list = getattr(self, join_object)
            if join_object_list_to_compare ^ current_join_object_list is not None:
                join_object_list_to_compare.deleteall()
                current_join_object_list.save()

    @transactional
    @consistcheck("delete")
    def delete(self):
        sql_query = self.sql_dict[DAO.__DELETE_OBJECT_BY_UUID] % (self.__class__.entity, self.uuid)
        with dbcursor_wrapper(sql_query) as cursor:
            pass
        self.__is_persisted = False


class VDAO(DAO):

    def __init__(self, uuid, row=None):
        super(VDAO, self).__init__(uuid, row)

    def load(self):
        super(VDAO, self).load()

    def save(self):
        pass

    def delete(self):
        pass


class DAOList(set):

    __LOAD_LIST_SQL_KEY_NAME = "load"

    sql_dict = {__LOAD_LIST_SQL_KEY_NAME: "SELECT %s FROM %s %s"}

    def __str__(self):
        elems = []
        for e in self:
            elems.append("%s" % e)
        return ",".join(elems)

    def __init__(self, dao_list_type):
        """

        :type dao_list_type: object of DAO type
        """
        super(DAOList, self).__init__()
        self.dao = dao_list_type
        self.entity = dao_list_type.entity

    @typecheck
    def add(self, dao_to_add):
        super(DAOList, self).add(dao_to_add)

    @typecheck
    def remove(self, dao_to_delete):
        super(DAOList, self).remove(dao_to_delete)

    @consistcheck("load")
    def load(self, subset=None):
        where_clause = ""
        if subset is not None:
            where_clause = "WHERE %s" % subset
        query = DAOList.sql_dict[DAOList.__LOAD_LIST_SQL_KEY_NAME] % (",".join(self.dao.data_fields), self.entity, where_clause)
        with dbcursor_wrapper(query) as cursor:
            rows = cursor.fetchall()
            for row in rows:
                uuid = getattr(row, 'uuid')
                dao = self.dao(uuid, row)
                #dao.load()
                self.add(dao)


class DAOListl(list):

    __LOAD_LIST_SQL_KEY_NAME = "load"

    sql_dict = {__LOAD_LIST_SQL_KEY_NAME: "SELECT %s FROM %s %s"}

    def __str__(self):
        elems = []
        for e in self:
            elems.append("%s" % e)
        return ",".join(elems)

    def __init__(self, dao_list_type):
        """

        :type dao_list_type: object of DAO type
        """
        super(DAOListl, self).__init__()
        self.dao = dao_list_type
        self.entity = dao_list_type.entity

    @typecheck
    def append(self, dao_to_add):
        super(DAOListl, self).append(dao_to_add)

    @typecheck
    def remove(self, dao_to_delete):
        super(DAOListl, self).remove(dao_to_delete)

    @consistcheck("load")
    def load(self, subset=None):
        self.clear()
        where_clause = ""
        if subset is not None:
            where_clause = "WHERE %s" % subset
        query = DAOListl.sql_dict[DAOListl.__LOAD_LIST_SQL_KEY_NAME] % (",".join(self.dao.data_fields), self.entity, where_clause)
        order_clause = "ORDER BY %s" % self.dao.sortkey
        query = "%s %s" % (query, order_clause)
        with dbcursor_wrapper(query) as cursor:
            rows = cursor.fetchall()
            for row in rows:
                uuid = getattr(row, 'uuid')
                dao = self.dao(uuid, row)
                #dao.load()
                self.append(dao)