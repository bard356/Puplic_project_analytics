--Задание - составить рейтинг топ-3 менеджеров по количеству звонков в каждом офисе за январь 2021
/* Данные в таблицах: call_log и user_log.
call_log содержит данные по звонкам со следующими полями:
• DT – дата звонка в формате «ДД.ММ.ГГГГ чч:мм:сс»
• OPERATOR_ID – id менеджера
user_log содержит информацию по сотрудникам:
• ID – id менеджера
• NAME – имя менеджера
• OFFICE – офис работы менеджера*/


--Запрос: 

with t as (
	select 
		user_log.office,
		user_log.name as manager,
		count(call_log.dt) as cnt_calls
	from call_log
	left join user_log on user_log.id=call_log.operator_id
	where trunc(call_log.dt,'dd')>='01.01.2021' and trunc(call_log.dt,'dd')< '01.02.2021'
	group by 
		user_log.office,
		user_log.name
	),
t2 as (
 select 
	office,
	row_number() over(partition by office
      		order by cnt_calls desc) as rating,
	manager,
	cnt_calls
 from t 
	)
select 
  office,
  rating,
  manager,
  cnt_calls
from t2
where rating <=3