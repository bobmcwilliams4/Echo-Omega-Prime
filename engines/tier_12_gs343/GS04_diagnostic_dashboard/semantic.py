import hashlib
import json
from typing import Dict, List, Any

SEMANTIC_MAP_VERSION = "1.0.0"
SEMANTIC_MAP_AUTHOR = "GS04_diagnostic_dashboard_team"
SEMANTIC_MAP_ENGINE = "GS04"

SEMANTIC_MAP: Dict[str, Dict[str, Any]] = {
    # Dashboard Data Aggregation Patterns
    "dashboard data aggregation": {"norm": "dashboard_data_aggregation", "related": ["aggregation pattern", "dashboard aggregation", "data summarization", "dashboard aggregation pattern"]},
    "aggregation pattern": {"norm": "dashboard_data_aggregation", "related": ["dashboard data aggregation", "dashboard aggregation"]},
    "dashboard aggregation": {"norm": "dashboard_data_aggregation", "related": ["dashboard data aggregation", "aggregation pattern"]},
    "data summarization": {"norm": "dashboard_data_aggregation", "related": ["dashboard data aggregation"]},
    "dashboard aggregation pattern": {"norm": "dashboard_data_aggregation", "related": ["dashboard data aggregation"]},
    "agg pattern": {"norm": "dashboard_data_aggregation", "related": ["aggregation pattern"]},
    "agg. pattern": {"norm": "dashboard_data_aggregation", "related": ["aggregation pattern"]},
    "aggregation": {"norm": "dashboard_data_aggregation", "related": ["dashboard data aggregation"]},
    "agg": {"norm": "dashboard_data_aggregation", "related": ["aggregation"]},
    "summarization": {"norm": "dashboard_data_aggregation", "related": ["data summarization"]},
    "summarize": {"norm": "dashboard_data_aggregation", "related": ["data summarization"]},
    "summary": {"norm": "dashboard_data_aggregation", "related": ["data summarization"]},

    # System Health Score Weighted Composite
    "system health score": {"norm": "system_health_score_weighted_composite", "related": ["health score", "weighted health score", "composite health score", "system health composite"]},
    "health score": {"norm": "system_health_score_weighted_composite", "related": ["system health score"]},
    "weighted health score": {"norm": "system_health_score_weighted_composite", "related": ["system health score"]},
    "composite health score": {"norm": "system_health_score_weighted_composite", "related": ["system health score"]},
    "system health composite": {"norm": "system_health_score_weighted_composite", "related": ["system health score"]},
    "sys health score": {"norm": "system_health_score_weighted_composite", "related": ["system health score"]},
    "sys health": {"norm": "system_health_score_weighted_composite", "related": ["system health score"]},
    "shs": {"norm": "system_health_score_weighted_composite", "related": ["system health score"]},
    "weighted composite": {"norm": "system_health_score_weighted_composite", "related": ["system health score"]},
    "health composite": {"norm": "system_health_score_weighted_composite", "related": ["system health score"]},
    "composite score": {"norm": "system_health_score_weighted_composite", "related": ["system health score"]},

    # Engine Status Matrix
    "engine status matrix": {"norm": "engine_status_matrix", "related": ["status matrix", "engine matrix", "engine status", "status grid"]},
    "status matrix": {"norm": "engine_status_matrix", "related": ["engine status matrix"]},
    "engine matrix": {"norm": "engine_status_matrix", "related": ["engine status matrix"]},
    "engine status": {"norm": "engine_status_matrix", "related": ["engine status matrix"]},
    "status grid": {"norm": "engine_status_matrix", "related": ["engine status matrix"]},
    "esm": {"norm": "engine_status_matrix", "related": ["engine status matrix"]},
    "eng status matrix": {"norm": "engine_status_matrix", "related": ["engine status matrix"]},
    "eng status": {"norm": "engine_status_matrix", "related": ["engine status matrix"]},
    "engine grid": {"norm": "engine_status_matrix", "related": ["engine status matrix"]},
    "matrix": {"norm": "engine_status_matrix", "related": ["engine status matrix"]},

    # Error Rate Trending
    "error rate trending": {"norm": "error_rate_trending", "related": ["error trending", "error rate trend", "error trend", "error rate", "error trends"]},
    "error trending": {"norm": "error_rate_trending", "related": ["error rate trending"]},
    "error rate trend": {"norm": "error_rate_trending", "related": ["error rate trending"]},
    "error trend": {"norm": "error_rate_trending", "related": ["error rate trending"]},
    "error rate": {"norm": "error_rate_trending", "related": ["error rate trending"]},
    "error trends": {"norm": "error_rate_trending", "related": ["error rate trending"]},
    "ert": {"norm": "error_rate_trending", "related": ["error rate trending"]},
    "err rate": {"norm": "error_rate_trending", "related": ["error rate trending"]},
    "err trending": {"norm": "error_rate_trending", "related": ["error rate trending"]},
    "err trend": {"norm": "error_rate_trending", "related": ["error rate trending"]},
    "err trends": {"norm": "error_rate_trending", "related": ["error rate trending"]},

    # Recovery Success Metrics
    "recovery success metrics": {"norm": "recovery_success_metrics", "related": ["recovery metrics", "success metrics", "recovery success", "recovery rate", "recovery success rate"]},
    "recovery metrics": {"norm": "recovery_success_metrics", "related": ["recovery success metrics"]},
    "success metrics": {"norm": "recovery_success_metrics", "related": ["recovery success metrics"]},
    "recovery success": {"norm": "recovery_success_metrics", "related": ["recovery success metrics"]},
    "recovery rate": {"norm": "recovery_success_metrics", "related": ["recovery success metrics"]},
    "recovery success rate": {"norm": "recovery_success_metrics", "related": ["recovery success metrics"]},
    "rsm": {"norm": "recovery_success_metrics", "related": ["recovery success metrics"]},
    "recov success": {"norm": "recovery_success_metrics", "related": ["recovery success metrics"]},
    "recov metrics": {"norm": "recovery_success_metrics", "related": ["recovery success metrics"]},
    "recov rate": {"norm": "recovery_success_metrics", "related": ["recovery success metrics"]},

    # Drift Severity Dashboard
    "drift severity dashboard": {"norm": "drift_severity_dashboard", "related": ["drift dashboard", "severity dashboard", "drift severity", "drift monitor"]},
    "drift dashboard": {"norm": "drift_severity_dashboard", "related": ["drift severity dashboard"]},
    "severity dashboard": {"norm": "drift_severity_dashboard", "related": ["drift severity dashboard"]},
    "drift severity": {"norm": "drift_severity_dashboard", "related": ["drift severity dashboard"]},
    "drift monitor": {"norm": "drift_severity_dashboard", "related": ["drift severity dashboard"]},
    "dsd": {"norm": "drift_severity_dashboard", "related": ["drift severity dashboard"]},
    "drift dash": {"norm": "drift_severity_dashboard", "related": ["drift severity dashboard"]},
    "drift sev": {"norm": "drift_severity_dashboard", "related": ["drift severity dashboard"]},
    "drift severity dash": {"norm": "drift_severity_dashboard", "related": ["drift severity dashboard"]},
    "drift sev dash": {"norm": "drift_severity_dashboard", "related": ["drift severity dashboard"]},

    # Alert Management: Acknowledge, Snooze, Escalate
    "alert management": {"norm": "alert_management", "related": ["alert acknowledge", "alert snooze", "alert escalate", "alert actions", "alert handling"]},
    "alert acknowledge": {"norm": "alert_acknowledge", "related": ["acknowledge alert", "ack alert", "alert management"]},
    "acknowledge alert": {"norm": "alert_acknowledge", "related": ["alert acknowledge"]},
    "ack alert": {"norm": "alert_acknowledge", "related": ["alert acknowledge"]},
    "alert snooze": {"norm": "alert_snooze", "related": ["snooze alert", "snooze", "alert management"]},
    "snooze alert": {"norm": "alert_snooze", "related": ["alert snooze"]},
    "snooze": {"norm": "alert_snooze", "related": ["alert snooze"]},
    "alert escalate": {"norm": "alert_escalate", "related": ["escalate alert", "escalate", "alert management"]},
    "escalate alert": {"norm": "alert_escalate", "related": ["alert escalate"]},
    "escalate": {"norm": "alert_escalate", "related": ["alert escalate"]},
    "alert actions": {"norm": "alert_management", "related": ["alert management"]},
    "alert handling": {"norm": "alert_management", "related": ["alert management"]},
    "alert ack": {"norm": "alert_acknowledge", "related": ["alert acknowledge"]},
    "alert snz": {"norm": "alert_snooze", "related": ["alert snooze"]},
    "alert esc": {"norm": "alert_escalate", "related": ["alert escalate"]},

    # Dashboard Refresh Strategies
    "dashboard refresh strategies": {"norm": "dashboard_refresh_strategies", "related": ["refresh strategies", "dashboard refresh", "refresh policy", "refresh interval"]},
    "refresh strategies": {"norm": "dashboard_refresh_strategies", "related": ["dashboard refresh strategies"]},
    "dashboard refresh": {"norm": "dashboard_refresh_strategies", "related": ["dashboard refresh strategies"]},
    "refresh policy": {"norm": "dashboard_refresh_strategies", "related": ["dashboard refresh strategies"]},
    "refresh interval": {"norm": "dashboard_refresh_strategies", "related": ["dashboard refresh strategies"]},
    "refresh strat": {"norm": "dashboard_refresh_strategies", "related": ["dashboard refresh strategies"]},
    "dash refresh": {"norm": "dashboard_refresh_strategies", "related": ["dashboard refresh strategies"]},
    "dash refresh strat": {"norm": "dashboard_refresh_strategies", "related": ["dashboard refresh strategies"]},
    "drs": {"norm": "dashboard_refresh_strategies", "related": ["dashboard refresh strategies"]},

    # Real-Time vs Batch Metrics
    "real-time metrics": {"norm": "real_time_metrics", "related": ["realtime metrics", "real time metrics", "batch metrics", "metrics batch", "metrics realtime"]},
    "realtime metrics": {"norm": "real_time_metrics", "related": ["real-time metrics"]},
    "real time metrics": {"norm": "real_time_metrics", "related": ["real-time metrics"]},
    "batch metrics": {"norm": "batch_metrics", "related": ["metrics batch", "real-time metrics"]},
    "metrics batch": {"norm": "batch_metrics", "related": ["batch metrics"]},
    "metrics realtime": {"norm": "real_time_metrics", "related": ["real-time metrics"]},
    "rt metrics": {"norm": "real_time_metrics", "related": ["real-time metrics"]},
    "rtm": {"norm": "real_time_metrics", "related": ["real-time metrics"]},
    "bm": {"norm": "batch_metrics", "related": ["batch metrics"]},
    "batch": {"norm": "batch_metrics", "related": ["batch metrics"]},
    "realtime": {"norm": "real_time_metrics", "related": ["real-time metrics"]},

    # Metric Retention Policies
    "metric retention policies": {"norm": "metric_retention_policies", "related": ["retention policy", "metric retention", "metrics retention", "data retention"]},
    "retention policy": {"norm": "metric_retention_policies", "related": ["metric retention policies"]},
    "metric retention": {"norm": "metric_retention_policies", "related": ["metric retention policies"]},
    "metrics retention": {"norm": "metric_retention_policies", "related": ["metric retention policies"]},
    "data retention": {"norm": "metric_retention_policies", "related": ["metric retention policies"]},
    "retention": {"norm": "metric_retention_policies", "related": ["metric retention policies"]},
    "mrp": {"norm": "metric_retention_policies", "related": ["metric retention policies"]},
    "ret policy": {"norm": "metric_retention_policies", "related": ["retention policy"]},

    # Dashboard Access Control
    "dashboard access control": {"norm": "dashboard_access_control", "related": ["access control", "dashboard acl", "dashboard permissions", "dashboard roles"]},
    "access control": {"norm": "dashboard_access_control", "related": ["dashboard access control"]},
    "dashboard acl": {"norm": "dashboard_access_control", "related": ["dashboard access control"]},
    "dashboard permissions": {"norm": "dashboard_access_control", "related": ["dashboard access control"]},
    "dashboard roles": {"norm": "dashboard_access_control", "related": ["dashboard access control"]},
    "dac": {"norm": "dashboard_access_control", "related": ["dashboard access control"]},
    "dash access": {"norm": "dashboard_access_control", "related": ["dashboard access control"]},
    "dash acl": {"norm": "dashboard_access_control", "related": ["dashboard access control"]},
    "dash permissions": {"norm": "dashboard_access_control", "related": ["dashboard access control"]},
    "dash roles": {"norm": "dashboard_access_control", "related": ["dashboard access control"]},

    # Custom Dashboard Views
    "custom dashboard views": {"norm": "custom_dashboard_views", "related": ["custom views", "dashboard views", "custom dashboards", "dashboard customization"]},
    "custom views": {"norm": "custom_dashboard_views", "related": ["custom dashboard views"]},
    "dashboard views": {"norm": "custom_dashboard_views", "related": ["custom dashboard views"]},
    "custom dashboards": {"norm": "custom_dashboard_views", "related": ["custom dashboard views"]},
    "dashboard customization": {"norm": "custom_dashboard_views", "related": ["custom dashboard views"]},
    "cdv": {"norm": "custom_dashboard_views", "related": ["custom dashboard views"]},
    "custom dash": {"norm": "custom_dashboard_views", "related": ["custom dashboard views"]},
    "dash custom": {"norm": "custom_dashboard_views", "related": ["custom dashboard views"]},
    "dash views": {"norm": "custom_dashboard_views", "related": ["custom dashboard views"]},

    # Metric Correlation Display
    "metric correlation display": {"norm": "metric_correlation_display", "related": ["correlation display", "metric correlation", "correlation dashboard", "metrics correlation"]},
    "correlation display": {"norm": "metric_correlation_display", "related": ["metric correlation display"]},
    "metric correlation": {"norm": "metric_correlation_display", "related": ["metric correlation display"]},
    "correlation dashboard": {"norm": "metric_correlation_display", "related": ["metric correlation display"]},
    "metrics correlation": {"norm": "metric_correlation_display", "related": ["metric correlation display"]},
    "mcd": {"norm": "metric_correlation_display", "related": ["metric correlation display"]},
    "corr display": {"norm": "metric_correlation_display", "related": ["correlation display"]},
    "corr dash": {"norm": "metric_correlation_display", "related": ["correlation dashboard"]},

    # Heat Map for Engine Health
    "heat map for engine health": {"norm": "engine_health_heat_map", "related": ["engine health heatmap", "engine heatmap", "health heatmap", "engine health map"]},
    "engine health heatmap": {"norm": "engine_health_heat_map", "related": ["heat map for engine health"]},
    "engine heatmap": {"norm": "engine_health_heat_map", "related": ["heat map for engine health"]},
    "health heatmap": {"norm": "engine_health_heat_map", "related": ["heat map for engine health"]},
    "engine health map": {"norm": "engine_health_heat_map", "related": ["heat map for engine health"]},
    "ehhm": {"norm": "engine_health_heat_map", "related": ["heat map for engine health"]},
    "heatmap": {"norm": "engine_health_heat_map", "related": ["heat map for engine health"]},
    "heat map": {"norm": "engine_health_heat_map", "related": ["heat map for engine health"]},
    "eng heatmap": {"norm": "engine_health_heat_map", "related": ["engine heatmap"]},
    "eng health heatmap": {"norm": "engine_health_heat_map", "related": ["engine health heatmap"]},

    # Time Series Data Management
    "time series data management": {"norm": "time_series_data_management", "related": ["ts data management", "time series management", "ts management", "timeseries management"]},
    "ts data management": {"norm": "time_series_data_management", "related": ["time series data management"]},
    "time series management": {"norm": "time_series_data_management", "related": ["time series data management"]},
    "ts management": {"norm": "time_series_data_management", "related": ["time series data management"]},
    "timeseries management": {"norm": "time_series_data_management", "related": ["time series data management"]},
    "tsdm": {"norm": "time_series_data_management", "related": ["time series data management"]},
    "timeseries data": {"norm": "time_series_data_management", "related": ["time series data management"]},
    "ts data": {"norm": "time_series_data_management", "related": ["time series data management"]},
    "ts": {"norm": "time_series_data_management", "related": ["time series data management"]},

    # Dashboard Export: JSON, CSV, PDF
    "dashboard export": {"norm": "dashboard_export", "related": ["export dashboard", "dashboard export json", "dashboard export csv", "dashboard export pdf", "export json", "export csv", "export pdf"]},
    "export dashboard": {"norm": "dashboard_export", "related": ["dashboard export"]},
    "dashboard export json": {"norm": "dashboard_export_json", "related": ["dashboard export", "export json"]},
    "dashboard export csv": {"norm": "dashboard_export_csv", "related": ["dashboard export", "export csv"]},
    "dashboard export pdf": {"norm": "dashboard_export_pdf", "related": ["dashboard export", "export pdf"]},
    "export json": {"norm": "dashboard_export_json", "related": ["dashboard export json"]},
    "export csv": {"norm": "dashboard_export_csv", "related": ["dashboard export csv"]},
    "export pdf": {"norm": "dashboard_export_pdf", "related": ["dashboard export pdf"]},
    "dash export": {"norm": "dashboard_export", "related": ["dashboard export"]},
    "dash export json": {"norm": "dashboard_export_json", "related": ["dashboard export json"]},
    "dash export csv": {"norm": "dashboard_export_csv", "related": ["dashboard export csv"]},
    "dash export pdf": {"norm": "dashboard_export_pdf", "related": ["dashboard export pdf"]},
    "de": {"norm": "dashboard_export", "related": ["dashboard export"]},
    "de json": {"norm": "dashboard_export_json", "related": ["dashboard export json"]},
    "de csv": {"norm": "dashboard_export_csv", "related": ["dashboard export csv"]},
    "de pdf": {"norm": "dashboard_export_pdf", "related": ["dashboard export pdf"]},

    # SLO Compliance Dashboard
    "slo compliance dashboard": {"norm": "slo_compliance_dashboard", "related": ["slo dashboard", "compliance dashboard", "slo compliance", "service level objective dashboard"]},
    "slo dashboard": {"norm": "slo_compliance_dashboard", "related": ["slo compliance dashboard"]},
    "compliance dashboard": {"norm": "slo_compliance_dashboard", "related": ["slo compliance dashboard"]},
    "slo compliance": {"norm": "slo_compliance_dashboard", "related": ["slo compliance dashboard"]},
    "service level objective dashboard": {"norm": "slo_compliance_dashboard", "related": ["slo compliance dashboard"]},
    "slo dash": {"norm": "slo_compliance_dashboard", "related": ["slo compliance dashboard"]},
    "slo comp dash": {"norm": "slo_compliance_dashboard", "related": ["slo compliance dashboard"]},
    "slo comp": {"norm": "slo_compliance_dashboard", "related": ["slo compliance dashboard"]},
    "slo": {"norm": "slo_compliance_dashboard", "related": ["slo compliance dashboard"]},
    "slo dashboard compliance": {"norm": "slo_compliance_dashboard", "related": ["slo compliance dashboard"]},

    # Top Errors Leaderboard
    "top errors leaderboard": {"norm": "top_errors_leaderboard", "related": ["errors leaderboard", "top errors", "error leaderboard", "top error leaderboard"]},
    "errors leaderboard": {"norm": "top_errors_leaderboard", "related": ["top errors leaderboard"]},
    "top errors": {"norm": "top_errors_leaderboard", "related": ["top errors leaderboard"]},
    "error leaderboard": {"norm": "top_errors_leaderboard", "related": ["top errors leaderboard"]},
    "top error leaderboard": {"norm": "top_errors_leaderboard", "related": ["top errors leaderboard"]},
    "tel": {"norm": "top_errors_leaderboard", "related": ["top errors leaderboard"]},
    "top err leaderboard": {"norm": "top_errors_leaderboard", "related": ["top errors leaderboard"]},
    "top err": {"norm": "top_errors_leaderboard", "related": ["top errors leaderboard"]},
    "err leaderboard": {"norm": "top_errors_leaderboard", "related": ["top errors leaderboard"]},
    "errors board": {"norm": "top_errors_leaderboard", "related": ["top errors leaderboard"]},

    # Recovery Time Tracking
    "recovery time tracking": {"norm": "recovery_time_tracking", "related": ["recovery tracking", "recovery time", "recovery duration", "recovery time monitor"]},
    "recovery tracking": {"norm": "recovery_time_tracking", "related": ["recovery time tracking"]},
    "recovery time": {"norm": "recovery_time_tracking", "related": ["recovery time tracking"]},
    "recovery duration": {"norm": "recovery_time_tracking", "related": ["recovery time tracking"]},
    "recovery time monitor": {"norm": "recovery_time_tracking", "related": ["recovery time tracking"]},
    "rtt": {"norm": "recovery_time_tracking", "related": ["recovery time tracking"]},
    "recov time": {"norm": "recovery_time_tracking", "related": ["recovery time tracking"]},
    "recov tracking": {"norm": "recovery_time_tracking", "related": ["recovery time tracking"]},
    "recov duration": {"norm": "recovery_time_tracking", "related": ["recovery time tracking"]},

    # System Capacity Dashboard
    "system capacity dashboard": {"norm": "system_capacity_dashboard", "related": ["capacity dashboard", "system capacity", "capacity monitor", "capacity dash"]},
    "capacity dashboard": {"norm": "system_capacity_dashboard", "related": ["system capacity dashboard"]},
    "system capacity": {"norm": "system_capacity_dashboard", "related": ["system capacity dashboard"]},
    "capacity monitor": {"norm": "system_capacity_dashboard", "related": ["system capacity dashboard"]},
    "capacity dash": {"norm": "system_capacity_dashboard", "related": ["system capacity dashboard"]},
    "scd": {"norm": "system_capacity_dashboard", "related": ["system capacity dashboard"]},
    "sys capacity dash": {"norm": "system_capacity_dashboard", "related": ["system capacity dashboard"]},
    "sys capacity": {"norm": "system_capacity_dashboard", "related": ["system capacity dashboard"]},
    "sys cap dash": {"norm": "system_capacity_dashboard", "related": ["system capacity dashboard"]},
    "sys cap": {"norm": "system_capacity_dashboard", "related": ["system capacity dashboard"]},

    # Misspellings and common typos (examples)
    "dasboard": {"norm": "dashboard", "related": ["dashboard"]},
    "dashbord": {"norm": "dashboard", "related": ["dashboard"]},
    "dashbaord": {"norm": "dashboard", "related": ["dashboard"]},
    "metrci": {"norm": "metric", "related": ["metric"]},
    "metrc": {"norm": "metric", "related": ["metric"]},
    "metricks": {"norm": "metrics", "related": ["metrics"]},
    "metricks retention": {"norm": "metric_retention_policies", "related": ["metric retention policies"]},
    "aggretation": {"norm": "dashboard_data_aggregation", "related": ["dashboard data aggregation"]},
    "aggretation pattern": {"norm": "dashboard_data_aggregation", "related": ["aggregation pattern"]},
    "recovry": {"norm": "recovery", "related": ["recovery"]},
    "recovry time": {"norm": "recovery_time_tracking", "related": ["recovery time tracking"]},
    "recovry metrics": {"norm": "recovery_success_metrics", "related": ["recovery success metrics"]},
    "aler management": {"norm": "alert_management", "related": ["alert management"]},
    "aler acknowledge": {"norm": "alert_acknowledge", "related": ["alert acknowledge"]},
    "aler snooze": {"norm": "alert_snooze", "related": ["alert snooze"]},
    "aler escalate": {"norm": "alert_escalate", "related": ["alert escalate"]},
    "drfit severity dashboard": {"norm": "drift_severity_dashboard", "related": ["drift severity dashboard"]},
    "drfit dashboard": {"norm": "drift_severity_dashboard", "related": ["drift dashboard"]},
    "drfit severity": {"norm": "drift_severity_dashboard", "related": ["drift severity"]},
    "drfit monitor": {"norm": "drift_severity_dashboard", "related": ["drift monitor"]},
    "slo compiance dashboard": {"norm": "slo_compliance_dashboard", "related": ["slo compliance dashboard"]},
    "slo compiance": {"norm": "slo_compliance_dashboard", "related": ["slo compliance"]},
    "system capcity dashboard": {"norm": "system_capacity_dashboard", "related": ["system capacity dashboard"]},
    "system capcity": {"norm": "system_capacity_dashboard", "related": ["system capacity"]},
    "engin status matrix": {"norm": "engine_status_matrix", "related": ["engine status matrix"]},
    "engin matrix": {"norm": "engine_status_matrix", "related": ["engine matrix"]},
    "engin status": {"norm": "engine_status_matrix", "related": ["engine status"]},
    "engin grid": {"norm": "engine_status_matrix", "related": ["engine grid"]},
    "engin health heatmap": {"norm": "engine_health_heat_map", "related": ["engine health heatmap"]},
    "engin heatmap": {"norm": "engine_health_heat_map", "related": ["engine heatmap"]},
    "engin health map": {"norm": "engine_health_heat_map", "related": ["engine health map"]},

    # Miscellaneous
    "dashboard": {"norm": "dashboard", "related": ["dashboard data aggregation", "dashboard access control", "dashboard refresh strategies", "custom dashboard views"]},
    "metric": {"norm": "metric", "related": ["metric retention policies", "metric correlation display"]},
    "metrics": {"norm": "metric", "related": ["metric retention policies", "metric correlation display"]},
    "error": {"norm": "error", "related": ["error rate trending", "top errors leaderboard"]},
    "errors": {"norm": "error", "related": ["error rate trending", "top errors leaderboard"]},
    "system": {"norm": "system", "related": ["system health score weighted composite", "system capacity dashboard"]},
    "engine": {"norm": "engine", "related": ["engine status matrix", "engine health heat map"]},
    "alert": {"norm": "alert", "related": ["alert management", "alert acknowledge", "alert snooze", "alert escalate"]},
    "recovery": {"norm": "recovery", "related": ["recovery success metrics", "recovery time tracking"]},
    "drift": {"norm": "drift", "related": ["drift severity dashboard"]},
    "capacity": {"norm": "capacity", "related": ["system capacity dashboard"]},
    "compliance": {"norm": "compliance", "related": ["slo compliance dashboard"]},
    "correlation": {"norm": "correlation", "related": ["metric correlation display"]},
    "heat map": {"norm": "engine_health_heat_map", "related": ["engine health heatmap"]},
    "time series": {"norm": "time_series_data_management", "related": ["time series data management"]},
    "timeseries": {"norm": "time_series_data_management", "related": ["time series data management"]},
    "export": {"norm": "dashboard_export", "related": ["dashboard export"]},
    "leaderboard": {"norm": "top_errors_leaderboard", "related": ["top errors leaderboard"]},
    "tracking": {"norm": "recovery_time_tracking", "related": ["recovery time tracking"]},
    "retention": {"norm": "metric_retention_policies", "related": ["metric retention policies"]},
    "refresh": {"norm": "dashboard_refresh_strategies", "related": ["dashboard refresh strategies"]},
    "custom": {"norm": "custom_dashboard_views", "related": ["custom dashboard views"]},
    "view": {"norm": "custom_dashboard_views", "related": ["custom dashboard views"]},
    "views": {"norm": "custom_dashboard_views", "related": ["custom dashboard views"]},
    "acl": {"norm": "dashboard_access_control", "related": ["dashboard access control"]},
    "permissions": {"norm": "dashboard_access_control", "related": ["dashboard access control"]},
    "roles": {"norm": "dashboard_access_control", "related": ["dashboard access control"]},
    "score": {"norm": "system_health_score_weighted_composite", "related": ["system health score"]},
    "composite": {"norm": "system_health_score_weighted_composite", "related": ["system health score"]},
    "severity": {"norm": "drift_severity_dashboard", "related": ["drift severity dashboard"]},
    "monitor": {"norm": "drift_severity_dashboard", "related": ["drift severity dashboard"]},
    "success": {"norm": "recovery_success_metrics", "related": ["recovery success metrics"]},
    "duration": {"norm": "recovery_time_tracking", "related": ["recovery time tracking"]},
    "batch": {"norm": "batch_metrics", "related": ["batch metrics"]},
    "json": {"norm": "dashboard_export_json", "related": ["dashboard export json"]},
    "csv": {"norm": "dashboard_export_csv", "related": ["dashboard export csv"]},
    "pdf": {"norm": "dashboard_export_pdf", "related": ["dashboard export pdf"]},
    "slo": {"norm": "slo_compliance_dashboard", "related": ["slo compliance dashboard"]},
    "objective": {"norm": "slo_compliance_dashboard", "related": ["slo compliance dashboard"]},
    "service level objective": {"norm": "slo_compliance_dashboard", "related": ["slo compliance dashboard"]},
    "health": {"norm": "system_health_score_weighted_composite", "related": ["system health score weighted composite", "engine health heat map"]},
    "status": {"norm": "engine_status_matrix", "related": ["engine status matrix"]},
    "matrix": {"norm": "engine_status_matrix", "related": ["engine status matrix"]},
    "grid": {"norm": "engine_status_matrix", "related": ["engine status matrix"]},
    "trend": {"norm": "error_rate_trending", "related": ["error rate trending"]},
    "trending": {"norm": "error_rate_trending", "related": ["error rate trending"]},
    "rate": {"norm": "error_rate_trending", "related": ["error rate trending"]},
    "map": {"norm": "engine_health_heat_map", "related": ["engine health heat map"]},
    "data": {"norm": "dashboard_data_aggregation", "related": ["dashboard data aggregation"]},
    "management": {"norm": "alert_management", "related": ["alert management"]},
    "policy": {"norm": "metric_retention_policies", "related": ["metric retention policies"]},
    "policies": {"norm": "metric_retention_policies", "related": ["metric retention policies"]},
    "dashboard export": {"norm": "dashboard_export", "related": ["dashboard export"]},
    "dashboard export json": {"norm": "dashboard_export_json", "related": ["dashboard export json"]},
    "dashboard export csv": {"norm": "dashboard_export_csv", "related": ["dashboard export csv"]},
    "dashboard export pdf": {"norm": "dashboard_export_pdf", "related": ["dashboard export pdf"]},
    "dashboard export": {"norm": "dashboard_export", "related": ["dashboard export"]},
    "dashboard export json": {"norm": "dashboard_export_json", "related": ["dashboard export json"]},
    "dashboard export csv": {"norm": "dashboard_export_csv", "related": ["dashboard export csv"]},
    "dashboard export pdf": {"norm": "dashboard_export_pdf", "related": ["dashboard export pdf"]},
    "dashboard export": {"norm": "dashboard_export", "related": ["dashboard export"]},
    "dashboard export json": {"norm": "dashboard_export_json", "related": ["dashboard export json"]},
    "dashboard export csv": {"norm": "dashboard_export_csv", "related": ["dashboard export csv"]},
    "dashboard export pdf": {"norm": "dashboard_export_pdf", "related": ["dashboard export pdf"]},
}

_EXPECTED_ENTRY_COUNT = len(SEMANTIC_MAP)

def _compute_map_hash() -> str:
    # Deterministic hash: sort keys, serialize values as JSON
    items = sorted((k, v["norm"], sorted(v["related"])) for k, v in SEMANTIC_MAP.items())
    serialized = json.dumps(items, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

_MAP_INTEGRITY_HASH = _compute_map_hash()

def verify_integrity() -> Dict[str, Any]:
    actual_count = len(SEMANTIC_MAP)
    actual_hash = _compute_map_hash()
    is_valid = (actual_count == _EXPECTED_ENTRY_COUNT) and (actual_hash == _MAP_INTEGRITY_HASH)
    return {
        "status": "ok" if is_valid else "error",
        "entries": actual_count,
        "hash": actual_hash,
        "is_valid": is_valid
    }

def normalize_term(term: str) -> str:
    key = term.strip().lower()
    entry = SEMANTIC_MAP.get(key)
    if entry:
        return entry["norm"]
    return key

def get_related_terms(term: str) -> List[str]:
    key = term.strip().lower()
    entry = SEMANTIC_MAP.get(key)
    if entry:
        return list(entry["related"])
    return []

def get_all_mappings() -> Dict[str, Dict[str, Any]]:
    return dict(SEMANTIC_MAP)