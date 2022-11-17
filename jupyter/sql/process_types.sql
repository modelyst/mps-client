select type, technique, count(*) from process_detail group by type, technique order by count(*) desc
