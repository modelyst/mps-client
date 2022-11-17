select
	count(*)
from
	(
	select
		count(*)
	from
		collection__sample
	group by
		collection__sample.sample_id
	having
		count(*) > 1) as temp;
