PGDMP                         z            db6elkibg0sqru     14.5 (Ubuntu 14.5-1.pgdg20.04+1)    14.4     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    1652099    db6elkibg0sqru    DATABASE     c   CREATE DATABASE db6elkibg0sqru WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_US.UTF-8';
    DROP DATABASE db6elkibg0sqru;
                fiigtcykyydanj    false            �           0    0    DATABASE db6elkibg0sqru    ACL     A   REVOKE CONNECT,TEMPORARY ON DATABASE db6elkibg0sqru FROM PUBLIC;
                   fiigtcykyydanj    false    4326            �           0    0    db6elkibg0sqru    DATABASE PROPERTIES     R   ALTER DATABASE db6elkibg0sqru SET search_path TO '$user', 'public', 'heroku_ext';
                     fiigtcykyydanj    false                        2615    1652105 
   heroku_ext    SCHEMA        CREATE SCHEMA heroku_ext;
    DROP SCHEMA heroku_ext;
                u7f0t8ut1mnl4b    false            �           0    0    SCHEMA heroku_ext    ACL     4   GRANT USAGE ON SCHEMA heroku_ext TO fiigtcykyydanj;
                   u7f0t8ut1mnl4b    false    6            �           0    0    SCHEMA public    ACL     �   REVOKE ALL ON SCHEMA public FROM postgres;
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO fiigtcykyydanj;
GRANT ALL ON SCHEMA public TO PUBLIC;
                   fiigtcykyydanj    false    5            �           0    0    LANGUAGE plpgsql    ACL     1   GRANT ALL ON LANGUAGE plpgsql TO fiigtcykyydanj;
                   postgres    false    847            �            1259    1654196    action    TABLE     �   CREATE TABLE public.action (
    name_id integer NOT NULL,
    name character(200),
    description character(200),
    time_start character(20),
    day_start date,
    class integer DEFAULT 1 NOT NULL
);
    DROP TABLE public.action;
       public         heap    fiigtcykyydanj    false            �            1259    1654200    action_name_id_seq    SEQUENCE     �   ALTER TABLE public.action ALTER COLUMN name_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.action_name_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          fiigtcykyydanj    false    210            �            1259    1654201    action_tmrrw    VIEW     
  CREATE VIEW public.action_tmrrw AS
 SELECT action.name_id,
    action.name,
    action.description,
    action.time_start,
    action.day_start
   FROM public.action
  WHERE ((action.class = 1) AND (action.day_start = ( SELECT (CURRENT_DATE + '1 day'::interval))));
    DROP VIEW public.action_tmrrw;
       public          fiigtcykyydanj    false    210    210    210    210    210    210            �            1259    1654205    action_tmrrw_scond    VIEW       CREATE VIEW public.action_tmrrw_scond AS
 SELECT action.name_id,
    action.name,
    action.description,
    action.time_start,
    action.day_start
   FROM public.action
  WHERE ((action.class = 2) AND (action.day_start = ( SELECT (CURRENT_DATE + '1 day'::interval))));
 %   DROP VIEW public.action_tmrrw_scond;
       public          fiigtcykyydanj    false    210    210    210    210    210    210            �            1259    1654209    action_today    VIEW     �   CREATE VIEW public.action_today AS
 SELECT action.name_id,
    action.name,
    action.description,
    action.time_start,
    action.day_start
   FROM public.action
  WHERE ((action.class = 1) AND (action.day_start = ( SELECT CURRENT_DATE AS tday)));
    DROP VIEW public.action_today;
       public          fiigtcykyydanj    false    210    210    210    210    210    210            �            1259    1654213    action_today_scond    VIEW       CREATE VIEW public.action_today_scond AS
 SELECT action.name_id,
    action.name,
    action.description,
    action.time_start,
    action.day_start
   FROM public.action
  WHERE ((action.class = 2) AND (action.day_start = ( SELECT CURRENT_DATE AS "current_date")));
 %   DROP VIEW public.action_today_scond;
       public          fiigtcykyydanj    false    210    210    210    210    210    210            �            1259    1654218    select_all_data    VIEW     +  CREATE VIEW public.select_all_data AS
 SELECT action.name_id,
    action.name,
    action.time_start,
    action.day_start,
    action.class
   FROM public.action
  WHERE (action.day_start = ( SELECT (CURRENT_DATE + '1 day'::interval)))
  ORDER BY action.class, action.day_start, action.time_start;
 "   DROP VIEW public.select_all_data;
       public          fiigtcykyydanj    false    210    210    210    210    210            �          0    1654196    action 
   TABLE DATA           Z   COPY public.action (name_id, name, description, time_start, day_start, class) FROM stdin;
    public          fiigtcykyydanj    false    210   �       �           0    0    action_name_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.action_name_id_seq', 173, true);
          public          fiigtcykyydanj    false    211            N           2606    1654226    action action_pkey 
   CONSTRAINT     U   ALTER TABLE ONLY public.action
    ADD CONSTRAINT action_pkey PRIMARY KEY (name_id);
 <   ALTER TABLE ONLY public.action DROP CONSTRAINT action_pkey;
       public            fiigtcykyydanj    false    210            �   a  x��][sG~��<�B��gtu�����%1�K����`l��ɖ�,$l\�Ąݗ��%��"_$������F��Q�푧�]������������J����
���K޲�w�R�.T�/Yǲ%�OЉ��LݨX���W�"t��-B���5�Y�������w+��a�Ŋ|��ý=�b_������-�� ������I|�Ez�
߄7�G �����q��|��I8}NZ/:�lv�{�/b���ty�."� ��Y�o nm{O�lx�-��]�*y����@F����{��S�e���9����.���q���h�M���Y�x;�8>���7p$���@��9�!��,� �ԩ]����_ԅ�� ��t��� �bDԽ��8�x���N%[b�[|�1���p֏�n��n�賀��/gX�m5��gA�\���LE!�D$˨�Y��cw{@��/�B��F�`L�:d�(�>D� ~��-�E��>q�|��;�����tg+`mT��4I�4�h��!�Iz���4�N�y�ʟ��Ǩ?�A�sB����ݜ;�A~�ɡ�#!&&qH#�C�k|����ԕ�S�����ua5�:"W"e_Y�ӻJ�[�`��ưsH�L�ɠ��@X������3>ND6�+䣞��)����AN�<�� ��B��2]���` ��Bϑ�t�5=�X{�pc2�r -dQ �Q>�`ɨ?l$��UC2h�Oʽs੯`�/��J�K�����~{��2ƶ� /{��0Erb7/4t Y�5�[����T2�֎X;�i�!5��I�i(�R�ޡ7��dH����QC�B�+
C�n��J�A�T��N�Z�V�@�B}����xi�:~��K����U�.Q�%���	���|�Q_�J���'�g�)B)(�#�J��l:���7�YD��*��I�6��oI
�2�hٿ�B�a���������W"����G[Q�L��82�W������+�Ijb|#���W��M�_Ĩ+��N(����O����=�)d8��׵���m��0R�W�8�P���O�<o��L��3]O�F
���Sw�߁���Dr�����^8{jf$�E~��X�1;�v�eGX63�X��b9{� �ґ(��?�(I"ޯ���g�3����_��K]�^
l���!����J4��|���&�����);7�v����I��'m�I�R0e
%M���(}�D+N�4\`�5��٘'��!�.ɷ�Q��oj_7C��Y�fh�f(��\XS�9��Y���B����ꥌ�&'��I�P�P"����t��^��ې*���`2���7t��A|'<��I��km�����S�7yMA�b��Ni��{�R��I�FK���\pQ���2~K�t����,i.΃nbj|2y���t�L��3�ܹo�G.������Ş�<�5���M��֘	@&O�SE�N-�A�L���.K�cQ�D��G4���
À [�OX�����N�ߜ��������˜��'�߽6���q����*U�x�K�
�%�e����N��E���c�A�7Ö�-\V�/�`�_��W	״*-o8IT�߀�Ln����	'zs[@Խ�4��fp�9�E�8�/~z���='{���)�tD�Tn��2�^�����c,��oy	:��"z-Z������=��5[���h[U��t���hr	���>��+��>c��zG����^;�]�c��i�i��g`��5D��������Nªa�'v�����Z�y�"�=FM{(7=d�9��y@�A.�p�.�o 5�*x��
���ң� �<=��у���	��#��=�䇒���H��+�UK����\s�G�7El�~W!�N��\��������G�n�Y�'��"���͇���2F*��7�� 5�����Pg�"52�I�>IL�K����kX�=K��LɤK�g�r.!��K�g�r.!/��_����^:&�LK�)��ɘB�"d� =�l�3,Q��d��gX�\q�%���ޢ��eLm�|�����b�"%�#c��1?��'�Y�����v���3�И�l~�?��-[�fۆ $����!��Qz@ACC����� ���Q� H��kJ���R,��S\p��������.XY=�]]�X�t��M�1t1t�bQ҅�����|Qh�-�y'��g�B
QGC�5ǐ"���.K���bH��~GRho�R�[,�?�>x"����ߢ������#���v�����b?N{��~)mJ��`-y��-^Ov�}ݚ+\�52��\~�H��T�'W����w�$`jۢTۺ�<��W-�?����]L���W��G���f�e��x�8`ZG�<�����N.o�Ge�9���p�{o��k�bٮ���4�� eh(�4����C���@$�� kh�=�7`�a"����]JY��>�V�.AO�<ǒ�Ie,�(�L�"ç���3��ƙ���HD�"�n7)ҦML.j���f�(� K���a�iG'�_&�a��%<��:7Y����da��2��mr9��{�_�������#�P��9E�O�&��1L�(%�d�༩�y��QT�5�c����8��mhE5��&�tK��ǔ�<�І9XDK�@+�d�j(�ʈsS&��Ydۡ��ܴ^?�q�g��$��^?�q���>�Nw��H`����[��6w����%�fgfG�s7gFo}�ͩo���c3�;W�#>(H��F�^Wu2��ma�0���}!|��l����/����Fʱ3�aÎAx_��g�~6wsr�t��T"�h��#�c8e���_��|r����h��T#��1�6�a�����xfؙ�O]�}��{3��\�3�����S����W'g?��?�Y���#W�Ϗ�ϝ}o��=�9�nvF���6�1�5�a�Ƨ�?��M_�hz��t�����F�
���O+��N��I>�f�E��`~/�(�e�+k�PĠq��A)C"Y{W$Q��Hؖ���ed��ݼ�<�t��_W�$U��2�Pl�z�R`l0�n�(Ԅ,`qf�*�_��� ��	Ӊ3���@̶�߁��6vjP'11A�7�%��%iI���i�.|����(%憳�5,ѝ%�p���̒����,���@�[����H�d]-|u��Á;A0[��H>�t�A"�A�yFD�ę����8��{��Ws� �ڠ�9C��T���p���������Mj�ӿ��Z��w>�킎���2<�9w�Y��'9I;� �
�2�v"A�>$��Ҹ0�����l�Fi�� x&ʃR܁%�A��@�z�YE�᭷<²���٘��j�f�^�����ԕ�S�����uaHNeYo_��Ա��O'�|�����hS6e���G����:n`V|!�1(T�X�� �Ơ �N��Q��ʓ����v7��_$��7�O_�5y(ʚ��Rg��WE18,]��PA���,�#�iR�ܙ`$,��H{�3:E�,BV�R'ܑ�?�����<�úz���O.G�y��(�7Q���BA�FV�u�|Q�����V*n��?��p*�
-96��أ�0vdZ�]�����Y����u�ZY��/e�Y�N���T!բjS�U6��l����L�e+������wgmC�i�<�IЄN���([-9:��T�=�X=K��]�dY���V�e�+|����]��m�z�h��@�o���,Xx���Arx�-�՚��~��b��d����I�h]����A~Gʢ�Ʌ�a�âkk�	ch.Y�,I�/Iv^}4,뻑����?���     