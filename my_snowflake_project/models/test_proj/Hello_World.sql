
{{config(materialized='table')}}

with mock_data as (
    select 1 as ID,
    'Hello World' as Greeting,
    current_date() as Created_At
    
    union all

    select 2 as ID,
    'Welcome to DBT Projects' as Greeting,
    current_date() as Created_At
    
)

select * from mock_data