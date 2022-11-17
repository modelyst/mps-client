select
	process_detail.type,
	process_detail.technique,
	count(*)
from
	process_detail
group by
	process_detail.type,
	process_detail.technique
order by
	count(*) desc
