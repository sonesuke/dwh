{{
    config(
        materialized='table'
    )
}}

with source_data as (
    select
        "Id",
        "Name",
        "Email",
        "Department",
        "Title",
        "CreatedDate"
    from salesforce.contact
    where "IsDeleted" = false
    union all
    select
        "Id",
        "Name",
        "Email",
        null,
        "Title",
        "CreatedDate"
    from salesforce.lead
    where "IsDeleted" = false and
          "IsConverted" = false
)

select source_data."Id"         as salesforce_id,
       source_data."Name"       as name,
       -- source_data."Email"      as email,
       source_data."Department" as department,
       source_data."Title"      as title,
       {{ dbt_utils.surrogate_key('source_data."Id"', 'source_data."Email"', 'source_data."Name"') }} as id
from source_data


