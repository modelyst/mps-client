select
process_detail.type,
process_detail.technique,
count(distinct sample_process.sample_id) as n_samples_undergone
from sample_process
join process on sample_process.process_id = process.id
join process_detail on process.process_detail_id = process_detail.id
group by
process_detail.type,
process_detail.technique
order by count(distinct sample_process.sample_id) desc
