PGDMP             
            t         	   predictor    9.4.5    9.4.5 f    _           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                       false            `           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                       false            a           1262    19887 	   predictor    DATABASE     {   CREATE DATABASE predictor WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'de_DE.UTF-8' LC_CTYPE = 'de_DE.UTF-8';
    DROP DATABASE predictor;
             vvladych    false            b           1262    19887 	   predictor    COMMENT     G   COMMENT ON DATABASE predictor IS 'Database for the predictor project';
                  vvladych    false    3169                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
             postgres    false            c           0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                  postgres    false    6            d           0    0    public    ACL     �   REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;
                  postgres    false    6            �            3079    12809    plpgsql 	   EXTENSION     ?   CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;
    DROP EXTENSION plpgsql;
                  false            e           0    0    EXTENSION plpgsql    COMMENT     @   COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';
                       false    197            �            3079    20095 	   uuid-ossp 	   EXTENSION     ?   CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;
    DROP EXTENSION "uuid-ossp";
                  false    6            f           0    0    EXTENSION "uuid-ossp"    COMMENT     W   COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';
                       false    198            �           1247    20766    t_person_name_part_role    TYPE     �   CREATE TYPE t_person_name_part_role AS ENUM (
    'givenname',
    'middlename',
    'familyname',
    'patronym',
    'matronym',
    'noblerank',
    'academictitle',
    'shortname'
);
 *   DROP TYPE public.t_person_name_part_role;
       public       vvladych    false    6            �           1247    20752    t_person_name_role    TYPE     �   CREATE TYPE t_person_name_role AS ENUM (
    'realname',
    'pseudonym',
    'nickname',
    'codename',
    'religiousname',
    'commonname'
);
 %   DROP TYPE public.t_person_name_role;
       public       vvladych    false    6            �            1255    20106    set_prediction_created_date()    FUNCTION     �   CREATE FUNCTION set_prediction_created_date() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
	IF NEW.created_date IS NULL THEN
	NEW.created_date := NOW();
	END IF;
	RETURN NEW;
END$$;
 4   DROP FUNCTION public.set_prediction_created_date();
       public       vvladych    false    6    197            �            1259    20107    organisation    TABLE     y   CREATE TABLE organisation (
    uuid uuid DEFAULT uuid_generate_v4() NOT NULL,
    commonname character varying(4000)
);
     DROP TABLE public.organisation;
       public         vvladych    false    198    6    6            �            1259    20330 
   originator    TABLE     ~   CREATE TABLE originator (
    uuid uuid DEFAULT uuid_generate_v4() NOT NULL,
    short_description character varying(2000)
);
    DROP TABLE public.originator;
       public         vvladych    false    198    6    6            �            1259    20359    originator_to_organisation    TABLE     t   CREATE TABLE originator_to_organisation (
    originator_uuid uuid NOT NULL,
    organisation_uuid uuid NOT NULL
);
 .   DROP TABLE public.originator_to_organisation;
       public         vvladych    false    6            �            1259    20344    originator_to_person    TABLE     h   CREATE TABLE originator_to_person (
    originator_uuid uuid NOT NULL,
    person_uuid uuid NOT NULL
);
 (   DROP TABLE public.originator_to_person;
       public         vvladych    false    6            �            1259    20114    person    TABLE     �   CREATE TABLE person (
    uuid uuid DEFAULT uuid_generate_v4() NOT NULL,
    common_name character varying(2000),
    birth_date date
);
    DROP TABLE public.person;
       public         vvladych    false    198    6    6            �            1259    20121    person_to_personname    TABLE     h   CREATE TABLE person_to_personname (
    person_uuid uuid NOT NULL,
    personname_uuid uuid NOT NULL
);
 (   DROP TABLE public.person_to_personname;
       public         vvladych    false    6            �            1259    20124 
   personname    TABLE     w   CREATE TABLE personname (
    uuid uuid DEFAULT uuid_generate_v4() NOT NULL,
    personname_role t_person_name_role
);
    DROP TABLE public.personname;
       public         vvladych    false    198    6    6    647            �            1259    20131    personname_to_personnamepart    TABLE     x   CREATE TABLE personname_to_personnamepart (
    personname_uuid uuid NOT NULL,
    personnamepart_uuid uuid NOT NULL
);
 0   DROP TABLE public.personname_to_personnamepart;
       public         vvladych    false    6            �            1259    20134    personnamepart    TABLE     �   CREATE TABLE personnamepart (
    uuid uuid DEFAULT uuid_generate_v4() NOT NULL,
    namepart_value character varying(2000) NOT NULL,
    namepart_role t_person_name_part_role
);
 "   DROP TABLE public.personnamepart;
       public         vvladych    false    198    6    6    650            �            1259    20141 
   prediction    TABLE     �   CREATE TABLE prediction (
    uuid uuid DEFAULT uuid_generate_v4() NOT NULL,
    commonname character varying(4000) NOT NULL,
    short_description text,
    created_date date DEFAULT ('now'::text)::date NOT NULL
);
    DROP TABLE public.prediction;
       public         vvladych    false    198    6    6            �            1259    20374    prediction_to_originator    TABLE     p   CREATE TABLE prediction_to_originator (
    prediction_uuid uuid NOT NULL,
    originator_uuid uuid NOT NULL
);
 ,   DROP TABLE public.prediction_to_originator;
       public         vvladych    false    6            �            1259    20399    prediction_originator_V    VIEW     �  CREATE VIEW "prediction_originator_V" AS
 SELECT prediction.uuid,
    originator.uuid AS originator_uuid,
    person.uuid AS concrete_uuid,
    person.common_name,
    1 AS is_person,
    0 AS is_organisation
   FROM ((((prediction
     JOIN prediction_to_originator ON ((prediction.uuid = prediction_to_originator.prediction_uuid)))
     JOIN originator ON ((prediction_to_originator.originator_uuid = originator.uuid)))
     JOIN originator_to_person ON ((originator_to_person.originator_uuid = originator.uuid)))
     JOIN person ON ((originator_to_person.person_uuid = person.uuid)))
UNION ALL
 SELECT prediction.uuid,
    originator.uuid AS originator_uuid,
    organisation.uuid AS concrete_uuid,
    organisation.commonname AS common_name,
    0 AS is_person,
    1 AS is_organisation
   FROM ((((prediction
     JOIN prediction_to_originator ON ((prediction.uuid = prediction_to_originator.prediction_uuid)))
     JOIN originator ON ((prediction_to_originator.originator_uuid = originator.uuid)))
     JOIN originator_to_organisation ON ((originator_to_organisation.originator_uuid = originator.uuid)))
     JOIN organisation ON ((originator_to_organisation.organisation_uuid = organisation.uuid)));
 ,   DROP VIEW public."prediction_originator_V";
       public       vvladych    false    173    193    195    194    194    172    172    173    178    195    192    193    6            �            1259    20149    prediction_to_publication    TABLE     r   CREATE TABLE prediction_to_publication (
    prediction_uuid uuid NOT NULL,
    publication_uuid uuid NOT NULL
);
 -   DROP TABLE public.prediction_to_publication;
       public         vvladych    false    6            �            1259    20152    publication    TABLE     �   CREATE TABLE publication (
    uuid uuid DEFAULT uuid_generate_v4() NOT NULL,
    date date NOT NULL,
    title text,
    url character varying(4000)
);
    DROP TABLE public.publication;
       public         vvladych    false    198    6    6            �            1259    20159    publication_to_publisher    TABLE     p   CREATE TABLE publication_to_publisher (
    publisher_uuid uuid NOT NULL,
    publication_uuid uuid NOT NULL
);
 ,   DROP TABLE public.publication_to_publisher;
       public         vvladych    false    6            �            1259    20162 	   publisher    TABLE     �   CREATE TABLE publisher (
    uuid uuid DEFAULT uuid_generate_v4() NOT NULL,
    commonname character varying(2000) NOT NULL,
    url character varying(2000)
);
    DROP TABLE public.publisher;
       public         vvladych    false    198    6    6            �            1259    20169    prediction_publication_V    VIEW     a  CREATE VIEW "prediction_publication_V" AS
 SELECT prediction.uuid,
    publisher.commonname,
    publication.title,
    publication.date,
    publication.url,
    publication.uuid AS publication_uuid
   FROM ((((prediction
     JOIN prediction_to_publication ON ((prediction.uuid = prediction_to_publication.prediction_uuid)))
     JOIN publication ON ((prediction_to_publication.publication_uuid = publication.uuid)))
     JOIN publication_to_publisher ON ((publication.uuid = publication_to_publisher.publication_uuid)))
     JOIN publisher ON ((publication_to_publisher.publisher_uuid = publisher.uuid)));
 -   DROP VIEW public."prediction_publication_V";
       public       vvladych    false    182    182    181    181    180    180    180    180    179    179    178    6            �            1259    20174    prediction_to_textmodel    TABLE     n   CREATE TABLE prediction_to_textmodel (
    prediction_uuid uuid NOT NULL,
    textmodel_uuid uuid NOT NULL
);
 +   DROP TABLE public.prediction_to_textmodel;
       public         vvladych    false    6            �            1259    20177 	   textmodel    TABLE     �   CREATE TABLE textmodel (
    uuid uuid DEFAULT uuid_generate_v4() NOT NULL,
    date date,
    short_description character varying(4000)
);
    DROP TABLE public.textmodel;
       public         vvladych    false    198    6    6            �            1259    20322    prediction_textmodel_V    VIEW     i  CREATE VIEW "prediction_textmodel_V" AS
 SELECT prediction.uuid,
    textmodel.date,
    textmodel.short_description,
    textmodel.uuid AS textmodel_uuid
   FROM ((prediction
     JOIN prediction_to_textmodel ON ((prediction.uuid = prediction_to_textmodel.prediction_uuid)))
     JOIN textmodel ON ((prediction_to_textmodel.textmodel_uuid = textmodel.uuid)));
 +   DROP VIEW public."prediction_textmodel_V";
       public       vvladych    false    178    184    184    185    185    185    6            �            1259    20188    publication_to_publicationtext    TABLE     |   CREATE TABLE publication_to_publicationtext (
    publicationtext_uuid uuid NOT NULL,
    publication_uuid uuid NOT NULL
);
 2   DROP TABLE public.publication_to_publicationtext;
       public         vvladych    false    6            �            1259    20191    publicationtext    TABLE     c   CREATE TABLE publicationtext (
    uuid uuid DEFAULT uuid_generate_v4() NOT NULL,
    text text
);
 #   DROP TABLE public.publicationtext;
       public         vvladych    false    198    6    6            �            1259    20198    textmodel_to_tmstatement    TABLE     p   CREATE TABLE textmodel_to_tmstatement (
    textmodel_uuid uuid NOT NULL,
    tmstatement_uuid uuid NOT NULL
);
 ,   DROP TABLE public.textmodel_to_tmstatement;
       public         vvladych    false    6            �            1259    20201    tmstatement    TABLE     �   CREATE TABLE tmstatement (
    uuid uuid DEFAULT uuid_generate_v4() NOT NULL,
    text text NOT NULL,
    tmbegin date,
    tmend date
);
    DROP TABLE public.tmstatement;
       public         vvladych    false    198    6    6            �            1259    20326    textmodel_tmstatement_V    VIEW     �  CREATE VIEW "textmodel_tmstatement_V" AS
 SELECT textmodel.uuid,
    tmstatement.uuid AS tmstatement_uuid,
    tmstatement.tmbegin,
    tmstatement.tmend,
    tmstatement.text
   FROM ((textmodel
     JOIN textmodel_to_tmstatement ON ((textmodel.uuid = textmodel_to_tmstatement.textmodel_uuid)))
     JOIN tmstatement ON ((textmodel_to_tmstatement.tmstatement_uuid = tmstatement.uuid)));
 ,   DROP VIEW public."textmodel_tmstatement_V";
       public       vvladych    false    189    185    188    189    189    189    188    6            H          0    20107    organisation 
   TABLE DATA               1   COPY organisation (uuid, commonname) FROM stdin;
    public       vvladych    false    172   ��       Y          0    20330 
   originator 
   TABLE DATA               6   COPY originator (uuid, short_description) FROM stdin;
    public       vvladych    false    192   ԋ       [          0    20359    originator_to_organisation 
   TABLE DATA               Q   COPY originator_to_organisation (originator_uuid, organisation_uuid) FROM stdin;
    public       vvladych    false    194   �       Z          0    20344    originator_to_person 
   TABLE DATA               E   COPY originator_to_person (originator_uuid, person_uuid) FROM stdin;
    public       vvladych    false    193   �       I          0    20114    person 
   TABLE DATA               8   COPY person (uuid, common_name, birth_date) FROM stdin;
    public       vvladych    false    173   +�       J          0    20121    person_to_personname 
   TABLE DATA               E   COPY person_to_personname (person_uuid, personname_uuid) FROM stdin;
    public       vvladych    false    174   H�       K          0    20124 
   personname 
   TABLE DATA               4   COPY personname (uuid, personname_role) FROM stdin;
    public       vvladych    false    175   e�       L          0    20131    personname_to_personnamepart 
   TABLE DATA               U   COPY personname_to_personnamepart (personname_uuid, personnamepart_uuid) FROM stdin;
    public       vvladych    false    176   ��       M          0    20134    personnamepart 
   TABLE DATA               F   COPY personnamepart (uuid, namepart_value, namepart_role) FROM stdin;
    public       vvladych    false    177   ��       N          0    20141 
   prediction 
   TABLE DATA               P   COPY prediction (uuid, commonname, short_description, created_date) FROM stdin;
    public       vvladych    false    178   ��       \          0    20374    prediction_to_originator 
   TABLE DATA               M   COPY prediction_to_originator (prediction_uuid, originator_uuid) FROM stdin;
    public       vvladych    false    195   ٌ       O          0    20149    prediction_to_publication 
   TABLE DATA               O   COPY prediction_to_publication (prediction_uuid, publication_uuid) FROM stdin;
    public       vvladych    false    179   ��       S          0    20174    prediction_to_textmodel 
   TABLE DATA               K   COPY prediction_to_textmodel (prediction_uuid, textmodel_uuid) FROM stdin;
    public       vvladych    false    184   �       P          0    20152    publication 
   TABLE DATA               6   COPY publication (uuid, date, title, url) FROM stdin;
    public       vvladych    false    180   0�       U          0    20188    publication_to_publicationtext 
   TABLE DATA               Y   COPY publication_to_publicationtext (publicationtext_uuid, publication_uuid) FROM stdin;
    public       vvladych    false    186   M�       Q          0    20159    publication_to_publisher 
   TABLE DATA               M   COPY publication_to_publisher (publisher_uuid, publication_uuid) FROM stdin;
    public       vvladych    false    181   j�       V          0    20191    publicationtext 
   TABLE DATA               .   COPY publicationtext (uuid, text) FROM stdin;
    public       vvladych    false    187   ��       R          0    20162 	   publisher 
   TABLE DATA               3   COPY publisher (uuid, commonname, url) FROM stdin;
    public       vvladych    false    182   ��       T          0    20177 	   textmodel 
   TABLE DATA               ;   COPY textmodel (uuid, date, short_description) FROM stdin;
    public       vvladych    false    185   ��       W          0    20198    textmodel_to_tmstatement 
   TABLE DATA               M   COPY textmodel_to_tmstatement (textmodel_uuid, tmstatement_uuid) FROM stdin;
    public       vvladych    false    188   ލ       X          0    20201    tmstatement 
   TABLE DATA               :   COPY tmstatement (uuid, text, tmbegin, tmend) FROM stdin;
    public       vvladych    false    189   ��       �           2606    20209    organisation_PK 
   CONSTRAINT     W   ALTER TABLE ONLY organisation
    ADD CONSTRAINT "organisation_PK" PRIMARY KEY (uuid);
 H   ALTER TABLE ONLY public.organisation DROP CONSTRAINT "organisation_PK";
       public         vvladych    false    172    172            �           2606    20343    originator_PK 
   CONSTRAINT     S   ALTER TABLE ONLY originator
    ADD CONSTRAINT "originator_PK" PRIMARY KEY (uuid);
 D   ALTER TABLE ONLY public.originator DROP CONSTRAINT "originator_PK";
       public         vvladych    false    192    192            �           2606    20363    originator_to_organisation_PK 
   CONSTRAINT     �   ALTER TABLE ONLY originator_to_organisation
    ADD CONSTRAINT "originator_to_organisation_PK" PRIMARY KEY (originator_uuid, organisation_uuid);
 d   ALTER TABLE ONLY public.originator_to_organisation DROP CONSTRAINT "originator_to_organisation_PK";
       public         vvladych    false    194    194    194            �           2606    20348    originator_to_person_PK 
   CONSTRAINT        ALTER TABLE ONLY originator_to_person
    ADD CONSTRAINT "originator_to_person_PK" PRIMARY KEY (originator_uuid, person_uuid);
 X   ALTER TABLE ONLY public.originator_to_person DROP CONSTRAINT "originator_to_person_PK";
       public         vvladych    false    193    193    193            �           2606    20211 	   person_PK 
   CONSTRAINT     K   ALTER TABLE ONLY person
    ADD CONSTRAINT "person_PK" PRIMARY KEY (uuid);
 <   ALTER TABLE ONLY public.person DROP CONSTRAINT "person_PK";
       public         vvladych    false    173    173            �           2606    20213    person_to_personname_PK 
   CONSTRAINT        ALTER TABLE ONLY person_to_personname
    ADD CONSTRAINT "person_to_personname_PK" PRIMARY KEY (person_uuid, personname_uuid);
 X   ALTER TABLE ONLY public.person_to_personname DROP CONSTRAINT "person_to_personname_PK";
       public         vvladych    false    174    174    174            �           2606    20215    personname_PK 
   CONSTRAINT     S   ALTER TABLE ONLY personname
    ADD CONSTRAINT "personname_PK" PRIMARY KEY (uuid);
 D   ALTER TABLE ONLY public.personname DROP CONSTRAINT "personname_PK";
       public         vvladych    false    175    175            �           2606    20217    personname_to_personnamepart_PK 
   CONSTRAINT     �   ALTER TABLE ONLY personname_to_personnamepart
    ADD CONSTRAINT "personname_to_personnamepart_PK" PRIMARY KEY (personname_uuid, personnamepart_uuid);
 h   ALTER TABLE ONLY public.personname_to_personnamepart DROP CONSTRAINT "personname_to_personnamepart_PK";
       public         vvladych    false    176    176    176            �           2606    20219    personnamepart_PK 
   CONSTRAINT     [   ALTER TABLE ONLY personnamepart
    ADD CONSTRAINT "personnamepart_PK" PRIMARY KEY (uuid);
 L   ALTER TABLE ONLY public.personnamepart DROP CONSTRAINT "personnamepart_PK";
       public         vvladych    false    177    177            �           2606    20221    prediction_PK 
   CONSTRAINT     S   ALTER TABLE ONLY prediction
    ADD CONSTRAINT "prediction_PK" PRIMARY KEY (uuid);
 D   ALTER TABLE ONLY public.prediction DROP CONSTRAINT "prediction_PK";
       public         vvladych    false    178    178            �           2606    20378    prediction_to_originator_PK 
   CONSTRAINT     �   ALTER TABLE ONLY prediction_to_originator
    ADD CONSTRAINT "prediction_to_originator_PK" PRIMARY KEY (prediction_uuid, originator_uuid);
 `   ALTER TABLE ONLY public.prediction_to_originator DROP CONSTRAINT "prediction_to_originator_PK";
       public         vvladych    false    195    195    195            �           2606    20223    prediction_to_publication_PK 
   CONSTRAINT     �   ALTER TABLE ONLY prediction_to_publication
    ADD CONSTRAINT "prediction_to_publication_PK" PRIMARY KEY (prediction_uuid, publication_uuid);
 b   ALTER TABLE ONLY public.prediction_to_publication DROP CONSTRAINT "prediction_to_publication_PK";
       public         vvladych    false    179    179    179            �           2606    20225    prediction_to_textmodel_PK 
   CONSTRAINT     �   ALTER TABLE ONLY prediction_to_textmodel
    ADD CONSTRAINT "prediction_to_textmodel_PK" PRIMARY KEY (prediction_uuid, textmodel_uuid);
 ^   ALTER TABLE ONLY public.prediction_to_textmodel DROP CONSTRAINT "prediction_to_textmodel_PK";
       public         vvladych    false    184    184    184            �           2606    20227    publication_PK 
   CONSTRAINT     U   ALTER TABLE ONLY publication
    ADD CONSTRAINT "publication_PK" PRIMARY KEY (uuid);
 F   ALTER TABLE ONLY public.publication DROP CONSTRAINT "publication_PK";
       public         vvladych    false    180    180            �           2606    20229 !   publication_to_publicationtext_PK 
   CONSTRAINT     �   ALTER TABLE ONLY publication_to_publicationtext
    ADD CONSTRAINT "publication_to_publicationtext_PK" PRIMARY KEY (publicationtext_uuid, publication_uuid);
 l   ALTER TABLE ONLY public.publication_to_publicationtext DROP CONSTRAINT "publication_to_publicationtext_PK";
       public         vvladych    false    186    186    186            �           2606    20231    publicationtext_PK 
   CONSTRAINT     ]   ALTER TABLE ONLY publicationtext
    ADD CONSTRAINT "publicationtext_PK" PRIMARY KEY (uuid);
 N   ALTER TABLE ONLY public.publicationtext DROP CONSTRAINT "publicationtext_PK";
       public         vvladych    false    187    187            �           2606    20233    publisher_PK 
   CONSTRAINT     Q   ALTER TABLE ONLY publisher
    ADD CONSTRAINT "publisher_PK" PRIMARY KEY (uuid);
 B   ALTER TABLE ONLY public.publisher DROP CONSTRAINT "publisher_PK";
       public         vvladych    false    182    182            �           2606    20235    publisher_to_publication_PK 
   CONSTRAINT     �   ALTER TABLE ONLY publication_to_publisher
    ADD CONSTRAINT "publisher_to_publication_PK" PRIMARY KEY (publisher_uuid, publication_uuid);
 `   ALTER TABLE ONLY public.publication_to_publisher DROP CONSTRAINT "publisher_to_publication_PK";
       public         vvladych    false    181    181    181            �           2606    20237    textmodel_PK 
   CONSTRAINT     Q   ALTER TABLE ONLY textmodel
    ADD CONSTRAINT "textmodel_PK" PRIMARY KEY (uuid);
 B   ALTER TABLE ONLY public.textmodel DROP CONSTRAINT "textmodel_PK";
       public         vvladych    false    185    185            �           2606    20239    textmodel_tmstatement_PK 
   CONSTRAINT     �   ALTER TABLE ONLY textmodel_to_tmstatement
    ADD CONSTRAINT "textmodel_tmstatement_PK" PRIMARY KEY (textmodel_uuid, tmstatement_uuid);
 ]   ALTER TABLE ONLY public.textmodel_to_tmstatement DROP CONSTRAINT "textmodel_tmstatement_PK";
       public         vvladych    false    188    188    188            �           2606    20241    tmstatement_PK 
   CONSTRAINT     U   ALTER TABLE ONLY tmstatement
    ADD CONSTRAINT "tmstatement_PK" PRIMARY KEY (uuid);
 F   ALTER TABLE ONLY public.tmstatement DROP CONSTRAINT "tmstatement_PK";
       public         vvladych    false    189    189            �           2620    20242 "   prediction_create_date_INS_UPD_TRG    TRIGGER     �   CREATE TRIGGER "prediction_create_date_INS_UPD_TRG" BEFORE INSERT OR UPDATE ON prediction FOR EACH ROW EXECUTE PROCEDURE set_prediction_created_date();
 H   DROP TRIGGER "prediction_create_date_INS_UPD_TRG" ON public.prediction;
       public       vvladych    false    221    178            �           2606    20369 *   originator_to_organisation_organisation_FK    FK CONSTRAINT     �   ALTER TABLE ONLY originator_to_organisation
    ADD CONSTRAINT "originator_to_organisation_organisation_FK" FOREIGN KEY (organisation_uuid) REFERENCES organisation(uuid) ON UPDATE CASCADE ON DELETE CASCADE;
 q   ALTER TABLE ONLY public.originator_to_organisation DROP CONSTRAINT "originator_to_organisation_organisation_FK";
       public       vvladych    false    194    2969    172            �           2606    20364 (   originator_to_organisation_originator_FK    FK CONSTRAINT     �   ALTER TABLE ONLY originator_to_organisation
    ADD CONSTRAINT "originator_to_organisation_originator_FK" FOREIGN KEY (originator_uuid) REFERENCES originator(uuid) ON UPDATE CASCADE ON DELETE CASCADE;
 o   ALTER TABLE ONLY public.originator_to_organisation DROP CONSTRAINT "originator_to_organisation_originator_FK";
       public       vvladych    false    3003    192    194            �           2606    20349 "   originator_to_person_originator_FK    FK CONSTRAINT     �   ALTER TABLE ONLY originator_to_person
    ADD CONSTRAINT "originator_to_person_originator_FK" FOREIGN KEY (originator_uuid) REFERENCES originator(uuid) ON UPDATE CASCADE ON DELETE CASCADE;
 c   ALTER TABLE ONLY public.originator_to_person DROP CONSTRAINT "originator_to_person_originator_FK";
       public       vvladych    false    3003    192    193            �           2606    20354    originator_to_person_person_FK    FK CONSTRAINT     �   ALTER TABLE ONLY originator_to_person
    ADD CONSTRAINT "originator_to_person_person_FK" FOREIGN KEY (person_uuid) REFERENCES person(uuid) ON UPDATE CASCADE ON DELETE CASCADE;
 _   ALTER TABLE ONLY public.originator_to_person DROP CONSTRAINT "originator_to_person_person_FK";
       public       vvladych    false    193    173    2971            �           2606    20243    person_to_personname_person_FK    FK CONSTRAINT     �   ALTER TABLE ONLY person_to_personname
    ADD CONSTRAINT "person_to_personname_person_FK" FOREIGN KEY (person_uuid) REFERENCES person(uuid) ON UPDATE CASCADE ON DELETE CASCADE;
 _   ALTER TABLE ONLY public.person_to_personname DROP CONSTRAINT "person_to_personname_person_FK";
       public       vvladych    false    173    174    2971            �           2606    20248 "   person_to_personname_personname_FK    FK CONSTRAINT     �   ALTER TABLE ONLY person_to_personname
    ADD CONSTRAINT "person_to_personname_personname_FK" FOREIGN KEY (personname_uuid) REFERENCES personname(uuid) ON UPDATE CASCADE ON DELETE CASCADE;
 c   ALTER TABLE ONLY public.person_to_personname DROP CONSTRAINT "person_to_personname_personname_FK";
       public       vvladych    false    2975    175    174            �           2606    20253 *   personname_to_personnamepart_personname_FK    FK CONSTRAINT     �   ALTER TABLE ONLY personname_to_personnamepart
    ADD CONSTRAINT "personname_to_personnamepart_personname_FK" FOREIGN KEY (personname_uuid) REFERENCES personname(uuid) ON UPDATE CASCADE ON DELETE CASCADE;
 s   ALTER TABLE ONLY public.personname_to_personnamepart DROP CONSTRAINT "personname_to_personnamepart_personname_FK";
       public       vvladych    false    176    175    2975            �           2606    20258 .   personname_to_personnamepart_personnamepart_FK    FK CONSTRAINT     �   ALTER TABLE ONLY personname_to_personnamepart
    ADD CONSTRAINT "personname_to_personnamepart_personnamepart_FK" FOREIGN KEY (personnamepart_uuid) REFERENCES personnamepart(uuid) ON UPDATE CASCADE ON DELETE CASCADE;
 w   ALTER TABLE ONLY public.personname_to_personnamepart DROP CONSTRAINT "personname_to_personnamepart_personnamepart_FK";
       public       vvladych    false    177    2979    176            �           2606    20384 &   prediction_to_originator_originator_FK    FK CONSTRAINT     �   ALTER TABLE ONLY prediction_to_originator
    ADD CONSTRAINT "prediction_to_originator_originator_FK" FOREIGN KEY (originator_uuid) REFERENCES originator(uuid) ON UPDATE CASCADE ON DELETE CASCADE;
 k   ALTER TABLE ONLY public.prediction_to_originator DROP CONSTRAINT "prediction_to_originator_originator_FK";
       public       vvladych    false    192    3003    195            �           2606    20379 &   prediction_to_originator_prediction_FK    FK CONSTRAINT     �   ALTER TABLE ONLY prediction_to_originator
    ADD CONSTRAINT "prediction_to_originator_prediction_FK" FOREIGN KEY (prediction_uuid) REFERENCES prediction(uuid) ON UPDATE CASCADE ON DELETE CASCADE;
 k   ALTER TABLE ONLY public.prediction_to_originator DROP CONSTRAINT "prediction_to_originator_prediction_FK";
       public       vvladych    false    2981    195    178            �           2606    20263 '   prediction_to_publication_prediction_FK    FK CONSTRAINT     �   ALTER TABLE ONLY prediction_to_publication
    ADD CONSTRAINT "prediction_to_publication_prediction_FK" FOREIGN KEY (prediction_uuid) REFERENCES prediction(uuid) ON UPDATE CASCADE ON DELETE CASCADE;
 m   ALTER TABLE ONLY public.prediction_to_publication DROP CONSTRAINT "prediction_to_publication_prediction_FK";
       public       vvladych    false    178    2981    179            �           2606    20268 (   prediction_to_publication_publication_FK    FK CONSTRAINT     �   ALTER TABLE ONLY prediction_to_publication
    ADD CONSTRAINT "prediction_to_publication_publication_FK" FOREIGN KEY (publication_uuid) REFERENCES publication(uuid) ON UPDATE CASCADE ON DELETE CASCADE;
 n   ALTER TABLE ONLY public.prediction_to_publication DROP CONSTRAINT "prediction_to_publication_publication_FK";
       public       vvladych    false    2985    179    180            �           2606    20273 %   prediction_to_textmodel_prediction_FK    FK CONSTRAINT     �   ALTER TABLE ONLY prediction_to_textmodel
    ADD CONSTRAINT "prediction_to_textmodel_prediction_FK" FOREIGN KEY (prediction_uuid) REFERENCES prediction(uuid) ON UPDATE CASCADE ON DELETE CASCADE;
 i   ALTER TABLE ONLY public.prediction_to_textmodel DROP CONSTRAINT "prediction_to_textmodel_prediction_FK";
       public       vvladych    false    2981    178    184            �           2606    20278 $   prediction_to_textmodel_textmodel_FK    FK CONSTRAINT     �   ALTER TABLE ONLY prediction_to_textmodel
    ADD CONSTRAINT "prediction_to_textmodel_textmodel_FK" FOREIGN KEY (textmodel_uuid) REFERENCES textmodel(uuid) ON UPDATE CASCADE ON DELETE CASCADE;
 h   ALTER TABLE ONLY public.prediction_to_textmodel DROP CONSTRAINT "prediction_to_textmodel_textmodel_FK";
       public       vvladych    false    2993    185    184            �           2606    20283 -   publication_to_publicationtext_publication_FK    FK CONSTRAINT     �   ALTER TABLE ONLY publication_to_publicationtext
    ADD CONSTRAINT "publication_to_publicationtext_publication_FK" FOREIGN KEY (publication_uuid) REFERENCES publication(uuid) ON UPDATE CASCADE ON DELETE CASCADE;
 x   ALTER TABLE ONLY public.publication_to_publicationtext DROP CONSTRAINT "publication_to_publicationtext_publication_FK";
       public       vvladych    false    180    186    2985            �           2606    20288 1   publication_to_publicationtext_publicationtext_FK    FK CONSTRAINT     �   ALTER TABLE ONLY publication_to_publicationtext
    ADD CONSTRAINT "publication_to_publicationtext_publicationtext_FK" FOREIGN KEY (publicationtext_uuid) REFERENCES publicationtext(uuid) ON UPDATE CASCADE ON DELETE CASCADE;
 |   ALTER TABLE ONLY public.publication_to_publicationtext DROP CONSTRAINT "publication_to_publicationtext_publicationtext_FK";
       public       vvladych    false    2997    186    187            �           2606    20293 '   publisher_to_publication_publication_FK    FK CONSTRAINT     �   ALTER TABLE ONLY publication_to_publisher
    ADD CONSTRAINT "publisher_to_publication_publication_FK" FOREIGN KEY (publication_uuid) REFERENCES publication(uuid) ON UPDATE CASCADE ON DELETE CASCADE;
 l   ALTER TABLE ONLY public.publication_to_publisher DROP CONSTRAINT "publisher_to_publication_publication_FK";
       public       vvladych    false    180    181    2985            �           2606    20298 %   publisher_to_publication_publisher_FK    FK CONSTRAINT     �   ALTER TABLE ONLY publication_to_publisher
    ADD CONSTRAINT "publisher_to_publication_publisher_FK" FOREIGN KEY (publisher_uuid) REFERENCES publisher(uuid) ON UPDATE CASCADE ON DELETE CASCADE;
 j   ALTER TABLE ONLY public.publication_to_publisher DROP CONSTRAINT "publisher_to_publication_publisher_FK";
       public       vvladych    false    181    2989    182            �           2606    20303 "   textmodel_tmstatement_textmodel_FK    FK CONSTRAINT     �   ALTER TABLE ONLY textmodel_to_tmstatement
    ADD CONSTRAINT "textmodel_tmstatement_textmodel_FK" FOREIGN KEY (textmodel_uuid) REFERENCES textmodel(uuid) ON UPDATE CASCADE ON DELETE CASCADE;
 g   ALTER TABLE ONLY public.textmodel_to_tmstatement DROP CONSTRAINT "textmodel_tmstatement_textmodel_FK";
       public       vvladych    false    2993    185    188            �           2606    20308 $   textmodel_tmstatement_tmstatement_FK    FK CONSTRAINT     �   ALTER TABLE ONLY textmodel_to_tmstatement
    ADD CONSTRAINT "textmodel_tmstatement_tmstatement_FK" FOREIGN KEY (tmstatement_uuid) REFERENCES tmstatement(uuid) ON UPDATE CASCADE ON DELETE CASCADE;
 i   ALTER TABLE ONLY public.textmodel_to_tmstatement DROP CONSTRAINT "textmodel_tmstatement_tmstatement_FK";
       public       vvladych    false    3001    188    189            H      x������ � �      Y      x������ � �      [      x������ � �      Z      x������ � �      I      x������ � �      J      x������ � �      K      x������ � �      L      x������ � �      M      x������ � �      N      x������ � �      \      x������ � �      O      x������ � �      S      x������ � �      P      x������ � �      U      x������ � �      Q      x������ � �      V      x������ � �      R      x������ � �      T      x������ � �      W      x������ � �      X      x������ � �     