create table if not exists human_dna (
	id uuid,
	dna_sequence_size integer not null,
	dna_sequence varchar not null,
	is_mutant boolean not null,
	primary key(id)
);

create table if not exists human_dna_statistics (
	count_mutant_dna integer not null,
	count_human_dna integer not null,
	ratio numeric(5, 4) not null
);

insert into human_dna_statistics values (0, 0, 0);
