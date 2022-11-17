select
analysis.name,
count(distinct sample_process.sample_id) as n_samples_undergone
from sample_process
join sample_process_process_data on sample_process_process_data.sample_process_id = sample_process.id
join process_data on sample_process_process_data.process_data_id = process_data.id
join process_data_analysis on process_data_analysis.process_data_id = process_data.id
join analysis on process_data_analysis.analysis_id = analysis.id
group by analysis.name
order by count(distinct sample_process.sample_id) desc
