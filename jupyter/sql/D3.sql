select
	s.label,
	a1.output->>'composition' composition,
	coalesce(a2.output->>'I.A_ave', '0')::numeric fom
from
	sample s
join sample_process sp1 on
	sp1.sample_id = s.id
join sample_process_process_data sppd1 on
	sppd1.sample_process_id = sp1.id
join process_data pd1 on
	sppd1.process_data_id = pd1.id
join process_data_analysis pda1 on
	pda1.process_data_id = pd1.id
join analysis a1 on
	pda1.analysis_id = a1.id
join sample_process sp2 on
	sp2.sample_id = s.id
join sample_process_process_data sppd2 on
	sppd2.sample_process_id = sp2.id
join process_data pd2 on
	sppd2.process_data_id = pd2.id
join process_data_analysis pda2 on
	pda2.process_data_id = pd2.id
join analysis a2 on
	pda2.analysis_id = a2.id
where
	a1.name = 'xrfs_loadings_to_compositions'
	and a2.name = 'CA_FOMS_standard'
