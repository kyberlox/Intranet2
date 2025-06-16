-- Представление с новыми пользоваетлями
CREATE VIEW NewUsers AS
 SELECT users.id,
    users.active,
    users.last_name,
    users.name,
    users.second_name,
    to_date(users.indirect_data ->> 'date_register'::text, 'YYYY-MM-DD'::text) AS dat,
    users.indirect_data,
    users.photo_file_id
   FROM users
  WHERE users.active = true AND to_date(users.indirect_data ->> 'date_register'::text, 'YYYY-MM-DD'::text) >= (date_trunc('week'::text, CURRENT_DATE::timestamp with time zone) - '14 days'::interval)
  ORDER BY (to_date(users.indirect_data ->> 'date_register'::text, 'YYYY-MM-DD'::text));
