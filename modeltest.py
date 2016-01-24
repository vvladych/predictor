from predictor.model.predictor_model import PublicationDAO, PublicationtextDAO, PublisherDAO
from predictor.helpers.transaction_broker import transactional
import datetime


@transactional
def insert_new_publication_from_mask(pub_uuid, publ_uuid):
    publication_title = "testtitle"
    publication_text = "testtext"
    publication_url = "testurl"

    # insert publication
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

def main():
    """
    "publication_uuid: 05c59662-7356-4eda-84bb-1f880911ca9e"
    "publisher_uuid: e5df9499-bae7-4f71-9eb1-3427444eeb21"
    """
    insert_new_publication_from_mask("05c59662-7356-4eda-84bb-1f880911ca9e", "e5df9499-bae7-4f71-9eb1-3427444eeb21")

if __name__ == '__main__':
    main()