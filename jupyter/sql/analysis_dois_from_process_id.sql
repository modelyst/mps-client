select
    p.id as process_id,
    ja.doi as analysis_doi
from
    process p
join process_run pr on
    pr.process_id = p.id
join jcap_run jr on
    pr.jcap_run_id = jr.id
join jcap_experiment_run jer on
    jer.jcap_run_id = jr.id
join jcap_experiment je on
    jer.jcap_experiment_id = je.id
join jcap_analysis ja on
    ja.jcap_experiment_id = je.id
