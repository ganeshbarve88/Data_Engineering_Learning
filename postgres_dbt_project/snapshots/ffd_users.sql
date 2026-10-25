{% snapshot ffd_users %}

{{
    config(
      target_schema='family_fin_details_scd2',
      unique_key='userid',
      strategy='check',
      check_cols='all'
    )
}}

SELECT * FROM {{ source('family_fin_raw', 'raw_users') }}

{% endsnapshot %}