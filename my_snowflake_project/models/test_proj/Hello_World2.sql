{{config(materialized='table')}}

with mock_data as (
    select 1 as ID,
    'Hello_World' as Message,
    current_date() as Created_At

    UNION ALL

    select 2 as ID,
    'Welcome to DBT Projects' as Message,
    current_date() as Created_At
)

select * from mock_data