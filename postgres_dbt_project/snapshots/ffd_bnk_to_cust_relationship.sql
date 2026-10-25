{% snapshot ffd_bnk_to_cust_relationship %}

{{
    config(
      target_schema='family_fin_details_scd2',
      unique_key='cif_number',
      strategy='check',
      check_cols='all'
    )
}}

SELECT * FROM {{ source('family_fin_raw', 'raw_bnk_to_cust_relationship') }}

{% endsnapshot %}