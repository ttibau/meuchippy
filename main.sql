-- Id, Usuário, texto_do_tweet, data_hora

DROP TABLE tweets;

CREATE TABLE tweets (
  id SERIAL,
  usuario VARCHAR(100) NOT NULL,
  texto VARCHAR(150) NOT NULL,
  data TIMESTAMP NOT NULL,
  id_tweet VARCHAR(100) NOT NULL
)
