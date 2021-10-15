-- SELECT ORIGINAL
select
	t1."date",
	t1."rank",
	t1.song,
	t1.artist,
	t1."last-week",
	t1."peak-rank",
	t1."weeks-on-board"
from public."Billboard" as t1
limit 10;

-- Query buscar a primeira  vez que os artistas entraram
with cte_dedup_artist as (
	select
		t1."date"
		,t1."rank"
		,t1.artist
		,row_number() over(partition by artist order by artist, "date") as dedup
	from public."Billboard" as t1
	order by t1.artist, t1."date"
) 
select 
	t1."date"
	,t1."rank"
	,t1.artist
from cte_dedup_artist as t1
where t1.dedup = 1;

-- Criar uma tabela baseada nessa query
create table tb_web_site as (
	with cte_dedup_artist as (
		select
			t1."date"
			,t1."rank"
			,t1.artist
			,row_number() over(partition by artist order by artist, "date") as dedup
		from public."Billboard" as t1
		order by t1.artist, t1."date"
	) 
	select 
		t1."date"
		,t1."rank"
		,t1.artist
	from cte_dedup_artist as t1
	where t1.dedup = 1
);

-- Selecionando a tabela nova
select * from public.tb_web_site;

-- Imaginando que a tabela atualize como podemos atualizar a tb_web_site
-- Podemos criar uma view
create table tb_artist as (
	select
		t1."date"
		,t1."rank"
		,t1.artist
		,t1.song
	from public."Billboard" as t1
	where t1.artist = 'AC/DC'
	order by t1.artist, t1.song, t1."date"
);

drop table public.tb_artist;

select * from public.tb_artist;

-- Criar uma tabela baseada nessa query
create view vw_artist as (
with cte_dedup_artist as (
	select
		t1."date"
		,t1."rank"
		,t1.artist
		,row_number() over(partition by artist order by artist, "date") as dedup
	from public.tb_artist as t1
	order by t1.artist, t1."date"
) 
select 
	t1."date"
	,t1."rank"
	,t1.artist
from cte_dedup_artist as t1
where t1.dedup = 1
);

select * from vw_artist;

-- Adicionando outros artistas na tabela tb_artist
insert into tb_artist (
	select
		t1."date"
		,t1."rank"
		,t1.artist
		,t1.song
	from public."Billboard" as t1
	where t1.artist like 'Elvis%'
	order by t1.artist, t1.song, t1."date"
);

select * from vw_artist;

-- Criando a view song
create view vw_song as (
with cte_dedup_artist as (
	select
		t1."date"
		,t1."rank"
		,t1.artist
		,t1.song
		,row_number() over(partition by artist, song order by artist, song, "date") as dedup
	from public.tb_artist as t1
	order by t1.artist, t1.song, t1."date"
) 
select 
	t1."date"
	,t1."rank"
	,t1.artist
	,t1.song
from cte_dedup_artist as t1
where t1.dedup = 1
);

select * from vw_song; 


-- Adicionando outros artistas na tabela tb_artist
insert into tb_artist (
	select
		t1."date"
		,t1."rank"
		,t1.artist
		,t1.song
	from public."Billboard" as t1
	where t1.artist like 'Adele%'
	order by t1.artist, t1.song, t1."date"
);

select * from vw_artist;
select * from vw_song; 

-- Alterando a view song removendo o artista
drop view vw_song;
create or replace view vw_song as (
with cte_dedup_artist as (
	select
		t1."date"
		,t1."rank"
		,t1.song
		,row_number() over(partition by song order by song, "date") as dedup
	from public.tb_artist as t1
	order by t1.song, t1."date"
) 
select 
	t1."date"
	,t1."rank"
	,t1.song
from cte_dedup_artist as t1
where t1.dedup = 1
);

select * from vw_song; 


