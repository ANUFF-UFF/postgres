create table usuario(
    id serial PRIMARY KEY,
    email text not null unique,
    senha char(32) not null,
    nome text,
    reputacao real
);

create function create_usuario(e text, s text, n text default null)
returns int as $$
declare novo_id int;
begin
    INSERT INTO usuario (email, senha, nome) VALUES
    (e, md5(s), n) returning id into novo_id;

    return novo_id;
end;
$$ language plpgsql;

create table chat(
    id serial primary key,
    usuario_1_id serial not null references usuario(id),
    usuario_2_id serial not null references usuario(id),
    criado_em timestamp default current_timestamp
);

create table mensagem(
    id serial primary key,
    chat_id serial not null references chat(id),
    remetente_id serial not null references usuario(id),
    conteudo text not null,
    enviada_em timestamp default current_timestamp
);

create table anuncio(
    id serial primary key,
    autor serial not null references usuario(id),
    titulo text not null,
    descricao text,
    preco decimal(9, 2),
    criado_em timestamp default current_timestamp
);

create table avaliacao(
    id serial PRIMARY KEY,
    nota int not null,
    comentario text,
    criada_em timestamp default current_timestamp,
    autor serial not null references usuario(id),
    anuncio serial not null references anuncio(id),
    unique(autor, anuncio)
);


    
