select
	collection.type,
	collection.label,
	count(*)
from
	collection
join collection__sample on
	collection__sample.collection_id = collection.id
group by
	collection.type,
	collection.label
order by
	count(*) desc;
