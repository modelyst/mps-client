select
	process_detail.type,
	count(*)
from
	process_detail
	join process on process.process_detail_id = process_detail.id
group by
	process_detail.type
order by
	count(*) desc
