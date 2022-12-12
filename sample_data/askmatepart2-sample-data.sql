--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

ALTER TABLE IF EXISTS ONLY public.question DROP CONSTRAINT IF EXISTS pk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS pk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS pk_comment_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS pk_question_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.tag DROP CONSTRAINT IF EXISTS pk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_tag_id CASCADE;

DROP TABLE IF EXISTS public.question;
CREATE TABLE question (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    view_number integer,
    vote_number integer,
    title text,
    message text,
    image text
);

DROP TABLE IF EXISTS public.answer;
CREATE TABLE answer (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    vote_number integer,
    question_id integer,
    username text,
    message text,
    image text
);

DROP TABLE IF EXISTS public.comment;
CREATE TABLE comment (
    id serial NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    edited_count integer
);


DROP TABLE IF EXISTS public.question_tag;
CREATE TABLE question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);

DROP TABLE IF EXISTS public.tag;
CREATE TABLE tag (
    id serial NOT NULL,
    name text
);


ALTER TABLE ONLY answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);

ALTER TABLE ONLY question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);

ALTER TABLE ONLY tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES answer(id) ON DELETE CASCADE;

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE;

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE;

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE;

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES tag(id) ON DELETE CASCADE;

INSERT INTO question VALUES (0, '2022-11-28 08:29:00', 29, 7, 'How to make lists in Python?', 'I am totally new to this, any hints?', NULL);
INSERT INTO question VALUES (1, '2022-11-29 09:19:00', 15, 9, 'Wordpress loading multiple jQuery Versions', 'I developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $(".myBook").booklet();

I could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine.

BUT in my theme i also using jquery via webpack so the loading order is now following:

jquery
booklet
app.js (bundled file with webpack, including jquery)', 'question_1.jpeg');
INSERT INTO question VALUES (2, '2022-11-29 10:41:00', 1364, 57, 'Drawing canvas with an image picked with Cordova Camera Plugin', 'I''m getting an image from device and drawing a canvas with filters using Pixi JS. It works all well using computer to get an image. But when I''m on IOS, it throws errors such as cross origin issue, or that I''m trying to use an unknown format.
', NULL);
INSERT INTO question VALUES (3, '2022-11-30 15:13:00', 77, 11, 'Compose dynamic SQL string with psycopg2', 'In psycopg2 version 2.7 there''s the new sql module to do this string composition in a way that''s safe against SQL injection. I don''t know how to properly construct it.', NULL);
INSERT INTO question VALUES (4, '2022-11-30 18:11:00', 13, 2, 'How to remove items from a list while iterating?', 'I''m iterating over a list of tuples in Python, and am attempting to remove them if they meet certain criteria.', NULL);
INSERT INTO question VALUES (5, '2022-11-30 23:01:00', 101, 11, 'How do I compare strings in Java?', 'How do I compare strings in Java?', NULL);
INSERT INTO question VALUES (6, '2022-12-01 07:45:00', 613, 44, 'How do I split a list into equally-sized chunks?', 'How do I split a list into equally-sized chunks?', NULL);
INSERT INTO question VALUES (7, '2022-12-01 08:30:00', 905, 61, 'How can I horizontally center an element?', 'How can I horizontally center a <div> within another <div> using CSS?', 'question_7.png');
INSERT INTO question VALUES (8, '2022-12-01 10:59:00', 44, 15, 'How can I validate an email address in JavaScript?', 'I''d like to check if the user input is an email address in JavaScript, before sending it to a server or attempting to send an email to it, to prevent the most basic mistyping. How could I achieve this?', NULL);
INSERT INTO question VALUES (9, '2022-12-01 14:33:00', 29, 3, 'Insert text with single quotes in PostgreSQL', 'I need to insert values like: insert into test values (1,''user''s log''); If there is any method to do this correctly please share.', NULL);
SELECT pg_catalog.setval('question_id_seq', 9, true);

INSERT INTO answer VALUES (1, '2022-11-28 16:49:00', 4, 1, 'Bob', 'You need to use brackets: my_list = []', NULL);
INSERT INTO answer VALUES (2, '2022-11-29 14:42:00', 35, 1, 'Dave', 'Look it up in the Python docs', NULL);
INSERT INTO answer VALUES (3, '2022-11-30 18:11:00', 12, 3, 'Kaaz', 'You can use psycopg2.sql.Identifier to interpolate an identifier to a query.', NULL);
INSERT INTO answer VALUES (4, '2022-11-30 23:50:00', 7, 5, 'Ian', '== tests object references, .equals() tests the string values.', 'answer_4.png');
INSERT INTO answer VALUES (5, '2022-12-01 01:13:00', 0, 3, 'Rarity', 'Yes.', 'answer_5.jpg');
INSERT INTO answer VALUES (6, '2022-12-01 01:14:00', 0, 5, 'Applejuice', 'I don''t know, but here''s a picture of an apple:', 'answer_6.png');
INSERT INTO answer VALUES (7, '2022-12-01 07:50:00', 1, 6, 'Rob', 'noob', NULL);
INSERT INTO answer VALUES (8, '2022-12-01 07:55:00', 21, 6, 'Jessica', 'The simplest is this list comprehension one-liner: [lst[i:i + n] for i in range(0, len(lst), n)]', NULL);
INSERT INTO answer VALUES (9, '2022-12-01 08:31:00', 100, 7, 'Adam', 'The margin: 0 auto is what does the actual centering. You can apply this CSS to the inner <div>:', 'answer_9.png');
INSERT INTO answer VALUES (10, '2022-12-01 08:45:00', 80, 7, 'Evelyn', 'You can make the inner div into an inline element that can be centered with text-align like this:', 'answer_10.png');
INSERT INTO answer VALUES (11, '2022-12-01 08:50:00', 32, 7, 'Kat', 'It''s very easy to style the div horizontally and vertically centered with flexbox. Just add display: flex and justify-content: center; to #outer <div>.', NULL);
INSERT INTO answer VALUES (12, '2022-12-01 11:20:00', 0, 8, 'Guest', 'i''d like to know it too :(', NULL);
INSERT INTO answer VALUES (13, '2022-12-01 11:58:00', 2, 8, 'Martin', 'Using regular expressions is probably the best way.', NULL);
INSERT INTO answer VALUES (14, '2022-12-01 12:01:00', 0, 7, 'Rarity', 'Answer', NULL);
INSERT INTO answer VALUES (15, '2022-12-01 12:03:00', 1, 8, 'Mark', 'The only way to be absolutely, positively sure that what the user entered is in fact an email is to actually send an email and see what happens. Other than that it''s all just guesses.', NULL);
INSERT INTO answer VALUES (16, '2022-12-01 14:57:00', 9, 9, 'Peter', 'You can escape single quotes by doubling them up, this will work: ''user''''s log''', NULL);
INSERT INTO answer VALUES (17, '2022-12-01 15:03:00', 7, 9, 'James', 'If you have to deal with many single quotes or multiple layers of escaping, you can avoid quoting hell in PostgreSQL with dollar-quoted strings.', NULL);
INSERT INTO answer VALUES (18, '2022-12-01 17:26:00', 2, 9, 'Carl', 'look it up in the postgres docs', NULL);
SELECT pg_catalog.setval('answer_id_seq', 18, true);

INSERT INTO comment VALUES (1, 0, NULL, 'Please clarify the question as it is too vague!', '2022-11-28 08:49:00', 0);
INSERT INTO comment VALUES (2, 1, 1, 'I think you could use my_list = list() as well.', '2022-11-28 16:55:00', 0);
INSERT INTO comment VALUES (3, 3, NULL, 'Never, never, NEVER use Python string concatenation (+) or string parameters interpolation (%) to pass variables to a SQL query string. Not even at gunpoint.', '2022-11-30 16:13:00', 1);
INSERT INTO comment VALUES (4, 7, 10, 'I like this solution.', '2022-12-01 09:10:00', 1);
INSERT INTO comment VALUES (5, 8, NULL, 'let''s be realistic: you would not be using JavaScript to confirm whether an e-mail is authentic', '2022-12-01 11:58:00', 0);
INSERT INTO comment VALUES (6, 9, 16, 'Thanks, this worked!', '2022-12-01 15:15:00', 0);
INSERT INTO comment VALUES (7, 2, NULL, 'Fixed it, don''t worry', '2022-12-01 18:16:00', 0);
SELECT pg_catalog.setval('comment_id_seq', 7, true);

INSERT INTO tag VALUES (1, 'python');
INSERT INTO tag VALUES (2, 'sql');
INSERT INTO tag VALUES (3, 'css');
INSERT INTO tag VALUES (4, 'java');
INSERT INTO tag VALUES (5, 'javascript');
SELECT pg_catalog.setval('tag_id_seq', 5, true);

INSERT INTO question_tag VALUES (0, 1);
INSERT INTO question_tag VALUES (1, 3);
INSERT INTO question_tag VALUES (2, 3);
INSERT INTO question_tag VALUES (3, 2);
INSERT INTO question_tag VALUES (4, 1);
INSERT INTO question_tag VALUES (5, 4);
INSERT INTO question_tag VALUES (6, 1);
INSERT INTO question_tag VALUES (7, 3);
INSERT INTO question_tag VALUES (8, 5);
INSERT INTO question_tag VALUES (9, 2);