select
	name,
	count(*)
from
	analysis a
group by
	name
order by
	count(*) desc
