from predictor.model.predictor_model import PublicationDAO, PublicationtextDAO, PublisherDAO, Binaryfiles
from predictor.helpers.transaction_broker import transactional
from predictor.helpers.db_connection import get_db_connection
import datetime
import psycopg2
import tempfile
import subprocess


@transactional
def insert_new_publication_from_mask(pub_uuid, publ_uuid):
    publication_title = "testtitle"
    publication_text = "testtext"
    publication_url = "testurl"

    # insert predpublication
    publication_uuid = None
    if pub_uuid is not None:
        publication_uuid = pub_uuid

    publication = PublicationDAO(publication_uuid,
                                 datetime.date(2016, 1, 23),
                                 publication_title,
                                 publication_url)

    publication_text_DAO = PublicationtextDAO()
    publication_text_DAO.text = publication_text
    publication_text_DAO.save()
    publication.add_publicationtext(publication_text_DAO)

    publisher_uuid = publ_uuid
    publisher = PublisherDAO(publisher_uuid)
    publication.add_publisher(publisher)

    publication.save()

    print("Done")

@transactional
def import_pdf():
    conn = get_db_connection()
    data = open("/tmp/kprog20151209-Kurzfassung.pdf", mode='rb').read()
    cur = conn.cursor()
    cur.execute("INSERT INTO binaryfiles_tst(filecontent) VALUES(%s)", (psycopg2.Binary(data),))
    conn.commit()

def tmpfile():
    data = open("/tmp/kprog20151209-Kurzfassung.pdf", mode='rb').read()
    tmpfile = tempfile.NamedTemporaryFile()
    tmpfile.write(data)
    print(tmpfile.name)
    subprocess.call(["evince", tmpfile.name])
    tmpfile.close()

def read_pdf_from_db():
    conn = get_db_connection()
    cur = conn.cursor()
    sql = "SELECT filecontent FROM binaryfiles_tst WHERE uuid='76136328-5ad5-4f86-b383-87e634a61fee';"
    cur.execute(sql)
    rows = cur.fetchone()
    tmpfile = tempfile.NamedTemporaryFile()
    tmpfile.write(bytes(rows[0]))
    subprocess.call(["evince", tmpfile.name])
    tmpfile.close()
    conn.close()


def write_into_db():
    conn = get_db_connection()
    cur = conn.cursor()
    fieldlist=["uuid", "filecontent"]
    data = ["6636bcbf-ac4a-4b2e-a4f4-2fc9b3c6b995", psycopg2.Binary(bytes("data_b","utf-8"))]

    sql_save = "insert into %s (%s) VALUES(%s)" % ("binaryfiles_tst", ",".join(fieldlist), ",".join(list(map(lambda x: "%s", data))))
    print(sql_save)
    cur.execute(sql_save, data)
    conn.commit()
    conn.close()


@transactional
def write_binarydao():
    bindao = Binaryfiles(None, {"filecontent":"data_bbbb"})
    bindao.save()
    print("Done")


def main():
    """
    "publication_uuid: 05c59662-7356-4eda-84bb-1f880911ca9e"
    "publisher_uuid: e5df9499-bae7-4f71-9eb1-3427444eeb21"
    """
    #insert_new_publication_from_mask("05c59662-7356-4eda-84bb-1f880911ca9e", "e5df9499-bae7-4f71-9eb1-3427444eeb21")
    #import_pdf()
    #tmpfile()
    #read_pdf_from_db()
    #write_into_db()
    write_binarydao()


if __name__ == '__main__':
    main()