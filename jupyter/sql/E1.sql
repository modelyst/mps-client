select
	sample.label,
	process_detail.type,
	process_detail.technique,
	process.timestamp
from
	sample
join sample_process on
	sample_process.sample_id = sample.id
join process on
	sample_process.process_id = process.id
join process_detail on
	process.process_detail_id = process_detail.id
where
	sample.id = (
	select
		id
	from
		sample
	limit 1)
order by process.timestamp
