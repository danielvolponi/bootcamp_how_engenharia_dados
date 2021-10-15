-- Selecionando apenas artistas e musicas
select 
	t1.artist,	
	t1.song
from public."Billboard" as t1;

-- Selecionando apenas artistas e musicas ordenados
select distinct 
	t1.artist,	
	t1.song
from public."Billboard" as t1
order by 
	t1.artist, 
	t1.song;
	
-- Selecionando a quantidade de vezes que cada artista aparece
select
	t1.artist,	
	count(*) as qtd_artist
from public."Billboard" as t1
group by t1.artist 
order by qtd_artist desc;

-- Selecionando a quantidade de vezes que cada musica aparece
select
	t1.song,	
	count(*) as qtd_song
from public."Billboard" as t1
group by t1.song 
order by qtd_song desc;

-- Juntando o resultado destas queries
SELECT DISTINCT t1.artist
	,t2.qtd_artist
	,t1.song
	,t3.qtd_song
FROM PUBLIC."Billboard" AS t1
LEFT JOIN (
	SELECT t1.artist
		,count(*) AS qtd_artist
	FROM PUBLIC."Billboard" AS t1
	GROUP BY t1.artist
	ORDER BY qtd_artist DESC
	) AS t2 ON (t1.artist = t2.artist)
LEFT JOIN (
	SELECT t1.song
		,count(*) AS qtd_song
	FROM PUBLIC."Billboard" AS t1
	GROUP BY t1.song
	ORDER BY qtd_song DESC
	) AS t3 ON (t1.song = t3.song)
ORDER BY t1.artist
	,t1.song;


-- Simplificando a query anterior
with cte_artist as (
	SELECT t1.artist
		,count(*) AS qtd_artist
	FROM PUBLIC."Billboard" AS t1
	GROUP BY t1.artist
	ORDER BY qtd_artist DESC
),
cte_song as (
	SELECT t1.song
		,count(*) AS qtd_song
	FROM PUBLIC."Billboard" AS t1
	GROUP BY t1.song
	ORDER BY qtd_song DESC
)
SELECT DISTINCT t1.artist
	,t2.qtd_artist
	,t1.song
	,t3.qtd_song
FROM PUBLIC."Billboard" AS t1
LEFT JOIN cte_artist AS t2 ON (t1.artist = t2.artist)
LEFT JOIN cte_song AS t3 ON (t1.song = t3.song)
ORDER BY t1.artist
	,t1.song;

-- Window Function
with cte_billboard as (
	select distinct 
		t1.artist,	
		t1.song
	from public."Billboard" as t1
)
select *
	,row_number() over (order by artist, song) as "row_number"
	,row_number() over (partition by artist order by artist, song) as "row_number_artist"
from cte_billboard;

-- Filtrando com a Window Function
with cte_billboard as (
	select distinct 
		t1.artist,	
		t1.song
		,row_number() over (order by artist, song) as "row_number"
		,row_number() over (partition by artist order by artist, song) as "row_number_artist"
	from public."Billboard" as t1
	order by 
		t1.artist
		,t1.song
)
select *
from cte_billboard
where "row_number_artist" = 1;

-- Filtrando com a Window Function
with cte_billboard as (
	select distinct 
		t1.artist,	
		t1.song
	from public."Billboard" as t1
	order by 
		t1.artist
		,t1.song
)
select *
	,row_number() over (order by artist, song) as "row_number"
	,row_number() over (partition by artist order by artist, song) as "row_number_artist"
	,rank() over (partition by artist order by artist,song) as "rank"
	,lag(song, 1) over (partition by artist order by artist,song) as "lag_song" 
	,lead(song, 1) over (partition by artist order by artist,song) as "lead_song"
	,first_value(song) over (partition by artist order by artist,song) as "first_song"
from cte_billboard;







