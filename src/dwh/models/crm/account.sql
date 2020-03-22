{{
    config(
        materialized='table'
    )
}}

with source_data as (
    select "Id",
           "Name",
           "BillingPostalCode",
           "BillingState",
           "BillingCity",
           "BillingStreet",
           "CreatedDate"
    from salesforce.account
    where "IsDeleted" = false
    union all
    select distinct min("Id"),
                    "Company",
                    "PostalCode",
                    "State",
                    "City",
                    "Street",
                    min("CreatedDate")
    from salesforce.lead
    where "IsDeleted" = false
      and "IsConverted" = false
    group by
        "Company",
        "PostalCode",
        "State",
        "City",
        "Street"
)

select source_data."Id"                as salesforce_id,
       source_data."Name"              as name,
       source_data."BillingPostalCode" as postal_code,
       source_data."BillingState"      as state,
       source_data."BillingCity"       as city,
    {{ dbt_utils.surrogate_key('source_data."Id"', 'source_data."BillingPostalCode"', 'source_data."BillingState"') }} as id
from source_data


