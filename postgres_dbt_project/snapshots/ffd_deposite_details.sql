{% snapshot ffd_deposit_details %}

{{
    config(
      target_schema='family_fin_details_scd2',
      unique_key='account_number',
      strategy='check',
      check_cols='all'
    )
}}

SELECT * FROM {{ source('family_fin_raw', 'raw_deposit_details') }}

{% endsnapshot %}