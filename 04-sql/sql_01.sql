-- CREATE TABLE BILLBOARD
create table public."Billboard" (
	"rank" int4 NULL,
	song varchar(300) NULL,
	artist varchar(300) NULL,
	"last-week" int4 NULL,
	"peak-rank" int4 NULL,
	"weeks-on-board" int4 NULL,
	"date" date NULL
);

select count(*) as quantidade
from public."Billboard"
limit 100;