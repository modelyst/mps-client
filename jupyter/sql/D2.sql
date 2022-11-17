-- set search_path = 'development';

select
	c.label plate,
	max(coalesce(a.output->>'I.A_ave', '0')::numeric) fom
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
join collection__sample cs on
	cs.sample_id = s.id
join collection c on
	cs.collection_id = c.id
where
	name = 'CA_FOMS_standard'
	and c.type='JCAP_plate'
group by
	c.label
