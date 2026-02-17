import hashlib
import threading

SEMANTIC_MAP_VERSION = "1.0.0"
SEMANTIC_MAP_AUTHOR = "E11 Semantic Team"
SEMANTIC_MAP_ENGINE = "E11_tenant_router"

SEMANTIC_MAP = {
    # Tenant
    "tenant": "tenant",
    "tenants": "tenant",
    "customer": "tenant",
    "client": "tenant",
    "organization": "tenant",
    "org": "tenant",
    "subscriber": "tenant",
    "account": "tenant",
    "user_group": "tenant",
    "usergroup": "tenant",
    "company": "tenant",
    "business_unit": "tenant",
    "bu": "tenant",
    "division": "tenant",
    "project": "tenant",
    "workspace": "tenant",
    "space": "tenant",
    "group": "tenant",
    "entity": "tenant",
    "partition": "tenant",
    "isolate": "tenant",
    "isolation": "tenant",
    "isolated": "tenant",
    "multi-tenant": "tenant",
    "multitenant": "tenant",
    "multi tenant": "tenant",
    "multi_tenant": "tenant",
    "tenant_id": "tenant_id",
    "tenantid": "tenant_id",
    "tenant identifier": "tenant_id",
    "tenant key": "tenant_id",
    "tenant_key": "tenant_id",
    "customer_id": "tenant_id",
    "client_id": "tenant_id",
    "org_id": "tenant_id",
    "organization_id": "tenant_id",
    "subscriber_id": "tenant_id",
    "account_id": "tenant_id",
    "workspace_id": "tenant_id",
    "space_id": "tenant_id",
    "group_id": "tenant_id",
    "partition_id": "tenant_id",
    "project_id": "tenant_id",
    "entity_id": "tenant_id",
    "bu_id": "tenant_id",
    "division_id": "tenant_id",
    "company_id": "tenant_id",
    "business_unit_id": "tenant_id",

    # Tenant Isolation
    "tenant isolation": "tenant_isolation",
    "isolation enforcement": "tenant_isolation",
    "isolate tenant": "tenant_isolation",
    "isolation policy": "tenant_isolation",
    "isolation policies": "tenant_isolation",
    "isolation enforcement": "tenant_isolation",
    "tenant boundary": "tenant_isolation",
    "boundary enforcement": "tenant_isolation",
    "segregation": "tenant_isolation",
    "segregate": "tenant_isolation",
    "tenant segregation": "tenant_isolation",
    "data isolation": "tenant_isolation",
    "data segregate": "tenant_isolation",
    "data segregation": "tenant_isolation",
    "cross-tenant isolation": "tenant_isolation",
    "cross tenant isolation": "tenant_isolation",
    "cross_tenant_isolation": "tenant_isolation",
    "cross-tenant boundary": "tenant_isolation",
    "cross_tenant_boundary": "tenant_isolation",
    "cross tenant boundary": "tenant_isolation",
    "isolation_level": "tenant_isolation",
    "isolation level": "tenant_isolation",
    "tenant_isolation": "tenant_isolation",
    "isolation_enforcement": "tenant_isolation",
    "enforce_isolation": "tenant_isolation",

    # Tenant-Specific Configuration
    "tenant configuration": "tenant_config",
    "tenant config": "tenant_config",
    "tenant-specific configuration": "tenant_config",
    "tenant specific configuration": "tenant_config",
    "tenant_config": "tenant_config",
    "tenant settings": "tenant_config",
    "tenant preferences": "tenant_config",
    "tenant setup": "tenant_config",
    "tenant setup config": "tenant_config",
    "tenant setup configuration": "tenant_config",
    "tenant profile": "tenant_config",
    "tenant_profile": "tenant_config",
    "tenant custom config": "tenant_config",
    "tenant custom configuration": "tenant_config",
    "tenant custom settings": "tenant_config",
    "tenant customization": "tenant_config",
    "tenant customizations": "tenant_config",
    "customer configuration": "tenant_config",
    "client configuration": "tenant_config",
    "org configuration": "tenant_config",
    "organization configuration": "tenant_config",
    "subscriber configuration": "tenant_config",
    "account configuration": "tenant_config",
    "workspace configuration": "tenant_config",
    "space configuration": "tenant_config",
    "group configuration": "tenant_config",
    "partition configuration": "tenant_config",
    "project configuration": "tenant_config",
    "entity configuration": "tenant_config",
    "bu configuration": "tenant_config",
    "division configuration": "tenant_config",
    "company configuration": "tenant_config",
    "business_unit_configuration": "tenant_config",
    "business unit configuration": "tenant_config",

    # Resource Quota Management
    "resource quota": "resource_quota",
    "quota": "resource_quota",
    "resource quotas": "resource_quota",
    "quota management": "resource_quota",
    "resource quota management": "resource_quota",
    "quota manager": "resource_quota",
    "quota enforcement": "resource_quota",
    "quota policy": "resource_quota",
    "quota policies": "resource_quota",
    "quota limit": "resource_quota",
    "quota limits": "resource_quota",
    "resource limit": "resource_quota",
    "resource limits": "resource_quota",
    "resource allocation": "resource_quota",
    "resource allocation policy": "resource_quota",
    "resource allocation policies": "resource_quota",
    "resource allocation manager": "resource_quota",
    "resource_quota": "resource_quota",
    "quota_enforcement": "resource_quota",
    "enforce_quota": "resource_quota",
    "quota_enforcer": "resource_quota",
    "quota_enforcers": "resource_quota",
    "quota_enforcement_policy": "resource_quota",
    "quota_enforcement_policies": "resource_quota",
    "quota_manager": "resource_quota",

    # Per-Tenant Rate Limiting
    "rate limit": "rate_limit",
    "rate limiting": "rate_limit",
    "ratelimit": "rate_limit",
    "rate limiter": "rate_limit",
    "rate limit enforcement": "rate_limit",
    "rate limit policy": "rate_limit",
    "rate limit policies": "rate_limit",
    "rate limit manager": "rate_limit",
    "rate limit configuration": "rate_limit",
    "rate limit config": "rate_limit",
    "rate_limit": "rate_limit",
    "ratelimiting": "rate_limit",
    "ratelimiter": "rate_limit",
    "ratelimit enforcement": "rate_limit",
    "ratelimit policy": "rate_limit",
    "ratelimit policies": "rate_limit",
    "ratelimit manager": "rate_limit",
    "ratelimit configuration": "rate_limit",
    "ratelimit config": "rate_limit",
    "per-tenant rate limit": "rate_limit",
    "per tenant rate limit": "rate_limit",
    "per_tenant_rate_limit": "rate_limit",
    "tenant rate limit": "rate_limit",
    "tenant ratelimit": "rate_limit",
    "tenant rate limiting": "rate_limit",
    "tenant ratelimiting": "rate_limit",
    "tenant rate limiter": "rate_limit",
    "tenant ratelimiter": "rate_limit",
    "tenant rate limit enforcement": "rate_limit",
    "tenant ratelimit enforcement": "rate_limit",
    "tenant rate limit policy": "rate_limit",
    "tenant ratelimit policy": "rate_limit",
    "tenant rate limit manager": "rate_limit",
    "tenant ratelimit manager": "rate_limit",

    # Tenant Onboarding Workflow
    "tenant onboarding": "tenant_onboarding",
    "onboarding": "tenant_onboarding",
    "onboard tenant": "tenant_onboarding",
    "tenant onboarding workflow": "tenant_onboarding",
    "onboarding workflow": "tenant_onboarding",
    "tenant onboarding process": "tenant_onboarding",
    "onboarding process": "tenant_onboarding",
    "tenant onboarding automation": "tenant_onboarding",
    "onboarding automation": "tenant_onboarding",
    "tenant onboarding flow": "tenant_onboarding",
    "onboarding flow": "tenant_onboarding",
    "tenant_onboarding": "tenant_onboarding",
    "onboarding_tenant": "tenant_onboarding",
    "onboard_tenant": "tenant_onboarding",
    "tenant_onboarding_workflow": "tenant_onboarding",
    "onboarding_workflow": "tenant_onboarding",
    "tenant_onboarding_process": "tenant_onboarding",
    "onboarding_process": "tenant_onboarding",
    "tenant_onboarding_automation": "tenant_onboarding",
    "onboarding_automation": "tenant_onboarding",
    "tenant_onboarding_flow": "tenant_onboarding",
    "onboarding_flow": "tenant_onboarding",
    "tenant_registration": "tenant_onboarding",
    "tenant_register": "tenant_onboarding",
    "register_tenant": "tenant_onboarding",
    "tenant_signup": "tenant_onboarding",
    "tenant sign up": "tenant_onboarding",
    "tenant sign-up": "tenant_onboarding",
    "tenant_sign_up": "tenant_onboarding",
    "tenant_sign-up": "tenant_onboarding",

    # Tenant Data Segregation
    "data segregation": "data_segregation",
    "data segregate": "data_segregation",
    "segregate data": "data_segregation",
    "tenant data segregation": "data_segregation",
    "tenant data segregate": "data_segregation",
    "tenant data isolation": "data_segregation",
    "tenant data": "data_segregation",
    "tenant_data": "data_segregation",
    "data_isolation": "data_segregation",
    "data isolation": "data_segregation",
    "data segregator": "data_segregation",
    "data segregators": "data_segregation",
    "data segregation policy": "data_segregation",
    "data segregation policies": "data_segregation",
    "data segregation enforcement": "data_segregation",
    "data segregation manager": "data_segregation",
    "data segregation configuration": "data_segregation",
    "data segregation config": "data_segregation",
    "data_segregation": "data_segregation",
    "segregation_policy": "data_segregation",
    "segregation_policies": "data_segregation",
    "segregation_enforcement": "data_segregation",
    "segregation_manager": "data_segregation",
    "segregation_configuration": "data_segregation",
    "segregation_config": "data_segregation",

    # Cross-Tenant Query Prevention
    "cross-tenant query": "cross_tenant_query_prevention",
    "cross tenant query": "cross_tenant_query_prevention",
    "cross_tenant_query": "cross_tenant_query_prevention",
    "cross-tenant queries": "cross_tenant_query_prevention",
    "cross tenant queries": "cross_tenant_query_prevention",
    "cross_tenant_queries": "cross_tenant_query_prevention",
    "cross-tenant query prevention": "cross_tenant_query_prevention",
    "cross tenant query prevention": "cross_tenant_query_prevention",
    "cross_tenant_query_prevention": "cross_tenant_query_prevention",
    "cross-tenant query block": "cross_tenant_query_prevention",
    "cross tenant query block": "cross_tenant_query_prevention",
    "cross_tenant_query_block": "cross_tenant_query_prevention",
    "cross-tenant query blocking": "cross_tenant_query_prevention",
    "cross tenant query blocking": "cross_tenant_query_prevention",
    "cross_tenant_query_blocking": "cross_tenant_query_prevention",
    "cross-tenant query restriction": "cross_tenant_query_prevention",
    "cross tenant query restriction": "cross_tenant_query_prevention",
    "cross_tenant_query_restriction": "cross_tenant_query_prevention",
    "cross-tenant query restrictions": "cross_tenant_query_prevention",
    "cross tenant query restrictions": "cross_tenant_query_prevention",
    "cross_tenant_query_restrictions": "cross_tenant_query_prevention",
    "cross-tenant query filter": "cross_tenant_query_prevention",
    "cross tenant query filter": "cross_tenant_query_prevention",
    "cross_tenant_query_filter": "cross_tenant_query_prevention",
    "cross-tenant query filters": "cross_tenant_query_prevention",
    "cross tenant query filters": "cross_tenant_query_prevention",
    "cross_tenant_query_filters": "cross_tenant_query_prevention",
    "cross-tenant query prevention policy": "cross_tenant_query_prevention",
    "cross tenant query prevention policy": "cross_tenant_query_prevention",
    "cross_tenant_query_prevention_policy": "cross_tenant_query_prevention",
    "cross-tenant query prevention policies": "cross_tenant_query_prevention",
    "cross tenant query prevention policies": "cross_tenant_query_prevention",
    "cross_tenant_query_prevention_policies": "cross_tenant_query_prevention",

    # Tenant Feature Flags
    "feature flag": "feature_flag",
    "feature flags": "feature_flag",
    "featureflag": "feature_flag",
    "featureflags": "feature_flag",
    "tenant feature flag": "feature_flag",
    "tenant feature flags": "feature_flag",
    "tenant_feature_flag": "feature_flag",
    "tenant_feature_flags": "feature_flag",
    "feature flag management": "feature_flag",
    "feature flag manager": "feature_flag",
    "feature flag enforcement": "feature_flag",
    "feature flag policy": "feature_flag",
    "feature flag policies": "feature_flag",
    "feature flag configuration": "feature_flag",
    "feature flag config": "feature_flag",
    "feature_flag": "feature_flag",
    "feature_flag_management": "feature_flag",
    "feature_flag_manager": "feature_flag",
    "feature_flag_enforcement": "feature_flag",
    "feature_flag_policy": "feature_flag",
    "feature_flag_policies": "feature_flag",
    "feature_flag_configuration": "feature_flag",
    "feature_flag_config": "feature_flag",
    "tenant feature flag management": "feature_flag",
    "tenant feature flag manager": "feature_flag",
    "tenant feature flag enforcement": "feature_flag",
    "tenant feature flag policy": "feature_flag",
    "tenant feature flag policies": "feature_flag",
    "tenant feature flag configuration": "feature_flag",
    "tenant feature flag config": "feature_flag",
    "tenant_feature_flag_management": "feature_flag",
    "tenant_feature_flag_manager": "feature_flag",
    "tenant_feature_flag_enforcement": "feature_flag",
    "tenant_feature_flag_policy": "feature_flag",
    "tenant_feature_flag_policies": "feature_flag",
    "tenant_feature_flag_configuration": "feature_flag",
    "tenant_feature_flag_config": "feature_flag",

    # Tenant Billing Metering
    "billing": "billing_metering",
    "metering": "billing_metering",
    "tenant billing": "billing_metering",
    "tenant metering": "billing_metering",
    "billing metering": "billing_metering",
    "billing_metering": "billing_metering",
    "tenant billing metering": "billing_metering",
    "tenant_billing_metering": "billing_metering",
    "billing management": "billing_metering",
    "billing manager": "billing_metering",
    "billing enforcement": "billing_metering",
    "billing policy": "billing_metering",
    "billing policies": "billing_metering",
    "billing configuration": "billing_metering",
    "billing config": "billing_metering",
    "metering management": "billing_metering",
    "metering manager": "billing_metering",
    "metering enforcement": "billing_metering",
    "metering policy": "billing_metering",
    "metering policies": "billing_metering",
    "metering configuration": "billing_metering",
    "metering config": "billing_metering",
    "tenant billing management": "billing_metering",
    "tenant billing manager": "billing_metering",
    "tenant billing enforcement": "billing_metering",
    "tenant billing policy": "billing_metering",
    "tenant billing policies": "billing_metering",
    "tenant billing configuration": "billing_metering",
    "tenant billing config": "billing_metering",
    "tenant metering management": "billing_metering",
    "tenant metering manager": "billing_metering",
    "tenant metering enforcement": "billing_metering",
    "tenant metering policy": "billing_metering",
    "tenant metering policies": "billing_metering",
    "tenant metering configuration": "billing_metering",
    "tenant metering config": "billing_metering",
    "tenant_billing_management": "billing_metering",
    "tenant_billing_manager": "billing_metering",
    "tenant_billing_enforcement": "billing_metering",
    "tenant_billing_policy": "billing_metering",
    "tenant_billing_policies": "billing_metering",
    "tenant_billing_configuration": "billing_metering",
    "tenant_billing_config": "billing_metering",
    "tenant_metering_management": "billing_metering",
    "tenant_metering_manager": "billing_metering",
    "tenant_metering_enforcement": "billing_metering",
    "tenant_metering_policy": "billing_metering",
    "tenant_metering_policies": "billing_metering",
    "tenant_metering_configuration": "billing_metering",
    "tenant_metering_config": "billing_metering",

    # Misspellings, abbreviations, acronyms, related terms
    "tennant": "tenant",
    "tenent": "tenant",
    "tennat": "tenant",
    "tenanat": "tenant",
    "tenent_id": "tenant_id",
    "tennant_id": "tenant_id",
    "tennat_id": "tenant_id",
    "tenanat_id": "tenant_id",
    "cust_id": "tenant_id",
    "cli_id": "tenant_id",
    "orgid": "tenant_id",
    "acct_id": "tenant_id",
    "ws_id": "tenant_id",
    "grp_id": "tenant_id",
    "part_id": "tenant_id",
    "proj_id": "tenant_id",
    "ent_id": "tenant_id",
    "buid": "tenant_id",
    "divid": "tenant_id",
    "compid": "tenant_id",
    "bu_id": "tenant_id",
    "div_id": "tenant_id",
    "comp_id": "tenant_id",
    "bizunit_id": "tenant_id",
    "biz_unit_id": "tenant_id",
    "bizunit": "tenant",
    "biz_unit": "tenant",
    "bizunit configuration": "tenant_config",
    "biz_unit configuration": "tenant_config",

    # More synonyms and related terms
    "multi-tenancy": "multi_tenancy",
    "multitenancy": "multi_tenancy",
    "multi tenancy": "multi_tenancy",
    "multi_tenancy": "multi_tenancy",
    "multi-tenancy architecture": "multi_tenancy",
    "multitenancy architecture": "multi_tenancy",
    "multi tenancy architecture": "multi_tenancy",
    "multi_tenancy_architecture": "multi_tenancy",
    "tenant architecture": "multi_tenancy",
    "tenant_architecture": "multi_tenancy",
    "tenant router": "tenant_router",
    "tenant_router": "tenant_router",
    "tenant routing": "tenant_router",
    "tenant route": "tenant_router",
    "tenant routes": "tenant_router",
    "tenant routing engine": "tenant_router",
    "tenant routing manager": "tenant_router",
    "tenant routing policy": "tenant_router",
    "tenant routing configuration": "tenant_router",
    "tenant routing config": "tenant_router",
    "tenant routing enforcement": "tenant_router",
    "tenant routing workflow": "tenant_router",
    "tenant routing process": "tenant_router",
    "tenant routing automation": "tenant_router",
    "tenant routing flow": "tenant_router",
    "tenant routing feature": "tenant_router",
    "tenant routing features": "tenant_router",
    "tenant routing metering": "tenant_router",
    "tenant routing billing": "tenant_router",
    "tenant routing quota": "tenant_router",
    "tenant routing rate limit": "tenant_router",
    "tenant routing rate limiting": "tenant_router",
    "tenant routing isolation": "tenant_router",
    "tenant routing segregation": "tenant_router",
    "tenant routing cross-tenant query prevention": "tenant_router",
    "tenant routing feature flag": "tenant_router",
    "tenant routing feature flags": "tenant_router",
    "tenant routing onboarding": "tenant_router",
    "tenant routing onboarding workflow": "tenant_router",
    "tenant routing onboarding process": "tenant_router",
    "tenant routing onboarding automation": "tenant_router",
    "tenant routing onboarding flow": "tenant_router",
    "tenant routing onboarding feature": "tenant_router",
    "tenant routing onboarding features": "tenant_router",
    "tenant routing onboarding metering": "tenant_router",
    "tenant routing onboarding billing": "tenant_router",
    "tenant routing onboarding quota": "tenant_router",
    "tenant routing onboarding rate limit": "tenant_router",
    "tenant routing onboarding rate limiting": "tenant_router",
    "tenant routing onboarding isolation": "tenant_router",
    "tenant routing onboarding segregation": "tenant_router",
    "tenant routing onboarding cross-tenant query prevention": "tenant_router",
    "tenant routing onboarding feature flag": "tenant_router",
    "tenant routing onboarding feature flags": "tenant_router",

    # Additional related terms for completeness
    "tenant policy": "tenant_policy",
    "tenant policies": "tenant_policy",
    "tenant_policy": "tenant_policy",
    "tenant management": "tenant_management",
    "tenant manager": "tenant_management",
    "tenant_management": "tenant_management",
    "tenant admin": "tenant_management",
    "tenant administrator": "tenant_management",
    "tenant administration": "tenant_management",
    "tenant_admin": "tenant_management",
    "tenant_administrator": "tenant_management",
    "tenant_administration": "tenant_management",
    "tenant lifecycle": "tenant_management",
    "tenant_lifecycle": "tenant_management",
    "tenant lifecycle management": "tenant_management",
    "tenant_lifecycle_management": "tenant_management",
    "tenant provisioning": "tenant_management",
    "tenant_provisioning": "tenant_management",
    "tenant deprovisioning": "tenant_management",
    "tenant_deprovisioning": "tenant_management",
    "tenant deletion": "tenant_management",
    "tenant_deletion": "tenant_management",
    "tenant removal": "tenant_management",
    "tenant_removal": "tenant_management",
    "tenant update": "tenant_management",
    "tenant_update": "tenant_management",
    "tenant upgrade": "tenant_management",
    "tenant_upgrade": "tenant_management",
    "tenant downgrade": "tenant_management",
    "tenant_downgrade": "tenant_management",
    "tenant migration": "tenant_management",
    "tenant_migration": "tenant_management",
    "tenant transfer": "tenant_management",
    "tenant_transfer": "tenant_management",
    "tenant import": "tenant_management",
    "tenant_import": "tenant_management",
    "tenant export": "tenant_management",
    "tenant_export": "tenant_management",
    "tenant sync": "tenant_management",
    "tenant_sync": "tenant_management",
    "tenant synchronization": "tenant_management",
    "tenant_synchronization": "tenant_management",

    # Misspellings and abbreviations for management
    "tennant management": "tenant_management",
    "tenent management": "tenant_management",
    "tennat management": "tenant_management",
    "tenanat management": "tenant_management",
    "tennant manager": "tenant_management",
    "tenent manager": "tenant_management",
    "tennat manager": "tenant_management",
    "tenanat manager": "tenant_management",
    "tenant adminstrator": "tenant_management",
    "tenant administrater": "tenant_management",
    "tenant administrater": "tenant_management",
    "tenant administratior": "tenant_management",
    "tenant administrater": "tenant_management",
    "tenant administrater": "tenant_management",
    "tenant administratior": "tenant_management",
    "tenant administrater": "tenant_management",
    "tenant administrater": "tenant_management",
    "tenant administratior": "tenant_management",
    "tenant administrater": "tenant_management",
    "tenant administrater": "tenant_management",
    "tenant administratior": "tenant_management",

    # More cross-tenant terms
    "cross tenant": "cross_tenant",
    "cross-tenant": "cross_tenant",
    "cross_tenant": "cross_tenant",
    "cross tenant access": "cross_tenant_access",
    "cross-tenant access": "cross_tenant_access",
    "cross_tenant_access": "cross_tenant_access",
    "cross tenant data": "cross_tenant_data",
    "cross-tenant data": "cross_tenant_data",
    "cross_tenant_data": "cross_tenant_data",
    "cross tenant policy": "cross_tenant_policy",
    "cross-tenant policy": "cross_tenant_policy",
    "cross_tenant_policy": "cross_tenant_policy",
    "cross tenant management": "cross_tenant_management",
    "cross-tenant management": "cross_tenant_management",
    "cross_tenant_management": "cross_tenant_management",

    # More abbreviations and misspellings
    "mnt": "multi_tenancy",
    "mt": "multi_tenancy",
    "mt_arch": "multi_tenancy",
    "mt_architecture": "multi_tenancy",
    "mt_router": "tenant_router",
    "mt_routing": "tenant_router",
    "mt_config": "tenant_config",
    "mt_quota": "resource_quota",
    "mt_limit": "resource_quota",
    "mt_rate_limit": "rate_limit",
    "mt_onboarding": "tenant_onboarding",
    "mt_segregation": "data_segregation",
    "mt_cross_query": "cross_tenant_query_prevention",
    "mt_feature_flag": "feature_flag",
    "mt_billing": "billing_metering",
    "mt_metering": "billing_metering",
    "mt_policy": "tenant_policy",
    "mt_management": "tenant_management",

    # More synonyms for isolation, config, quota, etc.
    "partitioning": "tenant_isolation",
    "partition enforcement": "tenant_isolation",
    "partition policies": "tenant_isolation",
    "partition policy": "tenant_isolation",
    "partition manager": "tenant_isolation",
    "partition configuration": "tenant_isolation",
    "partition config": "tenant_isolation",
    "partition enforcement policy": "tenant_isolation",
    "partition enforcement policies": "tenant_isolation",
    "partitioning policy": "tenant_isolation",
    "partitioning policies": "tenant_isolation",
    "partitioning enforcement": "tenant_isolation",
    "partitioning manager": "tenant_isolation",
    "partitioning configuration": "tenant_isolation",
    "partitioning config": "tenant_isolation",

    # More synonyms for onboarding
    "registration": "tenant_onboarding",
    "register": "tenant_onboarding",
    "signup": "tenant_onboarding",
    "sign up": "tenant_onboarding",
    "sign-up": "tenant_onboarding",
    "sign_up": "tenant_onboarding",

    # More synonyms for feature flag
    "toggle": "feature_flag",
    "toggles": "feature_flag",
    "feature toggle": "feature_flag",
    "feature toggles": "feature_flag",
    "feature_toggle": "feature_flag",
    "feature_toggles": "feature_flag",
    "tenant feature toggle": "feature_flag",
    "tenant feature toggles": "feature_flag",
    "tenant_feature_toggle": "feature_flag",
    "tenant_feature_toggles": "feature_flag",

    # More synonyms for billing/metering
    "charge": "billing_metering",
    "charges": "billing_metering",
    "charging": "billing_metering",
    "invoice": "billing_metering",
    "invoices": "billing_metering",
    "invoicing": "billing_metering",
    "payment": "billing_metering",
    "payments": "billing_metering",
    "pay": "billing_metering",
    "meter": "billing_metering",
    "meters": "billing_metering",
    "metered": "billing_metering",
    "metering policy": "billing_metering",
    "metering policies": "billing_metering",
    "metering manager": "billing_metering",
    "metering configuration": "billing_metering",
    "metering config": "billing_metering",

    # More synonyms for quota
    "allocation": "resource_quota",
    "allocations": "resource_quota",
    "allocate": "resource_quota",
    "allocated": "resource_quota",
    "allocation policy": "resource_quota",
    "allocation policies": "resource_quota",
    "allocation manager": "resource_quota",
    "allocation configuration": "resource_quota",
    "allocation config": "resource_quota",

    # More synonyms for rate limit
    "throttle": "rate_limit",
    "throttling": "rate_limit",
    "throttler": "rate_limit",
    "throttle policy": "rate_limit",
    "throttle policies": "rate_limit",
    "throttle manager": "rate_limit",
    "throttle configuration": "rate_limit",
    "throttle config": "rate_limit",
    "tenant throttle": "rate_limit",
    "tenant throttling": "rate_limit",
    "tenant throttler": "rate_limit",
    "tenant throttle policy": "rate_limit",
    "tenant throttle policies": "rate_limit",
    "tenant throttle manager": "rate_limit",
    "tenant throttle configuration": "rate_limit",
    "tenant throttle config": "rate_limit",

    # More synonyms for cross-tenant query prevention
    "cross query": "cross_tenant_query_prevention",
    "cross-query": "cross_tenant_query_prevention",
    "cross_query": "cross_tenant_query_prevention",
    "cross query prevention": "cross_tenant_query_prevention",
    "cross-query prevention": "cross_tenant_query_prevention",
    "cross_query_prevention": "cross_tenant_query_prevention",
    "cross query block": "cross_tenant_query_prevention",
    "cross-query block": "cross_tenant_query_prevention",
    "cross_query_block": "cross_tenant_query_prevention",
    "cross query blocking": "cross_tenant_query_prevention",
    "cross-query blocking": "cross_tenant_query_prevention",
    "cross_query_blocking": "cross_tenant_query_prevention",
    "cross query restriction": "cross_tenant_query_prevention",
    "cross-query restriction": "cross_tenant_query_prevention",
    "cross_query_restriction": "cross_tenant_query_prevention",
    "cross query restrictions": "cross_tenant_query_prevention",
    "cross-query restrictions": "cross_tenant_query_prevention",
    "cross_query_restrictions": "cross_tenant_query_prevention",
    "cross query filter": "cross_tenant_query_prevention",
    "cross-query filter": "cross_tenant_query_prevention",
    "cross_query_filter": "cross_tenant_query_prevention",
    "cross query filters": "cross_tenant_query_prevention",
    "cross-query filters": "cross_tenant_query_prevention",
    "cross_query_filters": "cross_tenant_query_prevention",
    "cross query prevention policy": "cross_tenant_query_prevention",
    "cross-query prevention policy": "cross_tenant_query_prevention",
    "cross_query_prevention_policy": "cross_tenant_query_prevention",
    "cross query prevention policies": "cross_tenant_query_prevention",
    "cross-query prevention policies": "cross_tenant_query_prevention",
    "cross_query_prevention_policies": "cross_tenant_query_prevention",

    # More synonyms for data segregation
    "segregation": "data_segregation",
    "segregate": "data_segregation",
    "segregator": "data_segregation",
    "segregators": "data_segregation",
    "segregation policy": "data_segregation",
    "segregation policies": "data_segregation",
    "segregation enforcement": "data_segregation",
    "segregation manager": "data_segregation",
    "segregation configuration": "data_segregation",
    "segregation config": "data_segregation",
}

_EXPECTED_ENTRY_COUNT = len(SEMANTIC_MAP)

def _compute_map_hash():
    items = sorted(SEMANTIC_MAP.items())
    concat = "".join(f"{k}:{v}" for k, v in items)
    return hashlib.sha256(concat.encode("utf-8")).hexdigest()

_MAP_INTEGRITY_HASH = _compute_map_hash()

_integrity_lock = threading.Lock()

def verify_integrity():
    with _integrity_lock:
        current_hash = _compute_map_hash()
        is_valid = current_hash == _MAP_INTEGRITY_HASH
        return {
            "status": "ok" if is_valid else "corrupt",
            "entries": len(SEMANTIC_MAP),
            "hash": current_hash,
            "is_valid": is_valid
        }

def normalize_term(term: str) -> str:
    t = term.strip().lower().replace("-", " ").replace("_", " ")
    t = " ".join(t.split())
    # Try direct match
    if term in SEMANTIC_MAP:
        return SEMANTIC_MAP[term]
    if t in SEMANTIC_MAP:
        return SEMANTIC_MAP[t]
    # Try normalized forms
    t1 = t.replace(" ", "_")
    if t1 in SEMANTIC_MAP:
        return SEMANTIC_MAP[t1]
    t2 = t.replace(" ", "")
    if t2 in SEMANTIC_MAP:
        return SEMANTIC_MAP[t2]
    t3 = t.replace("_", "")
    if t3 in SEMANTIC_MAP:
        return SEMANTIC_MAP[t3]
    # Try plural/singular
    if t.endswith("s") and t[:-1] in SEMANTIC_MAP:
        return SEMANTIC_MAP[t[:-1]]
    if t.endswith("es") and t[:-2] in SEMANTIC_MAP:
        return SEMANTIC_MAP[t[:-2]]
    # Try removing "tenant" prefix/suffix
    if t.startswith("tenant ") and t[7:] in SEMANTIC_MAP:
        return SEMANTIC_MAP[t[7:]]
    if t.endswith(" tenant") and t[:-7] in SEMANTIC_MAP:
        return SEMANTIC_MAP[t[:-7]]
    # Try removing "cross tenant" prefix
    if t.startswith("cross tenant ") and t[13:] in SEMANTIC_MAP:
        return SEMANTIC_MAP[t[13:]]
    # Try removing "multi tenant" prefix
    if t.startswith("multi tenant ") and t[13:] in SEMANTIC_MAP:
        return SEMANTIC_MAP[t[13:]]
    # Try removing "mt_" prefix
    if t.startswith("mt ") and t[3:] in SEMANTIC_MAP:
        return SEMANTIC_MAP[t[3:]]
    if t.startswith("mt_") and t[3:] in SEMANTIC_MAP:
        return SEMANTIC_MAP[t[3:]]
    # Try removing "tenant_" prefix
    if t.startswith("tenant_") and t[7:] in SEMANTIC_MAP:
        return SEMANTIC_MAP[t[7:]]
    # Try removing "tenant " prefix
    if t.startswith("tenant ") and t[7:] in SEMANTIC_MAP:
        return SEMANTIC_MAP[t[7:]]
    # Try removing "tenant" suffix
    if t.endswith("_tenant") and t[:-7] in SEMANTIC_MAP:
        return SEMANTIC_MAP[t[:-7]]
    if t.endswith(" tenant") and t[:-7] in SEMANTIC_MAP:
        return SEMANTIC_MAP[t[:-7]]
    # Try removing "cross_tenant_" prefix
    if t.startswith("cross_tenant_") and t[14:] in SEMANTIC_MAP:
        return SEMANTIC_MAP[t[14:]]
    # Try removing "cross_tenant" prefix
    if t.startswith("cross_tenant") and t[13:] in SEMANTIC_MAP:
        return SEMANTIC_MAP[t[13:]]
    # Try removing "cross-tenant " prefix
    if t.startswith("cross-tenant ") and t[13:] in SEMANTIC_MAP:
        return SEMANTIC_MAP[t[13:]]
    # Try removing "cross-tenant" prefix
    if t.startswith("cross-tenant") and t[12:] in SEMANTIC_MAP:
        return SEMANTIC_MAP[t[12:]]
    # Try removing "multi_tenant_" prefix
    if t.startswith("multi_tenant_") and t[13:] in SEMANTIC_MAP:
        return SEMANTIC_MAP[t[13:]]
    # Try removing "multi_tenant" prefix
    if t.startswith("multi_tenant") and t[12:] in SEMANTIC_MAP:
        return SEMANTIC_MAP[t[12:]]
    # Try removing "multi-tenant " prefix
    if t.startswith("multi-tenant ") and t[13:] in SEMANTIC_MAP:
        return SEMANTIC_MAP[t[13:]]
    # Try removing "multi-tenant" prefix
    if t.startswith("multi-tenant") and t[12:] in SEMANTIC_MAP:
        return SEMANTIC_MAP[t[12:]]
    return t

def get_related_terms(term: str) -> list:
    normalized = normalize_term(term)
    related = []
    for k, v in SEMANTIC_MAP.items():
        if v == normalized and k != term:
            related.append(k)
    return related

def get_all_mappings() -> dict:
    return dict(SEMANTIC_MAP)