{% snapshot ffd_bank_details %}

{{
    config(
      target_schema='family_fin_details_scd2',
      unique_key='bank_id',
      strategy='check',
      check_cols='all'
    )
}}

SELECT * FROM {{ source('family_fin_raw', 'raw_bank_details') }}

{% endsnapshot %}