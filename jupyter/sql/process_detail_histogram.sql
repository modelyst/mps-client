select
process_detail.id, process_detail.type, process_detail.technique, count(*)
from process join process_detail on process.process_detail_id = process_detail.id
group by process_detail.id, process_detail.type, process_detail.technique
order by count(*) desc
