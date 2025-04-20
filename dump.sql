--
-- PostgreSQL database dump
--

-- Dumped from database version 16.8 (Ubuntu 16.8-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.8 (Ubuntu 16.8-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: exercese; Type: TABLE; Schema: public; Owner: maksim
--

CREATE TABLE public.exercese (
    exercese_id integer NOT NULL,
    type_id integer,
    trening_id integer
);


ALTER TABLE public.exercese OWNER TO maksim;

--
-- Name: exercese_exercese_id_seq; Type: SEQUENCE; Schema: public; Owner: maksim
--

ALTER TABLE public.exercese ALTER COLUMN exercese_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.exercese_exercese_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: exercese_type; Type: TABLE; Schema: public; Owner: maksim
--

CREATE TABLE public.exercese_type (
    type_id integer NOT NULL,
    name character varying(256),
    description text
);


ALTER TABLE public.exercese_type OWNER TO maksim;

--
-- Name: exercese_type_type_id_seq; Type: SEQUENCE; Schema: public; Owner: maksim
--

ALTER TABLE public.exercese_type ALTER COLUMN type_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.exercese_type_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: repetition; Type: TABLE; Schema: public; Owner: maksim
--

CREATE TABLE public.repetition (
    repetition_id integer NOT NULL,
    exercese_id integer,
    amount integer NOT NULL,
    extra_weight double precision
);


ALTER TABLE public.repetition OWNER TO maksim;

--
-- Name: repetition_repetition_id_seq; Type: SEQUENCE; Schema: public; Owner: maksim
--

ALTER TABLE public.repetition ALTER COLUMN repetition_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.repetition_repetition_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: trening; Type: TABLE; Schema: public; Owner: maksim
--

CREATE TABLE public.trening (
    trening_id integer NOT NULL,
    update_time timestamp without time zone,
    user_name character varying(256)
);


ALTER TABLE public.trening OWNER TO maksim;

--
-- Name: trening_trening_id_seq; Type: SEQUENCE; Schema: public; Owner: maksim
--

ALTER TABLE public.trening ALTER COLUMN trening_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.trening_trening_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: maksim
--

CREATE TABLE public.users (
    user_name character varying(256),
    password character varying(256)
);


ALTER TABLE public.users OWNER TO maksim;

--
-- Data for Name: exercese; Type: TABLE DATA; Schema: public; Owner: maksim
--

COPY public.exercese (exercese_id, type_id, trening_id) FROM stdin;
488	1	134
489	1	135
490	2	136
491	3	137
492	1	138
493	1	139
494	1	140
495	2	141
496	2	142
497	2	143
498	2	144
499	2	145
500	2	146
501	2	147
502	2	148
503	4	149
504	9	150
505	2	151
506	9	152
507	2	153
508	1	154
509	1	155
510	2	156
511	11	157
512	11	158
513	10	159
514	11	160
515	2	161
\.


--
-- Data for Name: exercese_type; Type: TABLE DATA; Schema: public; Owner: maksim
--

COPY public.exercese_type (type_id, name, description) FROM stdin;
1	Push-ups	Classic bodyweight exercise
2	Squats	Lower body strength exercise
3	Pull-ups	Upper body pulling exercise
4	Deadlift	Compound weightlifting exercise
9	Basic Glute Bridge	Lie on your back with knees bent, feet flat on the floor. Lift your hips by squeezing your glutes, then lower back down.
10	Seated Leg Abduction	 Push your legs outward against the resistance, then slowly return to the starting position. This targets the outer thighs and glutes.
11	Donkey Kickback	This targets the glutes and hamstrings.
12	The bars	Push-ups on a bars
13	1	2
\.


--
-- Data for Name: repetition; Type: TABLE DATA; Schema: public; Owner: maksim
--

COPY public.repetition (repetition_id, exercese_id, amount, extra_weight) FROM stdin;
491	488	10	0
492	488	10	0
493	488	10	0
494	489	10	0
495	489	10	0
496	489	10	0
497	490	50	0
498	490	50	0
499	490	50	10
500	491	12	-35
501	492	10	-10
502	493	10	-10
503	494	10	-10
504	495	10	-33
505	496	10	-33
506	497	10	-33
507	498	10	-33
508	499	10	-33
509	501	10	-33
510	502	10	-33
511	502	12	12
512	503	12	12
513	503	21	21
514	504	12	13
515	504	21	312
516	506	12	13
517	507	12	12
518	508	12	12
519	508	13	13
520	509	12	12
521	509	13	13
522	510	33	33
523	510	34	34
524	512	12	21
525	512	22	22
526	512	23	23
527	513	11	11
528	513	12	12
529	513	13	13
530	514	12	21
531	514	22	22
532	514	23	23
533	515	10	12
\.


--
-- Data for Name: trening; Type: TABLE DATA; Schema: public; Owner: maksim
--

COPY public.trening (trening_id, update_time, user_name) FROM stdin;
134	2025-02-16 00:00:00	Maksim
135	2025-02-16 00:00:00	Maksim
136	2025-02-16 00:00:00	Maksim
137	2025-03-21 00:00:00	Nastusha
138	2025-03-21 00:00:00	Maksim
139	2025-03-21 00:00:00	Maksim
140	2025-03-21 00:00:00	Maksim
141	2025-03-21 00:00:00	Maksim
142	2025-03-21 00:00:00	Maksim
143	2025-03-21 00:00:00	Maksim
144	2025-03-21 00:00:00	Maksim
145	2025-03-21 00:00:00	Maksim
146	2025-03-21 00:00:00	Maksim
147	2025-03-21 00:00:00	Maksim
148	2025-03-21 00:00:00	Maksim
149	2025-03-21 00:00:00	Maksim
150	2025-03-21 00:00:00	Maksim
151	2025-03-21 00:00:00	Maksim
152	2025-03-21 00:00:00	Maksim
153	2025-03-21 00:00:00	Maksim
154	2025-03-10 00:00:00	Maksim
155	2025-03-10 00:00:00	Maksim
156	2025-03-10 00:00:00	Maksim
157	2025-03-10 00:00:00	Maksim
158	2025-03-10 00:00:00	Maksim
159	2025-03-10 00:00:00	Maksim
160	2025-03-10 00:00:00	Maksim
161	2025-04-09 00:00:00	Maksim
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: maksim
--

COPY public.users (user_name, password) FROM stdin;
Maksim	$2b$12$q.r86J7glqdb1mOZ4AZtDunEewqzEmu.wlk7gzepdOP80uw2VNSme
Nastusha	$2b$12$lGd4EizzWVeweleVXicMs.TjlfUiO42GuwkSFLL133oxgfju06oAa
\.


--
-- Name: exercese_exercese_id_seq; Type: SEQUENCE SET; Schema: public; Owner: maksim
--

SELECT pg_catalog.setval('public.exercese_exercese_id_seq', 515, true);


--
-- Name: exercese_type_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: maksim
--

SELECT pg_catalog.setval('public.exercese_type_type_id_seq', 13, true);


--
-- Name: repetition_repetition_id_seq; Type: SEQUENCE SET; Schema: public; Owner: maksim
--

SELECT pg_catalog.setval('public.repetition_repetition_id_seq', 533, true);


--
-- Name: trening_trening_id_seq; Type: SEQUENCE SET; Schema: public; Owner: maksim
--

SELECT pg_catalog.setval('public.trening_trening_id_seq', 161, true);


--
-- Name: exercese exercese_pkey; Type: CONSTRAINT; Schema: public; Owner: maksim
--

ALTER TABLE ONLY public.exercese
    ADD CONSTRAINT exercese_pkey PRIMARY KEY (exercese_id);


--
-- Name: exercese_type exercese_type_pkey; Type: CONSTRAINT; Schema: public; Owner: maksim
--

ALTER TABLE ONLY public.exercese_type
    ADD CONSTRAINT exercese_type_pkey PRIMARY KEY (type_id);


--
-- Name: repetition repetition_pkey; Type: CONSTRAINT; Schema: public; Owner: maksim
--

ALTER TABLE ONLY public.repetition
    ADD CONSTRAINT repetition_pkey PRIMARY KEY (repetition_id);


--
-- Name: trening trening_pkey; Type: CONSTRAINT; Schema: public; Owner: maksim
--

ALTER TABLE ONLY public.trening
    ADD CONSTRAINT trening_pkey PRIMARY KEY (trening_id);


--
-- Name: users users_user_name_key; Type: CONSTRAINT; Schema: public; Owner: maksim
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_user_name_key UNIQUE (user_name);


--
-- Name: exercese exercese_trening_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: maksim
--

ALTER TABLE ONLY public.exercese
    ADD CONSTRAINT exercese_trening_id_fkey FOREIGN KEY (trening_id) REFERENCES public.trening(trening_id);


--
-- Name: exercese exercese_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: maksim
--

ALTER TABLE ONLY public.exercese
    ADD CONSTRAINT exercese_type_id_fkey FOREIGN KEY (type_id) REFERENCES public.exercese_type(type_id);


--
-- Name: trening fk_user_name; Type: FK CONSTRAINT; Schema: public; Owner: maksim
--

ALTER TABLE ONLY public.trening
    ADD CONSTRAINT fk_user_name FOREIGN KEY (user_name) REFERENCES public.users(user_name);


--
-- Name: repetition repetition_exercese_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: maksim
--

ALTER TABLE ONLY public.repetition
    ADD CONSTRAINT repetition_exercese_id_fkey FOREIGN KEY (exercese_id) REFERENCES public.exercese(exercese_id);


--
-- PostgreSQL database dump complete
--

