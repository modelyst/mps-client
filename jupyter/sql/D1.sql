select
	s.type,
	s.label,
	(coalesce(a.output->>'I.A_ave', '0'))::numeric fom
from
	analysis a
join process_data_analysis pda on
	pda.analysis_id = a.id
join process_data pd on
	pda.process_data_id = pd.id
join sample_process_process_data sppd on
	sppd.process_data_id = pd.id
join sample_process sp on
	sppd.sample_process_id = sp.id
join sample s on
	sp.sample_id = s.id
where
	name = 'CA_FOMS_standard'
order by
	fom desc
limit 10
