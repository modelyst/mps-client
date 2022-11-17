select
	ad.id,
	ad.name,
	count(*)
from
	analysis a
join analysis_details ad on
	a.analysis_detail_id = ad.id
group by
	ad.id,
	ad.name
having
	count(*) > 1
order by
	count(*) desc
