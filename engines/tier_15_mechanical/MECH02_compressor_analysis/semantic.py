import hashlib
import re

SEMANTIC_MAP_VERSION = "1.0.0"
SEMANTIC_MAP_AUTHOR = "MECH02 Python Engineering Team"
SEMANTIC_MAP_ENGINE = "MECH02_compressor_analysis"

# SEMANTIC_MAP: mapping domain terms, synonyms, acronyms, misspellings, related terms to normalized forms
SEMANTIC_MAP = {
    # reciprocating compressor clearance volume
    "reciprocating compressor clearance volume": "reciprocating_compressor_clearance_volume",
    "clearance volume": "reciprocating_compressor_clearance_volume",
    "compressor clearance": "reciprocating_compressor_clearance_volume",
    "clearance": "reciprocating_compressor_clearance_volume",
    "recip clearance": "reciprocating_compressor_clearance_volume",
    "recip compressor clearance": "reciprocating_compressor_clearance_volume",
    "reciprocating clearance": "reciprocating_compressor_clearance_volume",
    "rcv": "reciprocating_compressor_clearance_volume",
    "reciprocating compressor cv": "reciprocating_compressor_clearance_volume",
    "compressor cv": "reciprocating_compressor_clearance_volume",
    "compressor clearance vol": "reciprocating_compressor_clearance_volume",
    "recip clearance vol": "reciprocating_compressor_clearance_volume",
    "clearance vol": "reciprocating_compressor_clearance_volume",
    "reciprocating compressor dead space": "reciprocating_compressor_clearance_volume",
    "dead space": "reciprocating_compressor_clearance_volume",
    "dead volume": "reciprocating_compressor_clearance_volume",
    "compressor dead volume": "reciprocating_compressor_clearance_volume",
    "recip dead volume": "reciprocating_compressor_clearance_volume",
    "reciprocating compressor dead volume": "reciprocating_compressor_clearance_volume",
    "reciprocating compressor residual volume": "reciprocating_compressor_clearance_volume",
    "residual volume": "reciprocating_compressor_clearance_volume",
    "compressor residual volume": "reciprocating_compressor_clearance_volume",
    "recip residual volume": "reciprocating_compressor_clearance_volume",

    # centrifugal surge control
    "centrifugal surge control": "centrifugal_surge_control",
    "surge control": "centrifugal_surge_control",
    "centrifugal compressor surge control": "centrifugal_surge_control",
    "compressor surge control": "centrifugal_surge_control",
    "centrifugal surge": "centrifugal_surge_control",
    "surge protection": "centrifugal_surge_control",
    "anti-surge": "centrifugal_surge_control",
    "antisurge": "centrifugal_surge_control",
    "anti surge": "centrifugal_surge_control",
    "centrifugal anti-surge": "centrifugal_surge_control",
    "centrifugal antisurge": "centrifugal_surge_control",
    "centrifugal anti surge": "centrifugal_surge_control",
    "compressor anti-surge": "centrifugal_surge_control",
    "compressor antisurge": "centrifugal_surge_control",
    "compressor anti surge": "centrifugal_surge_control",
    "surge controller": "centrifugal_surge_control",
    "surge detection": "centrifugal_surge_control",
    "surge avoidance": "centrifugal_surge_control",
    "surge margin": "centrifugal_surge_control",
    "surge line": "centrifugal_surge_control",
    "surge limit": "centrifugal_surge_control",

    # polytropic vs isentropic efficiency
    "polytropic vs isentropic efficiency": "polytropic_vs_isentropic_efficiency",
    "polytropic efficiency": "polytropic_vs_isentropic_efficiency",
    "isentropic efficiency": "polytropic_vs_isentropic_efficiency",
    "compressor efficiency": "polytropic_vs_isentropic_efficiency",
    "efficiency comparison": "polytropic_vs_isentropic_efficiency",
    "polytropic/isotropic efficiency": "polytropic_vs_isentropic_efficiency",
    "polytropic efficiency calculation": "polytropic_vs_isentropic_efficiency",
    "isentropic efficiency calculation": "polytropic_vs_isentropic_efficiency",
    "compressor polytropic efficiency": "polytropic_vs_isentropic_efficiency",
    "compressor isentropic efficiency": "polytropic_vs_isentropic_efficiency",
    "poly efficiency": "polytropic_vs_isentropic_efficiency",
    "iso efficiency": "polytropic_vs_isentropic_efficiency",
    "poly vs iso efficiency": "polytropic_vs_isentropic_efficiency",
    "poly vs iso": "polytropic_vs_isentropic_efficiency",
    "polytropic vs isentropic": "polytropic_vs_isentropic_efficiency",
    "isentropic vs polytropic": "polytropic_vs_isentropic_efficiency",
    "efficiency types": "polytropic_vs_isentropic_efficiency",
    "compressor efficiency types": "polytropic_vs_isentropic_efficiency",

    # rod load analysis reciprocating
    "rod load analysis reciprocating": "rod_load_analysis_reciprocating",
    "rod load analysis": "rod_load_analysis_reciprocating",
    "reciprocating rod load analysis": "rod_load_analysis_reciprocating",
    "rod load": "rod_load_analysis_reciprocating",
    "compressor rod load": "rod_load_analysis_reciprocating",
    "recip rod load": "rod_load_analysis_reciprocating",
    "rod loading": "rod_load_analysis_reciprocating",
    "rod load calculation": "rod_load_analysis_reciprocating",
    "rod load monitoring": "rod_load_analysis_reciprocating",
    "rod load limit": "rod_load_analysis_reciprocating",
    "rod load failure": "rod_load_analysis_reciprocating",
    "rod load stress": "rod_load_analysis_reciprocating",
    "rod load design": "rod_load_analysis_reciprocating",
    "rod load safety": "rod_load_analysis_reciprocating",
    "reciprocating compressor rod load": "rod_load_analysis_reciprocating",
    "compressor rod load analysis": "rod_load_analysis_reciprocating",

    # intercooling benefits multistage
    "intercooling benefits multistage": "intercooling_benefits_multistage",
    "intercooling benefits": "intercooling_benefits_multistage",
    "intercooling": "intercooling_benefits_multistage",
    "multistage intercooling": "intercooling_benefits_multistage",
    "intercooler": "intercooling_benefits_multistage",
    "intercooler benefits": "intercooling_benefits_multistage",
    "intercooling advantages": "intercooling_benefits_multistage",
    "multistage compressor intercooling": "intercooling_benefits_multistage",
    "compressor intercooling": "intercooling_benefits_multistage",
    "intercooler design": "intercooling_benefits_multistage",
    "intercooler performance": "intercooling_benefits_multistage",
    "intercooler efficiency": "intercooling_benefits_multistage",
    "intercooling effect": "intercooling_benefits_multistage",
    "intercooling stage": "intercooling_benefits_multistage",
    "intercooling in multistage compressors": "intercooling_benefits_multistage",
    "intercooler in multistage compressors": "intercooling_benefits_multistage",

    # gas properties compression performance
    "gas properties compression performance": "gas_properties_compression_performance",
    "gas properties": "gas_properties_compression_performance",
    "compression performance": "gas_properties_compression_performance",
    "compressor performance": "gas_properties_compression_performance",
    "gas property": "gas_properties_compression_performance",
    "compressor gas properties": "gas_properties_compression_performance",
    "gas composition": "gas_properties_compression_performance",
    "gas compressibility": "gas_properties_compression_performance",
    "compressibility factor": "gas_properties_compression_performance",
    "z factor": "gas_properties_compression_performance",
    "gas density": "gas_properties_compression_performance",
    "gas viscosity": "gas_properties_compression_performance",
    "gas molecular weight": "gas_properties_compression_performance",
    "gas temperature": "gas_properties_compression_performance",
    "gas pressure": "gas_properties_compression_performance",
    "gas analysis": "gas_properties_compression_performance",
    "compressor gas analysis": "gas_properties_compression_performance",
    "gas composition analysis": "gas_properties_compression_performance",
    "gas performance": "gas_properties_compression_performance",
    "compressor gas performance": "gas_properties_compression_performance",

    # compressor valve design maintenance
    "compressor valve design maintenance": "compressor_valve_design_maintenance",
    "compressor valve design": "compressor_valve_design_maintenance",
    "compressor valve maintenance": "compressor_valve_design_maintenance",
    "valve design": "compressor_valve_design_maintenance",
    "valve maintenance": "compressor_valve_design_maintenance",
    "compressor valve": "compressor_valve_design_maintenance",
    "valve": "compressor_valve_design_maintenance",
    "valve failure": "compressor_valve_design_maintenance",
    "valve replacement": "compressor_valve_design_maintenance",
    "valve repair": "compressor_valve_design_maintenance",
    "valve inspection": "compressor_valve_design_maintenance",
    "compressor valve inspection": "compressor_valve_design_maintenance",
    "compressor valve repair": "compressor_valve_design_maintenance",
    "compressor valve replacement": "compressor_valve_design_maintenance",
    "valve types": "compressor_valve_design_maintenance",
    "valve selection": "compressor_valve_design_maintenance",
    "valve materials": "compressor_valve_design_maintenance",
    "valve reliability": "compressor_valve_design_maintenance",
    "valve design standards": "compressor_valve_design_maintenance",

    # packing rider ring wear mechanisms
    "packing rider ring wear mechanisms": "packing_rider_ring_wear_mechanisms",
    "packing wear": "packing_rider_ring_wear_mechanisms",
    "rider ring wear": "packing_rider_ring_wear_mechanisms",
    "packing ring wear": "packing_rider_ring_wear_mechanisms",
    "wear mechanisms": "packing_rider_ring_wear_mechanisms",
    "compressor packing wear": "packing_rider_ring_wear_mechanisms",
    "compressor rider ring wear": "packing_rider_ring_wear_mechanisms",
    "packing ring": "packing_rider_ring_wear_mechanisms",
    "rider ring": "packing_rider_ring_wear_mechanisms",
    "packing": "packing_rider_ring_wear_mechanisms",
    "packing failure": "packing_rider_ring_wear_mechanisms",
    "rider ring failure": "packing_rider_ring_wear_mechanisms",
    "packing ring failure": "packing_rider_ring_wear_mechanisms",
    "packing ring replacement": "packing_rider_ring_wear_mechanisms",
    "rider ring replacement": "packing_rider_ring_wear_mechanisms",
    "packing ring maintenance": "packing_rider_ring_wear_mechanisms",
    "rider ring maintenance": "packing_rider_ring_wear_mechanisms",
    "packing ring inspection": "packing_rider_ring_wear_mechanisms",
    "rider ring inspection": "packing_rider_ring_wear_mechanisms",
    "packing ring materials": "packing_rider_ring_wear_mechanisms",
    "rider ring materials": "packing_rider_ring_wear_mechanisms",

    # api 618 recip standards compliance
    "api 618 recip standards compliance": "api_618_recip_standards_compliance",
    "api 618 compliance": "api_618_recip_standards_compliance",
    "api 618": "api_618_recip_standards_compliance",
    "api618": "api_618_recip_standards_compliance",
    "api 618 reciprocating compressor": "api_618_recip_standards_compliance",
    "api 618 reciprocating": "api_618_recip_standards_compliance",
    "api 618 standards": "api_618_recip_standards_compliance",
    "api 618 standard": "api_618_recip_standards_compliance",
    "api 618 recip": "api_618_recip_standards_compliance",
    "api 618 compressor": "api_618_recip_standards_compliance",
    "api 618 recip compliance": "api_618_recip_standards_compliance",
    "api 618 reciprocating compliance": "api_618_recip_standards_compliance",
    "api 618 compressor compliance": "api_618_recip_standards_compliance",
    "api 618 requirements": "api_618_recip_standards_compliance",
    "api 618 specification": "api_618_recip_standards_compliance",
    "api 618 specs": "api_618_recip_standards_compliance",
    "api 618 spec": "api_618_recip_standards_compliance",
    "api 618 reciprocating compressor standards": "api_618_recip_standards_compliance",
    "api 618 reciprocating compressor compliance": "api_618_recip_standards_compliance",

    # api 617 centrifugal standards compliance
    "api 617 centrifugal standards compliance": "api_617_centrifugal_standards_compliance",
    "api 617 compliance": "api_617_centrifugal_standards_compliance",
    "api 617": "api_617_centrifugal_standards_compliance",
    "api617": "api_617_centrifugal_standards_compliance",
    "api 617 centrifugal compressor": "api_617_centrifugal_standards_compliance",
    "api 617 centrifugal": "api_617_centrifugal_standards_compliance",
    "api 617 standards": "api_617_centrifugal_standards_compliance",
    "api 617 standard": "api_617_centrifugal_standards_compliance",
    "api 617 compressor": "api_617_centrifugal_standards_compliance",
    "api 617 centrifugal compliance": "api_617_centrifugal_standards_compliance",
    "api 617 compressor compliance": "api_617_centrifugal_standards_compliance",
    "api 617 requirements": "api_617_centrifugal_standards_compliance",
    "api 617 specification": "api_617_centrifugal_standards_compliance",
    "api 617 specs": "api_617_centrifugal_standards_compliance",
    "api 617 spec": "api_617_centrifugal_standards_compliance",
    "api 617 centrifugal compressor standards": "api_617_centrifugal_standards_compliance",
    "api 617 centrifugal compressor compliance": "api_617_centrifugal_standards_compliance",

    # capacity control methods comparison
    "capacity control methods comparison": "capacity_control_methods_comparison",
    "capacity control methods": "capacity_control_methods_comparison",
    "capacity control": "capacity_control_methods_comparison",
    "compressor capacity control": "capacity_control_methods_comparison",
    "capacity control comparison": "capacity_control_methods_comparison",
    "capacity control techniques": "capacity_control_methods_comparison",
    "capacity control strategies": "capacity_control_methods_comparison",
    "capacity control options": "capacity_control_methods_comparison",
    "compressor capacity control methods": "capacity_control_methods_comparison",
    "capacity control method": "capacity_control_methods_comparison",
    "capacity control types": "capacity_control_methods_comparison",
    "capacity control systems": "capacity_control_methods_comparison",
    "capacity control system": "capacity_control_methods_comparison",
    "capacity control devices": "capacity_control_methods_comparison",
    "capacity control device": "capacity_control_methods_comparison",
    "capacity control valve": "capacity_control_methods_comparison",
    "capacity control valves": "capacity_control_methods_comparison",
    "compressor capacity control comparison": "capacity_control_methods_comparison",

    # vibration monitoring api 670
    "vibration monitoring api 670": "vibration_monitoring_api_670",
    "vibration monitoring": "vibration_monitoring_api_670",
    "api 670 vibration monitoring": "vibration_monitoring_api_670",
    "api 670": "vibration_monitoring_api_670",
    "api670": "vibration_monitoring_api_670",
    "api 670 compliance": "vibration_monitoring_api_670",
    "vibration monitoring compliance": "vibration_monitoring_api_670",
    "vibration monitoring standards": "vibration_monitoring_api_670",
    "vibration monitoring standard": "vibration_monitoring_api_670",
    "vibration monitoring requirements": "vibration_monitoring_api_670",
    "vibration monitoring specification": "vibration_monitoring_api_670",
    "vibration monitoring specs": "vibration_monitoring_api_670",
    "vibration monitoring spec": "vibration_monitoring_api_670",
    "vibration monitoring api 670 compliance": "vibration_monitoring_api_670",
    "vibration monitoring api 670 standards": "vibration_monitoring_api_670",
    "vibration monitoring api 670 specification": "vibration_monitoring_api_670",
    "vibration monitoring api 670 specs": "vibration_monitoring_api_670",
    "vibration monitoring api 670 spec": "vibration_monitoring_api_670",

    # screw compressor applications limitations
    "screw compressor applications limitations": "screw_compressor_applications_limitations",
    "screw compressor applications": "screw_compressor_applications_limitations",
    "screw compressor limitations": "screw_compressor_applications_limitations",
    "screw compressor": "screw_compressor_applications_limitations",
    "screw compressor application": "screw_compressor_applications_limitations",
    "screw compressor uses": "screw_compressor_applications_limitations",
    "screw compressor use": "screw_compressor_applications_limitations",
    "screw compressor advantages": "screw_compressor_applications_limitations",
    "screw compressor disadvantages": "screw_compressor_applications_limitations",
    "screw compressor pros": "screw_compressor_applications_limitations",
    "screw compressor cons": "screw_compressor_applications_limitations",
    "screw compressor suitability": "screw_compressor_applications_limitations",
    "screw compressor selection": "screw_compressor_applications_limitations",
    "screw compressor types": "screw_compressor_applications_limitations",
    "screw compressor design": "screw_compressor_applications_limitations",
    "screw compressor performance": "screw_compressor_applications_limitations",
    "screw compressor efficiency": "screw_compressor_applications_limitations",
    "screw compressor capacity": "screw_compressor_applications_limitations",

    # compression ratio calculation multistage
    "compression ratio calculation multistage": "compression_ratio_calculation_multistage",
    "compression ratio calculation": "compression_ratio_calculation_multistage",
    "compression ratio": "compression_ratio_calculation_multistage",
    "multistage compression ratio": "compression_ratio_calculation_multistage",
    "compressor compression ratio": "compression_ratio_calculation_multistage",
    "multistage compressor compression ratio": "compression_ratio_calculation_multistage",
    "compression ratio formula": "compression_ratio_calculation_multistage",
    "compression ratio equations": "compression_ratio_calculation_multistage",
    "compression ratio equation": "compression_ratio_calculation_multistage",
    "compression ratio calculation multistage compressors": "compression_ratio_calculation_multistage",
    "compression ratio calculation multistage compressor": "compression_ratio_calculation_multistage",
    "compression ratio calculation for multistage compressors": "compression_ratio_calculation_multistage",
    "compression ratio calculation for multistage compressor": "compression_ratio_calculation_multistage",
    "compression ratio calculation for compressors": "compression_ratio_calculation_multistage",
    "compression ratio calculation for compressor": "compression_ratio_calculation_multistage",
    "compression ratio calculation in compressors": "compression_ratio_calculation_multistage",
    "compression ratio calculation in compressor": "compression_ratio_calculation_multistage",

    # field gas compression for gas lift
    "field gas compression for gas lift": "field_gas_compression_for_gas_lift",
    "field gas compression": "field_gas_compression_for_gas_lift",
    "gas lift compression": "field_gas_compression_for_gas_lift",
    "field gas compressor": "field_gas_compression_for_gas_lift",
    "gas lift compressor": "field_gas_compression_for_gas_lift",
    "gas lift": "field_gas_compression_for_gas_lift",
    "gas lift field compression": "field_gas_compression_for_gas_lift",
    "field compressor gas lift": "field_gas_compression_for_gas_lift",
    "field gas lift compressor": "field_gas_compression_for_gas_lift",
    "field gas lift compression": "field_gas_compression_for_gas_lift",
    "gas lift field compressor": "field_gas_compression_for_gas_lift",
    "gas lift field compression": "field_gas_compression_for_gas_lift",
    "gas lift compressor field": "field_gas_compression_for_gas_lift",
    "gas lift compression field": "field_gas_compression_for_gas_lift",

    # gas dehydration before compression
    "gas dehydration before compression": "gas_dehydration_before_compression",
    "gas dehydration": "gas_dehydration_before_compression",
    "dehydration before compression": "gas_dehydration_before_compression",
    "compressor gas dehydration": "gas_dehydration_before_compression",
    "gas dehydration compressor": "gas_dehydration_before_compression",
    "gas dehydration process": "gas_dehydration_before_compression",
    "gas dehydration methods": "gas_dehydration_before_compression",
    "gas dehydration system": "gas_dehydration_before_compression",
    "gas dehydration systems": "gas_dehydration_before_compression",
    "gas dehydration unit": "gas_dehydration_before_compression",
    "gas dehydration units": "gas_dehydration_before_compression",
    "gas dehydration plant": "gas_dehydration_before_compression",
    "gas dehydration plants": "gas_dehydration_before_compression",
    "gas dehydration technology": "gas_dehydration_before_compression",
    "gas dehydration technologies": "gas_dehydration_before_compression",
    "gas dehydration equipment": "gas_dehydration_before_compression",
    "gas dehydration equipment compressor": "gas_dehydration_before_compression",

    # compressor driver selection engine motor turbine
    "compressor driver selection engine motor turbine": "compressor_driver_selection_engine_motor_turbine",
    "compressor driver selection": "compressor_driver_selection_engine_motor_turbine",
    "compressor driver": "compressor_driver_selection_engine_motor_turbine",
    "compressor engine": "compressor_driver_selection_engine_motor_turbine",
    "compressor motor": "compressor_driver_selection_engine_motor_turbine",
    "compressor turbine": "compressor_driver_selection_engine_motor_turbine",
    "compressor driver selection engine": "compressor_driver_selection_engine_motor_turbine",
    "compressor driver selection motor": "compressor_driver_selection_engine_motor_turbine",
    "compressor driver selection turbine": "compressor_driver_selection_engine_motor_turbine",
    "compressor driver selection engines": "compressor_driver_selection_engine_motor_turbine",
    "compressor driver selection motors": "compressor_driver_selection_engine_motor_turbine",
    "compressor driver selection turbines": "compressor_driver_selection_engine_motor_turbine",
    "compressor driver selection criteria": "compressor_driver_selection_engine_motor_turbine",
    "compressor driver selection requirements": "compressor_driver_selection_engine_motor_turbine",
    "compressor driver selection specification": "compressor_driver_selection_engine_motor_turbine",
    "compressor driver selection specs": "compressor_driver_selection_engine_motor_turbine",
    "compressor driver selection spec": "compressor_driver_selection_engine_motor_turbine",
    "compressor driver selection options": "compressor_driver_selection_engine_motor_turbine",
    "compressor driver selection alternatives": "compressor_driver_selection_engine_motor_turbine",

    # compressor station design layout
    "compressor station design layout": "compressor_station_design_layout",
    "compressor station design": "compressor_station_design_layout",
    "compressor station layout": "compressor_station_design_layout",
    "station design": "compressor_station_design_layout",
    "station layout": "compressor_station_design_layout",
    "compressor station": "compressor_station_design_layout",
    "station": "compressor_station_design_layout",
    "compressor station design criteria": "compressor_station_design_layout",
    "compressor station design requirements": "compressor_station_design_layout",
    "compressor station design specification": "compressor_station_design_layout",
    "compressor station design specs": "compressor_station_design_layout",
    "compressor station design spec": "compressor_station_design_layout",
    "compressor station design options": "compressor_station_design_layout",
    "compressor station design alternatives": "compressor_station_design_layout",
    "compressor station design standards": "compressor_station_design_layout",
    "compressor station design standard": "compressor_station_design_layout",
    "compressor station design layout criteria": "compressor_station_design_layout",
    "compressor station design layout requirements": "compressor_station_design_layout",
    "compressor station design layout specification": "compressor_station_design_layout",
    "compressor station design layout specs": "compressor_station_design_layout",
    "compressor station design layout spec": "compressor_station_design_layout",

    # ngl recovery compression refrigeration
    "ngl recovery compression refrigeration": "ngl_recovery_compression_refrigeration",
    "ngl recovery compression": "ngl_recovery_compression_refrigeration",
    "ngl recovery refrigeration": "ngl_recovery_compression_refrigeration",
    "ngl recovery": "ngl_recovery_compression_refrigeration",
    "ngl compression": "ngl_recovery_compression_refrigeration",
    "ngl refrigeration": "ngl_recovery_compression_refrigeration",
    "ngl": "ngl_recovery_compression_refrigeration",
    "ngl recovery compressor": "ngl_recovery_compression_refrigeration",
    "ngl recovery compressors": "ngl_recovery_compression_refrigeration",
    "ngl recovery compression system": "ngl_recovery_compression_refrigeration",
    "ngl recovery compression systems": "ngl_recovery_compression_refrigeration",
    "ngl recovery compression unit": "ngl_recovery_compression_refrigeration",
    "ngl recovery compression units": "ngl_recovery_compression_refrigeration",
    "ngl recovery compression plant": "ngl_recovery_compression_refrigeration",
    "ngl recovery compression plants": "ngl_recovery_compression_refrigeration",
    "ngl recovery compression technology": "ngl_recovery_compression_refrigeration",
    "ngl recovery compression technologies": "ngl_recovery_compression_refrigeration",
    "ngl recovery compression equipment": "ngl_recovery_compression_refrigeration",
    "ngl recovery compression equipment refrigeration": "ngl_recovery_compression_refrigeration",

    # gas gathering compression systems
    "gas gathering compression systems": "gas_gathering_compression_systems",
    "gas gathering compression": "gas_gathering_compression_systems",
    "gas gathering compressor": "gas_gathering_compression_systems",
    "gas gathering compressors": "gas_gathering_compression_systems",
    "gas gathering": "gas_gathering_compression_systems",
    "gas gathering system": "gas_gathering_compression_systems",
    "gas gathering systems": "gas_gathering_compression_systems",
    "gas gathering compression system": "gas_gathering_compression_systems",
    "gas gathering compression unit": "gas_gathering_compression_systems",
    "gas gathering compression units": "gas_gathering_compression_systems",
    "gas gathering compression plant": "gas_gathering_compression_systems",
    "gas gathering compression plants": "gas_gathering_compression_systems",
    "gas gathering compression technology": "gas_gathering_compression_systems",
    "gas gathering compression technologies": "gas_gathering_compression_systems",
    "gas gathering compression equipment": "gas_gathering_compression_systems",
    "gas gathering compression equipment system": "gas_gathering_compression_systems",
    "gas gathering compression equipment systems": "gas_gathering_compression_systems",
    "gas gathering compression equipment unit": "gas_gathering_compression_systems",
    "gas gathering compression equipment units": "gas_gathering_compression_systems",
    "gas gathering compression equipment plant": "gas_gathering_compression_systems",
    "gas gathering compression equipment plants": "gas_gathering_compression_systems",
    "gas gathering compression equipment technology": "gas_gathering_compression_systems",
    "gas gathering compression equipment technologies": "gas_gathering_compression_systems",
}

# Add misspellings, abbreviations, and more synonyms for each domain (targeting 200+ entries)
misspellings = {
    "reciprocating compressor clearnce volume": "reciprocating_compressor_clearance_volume",
    "centrifugal surge cntrol": "centrifugal_surge_control",
    "polytropic vs isentropic efficency": "polytropic_vs_isentropic_efficiency",
    "rod load analisis reciprocating": "rod_load_analysis_reciprocating",
    "intercooling benfits multistage": "intercooling_benefits_multistage",
    "gas properties comprssion performance": "gas_properties_compression_performance",
    "compressor valve desgin maintenance": "compressor_valve_design_maintenance",
    "packing rider ring wear mechnisms": "packing_rider_ring_wear_mechanisms",
    "api 618 recip standards complience": "api_618_recip_standards_compliance",
    "api 617 centrifugal standards complience": "api_617_centrifugal_standards_compliance",
    "capacity control methods comparsion": "capacity_control_methods_comparison",
    "vibration monitoring api 6700": "vibration_monitoring_api_670",
    "screw compressor aplications limitations": "screw_compressor_applications_limitations",
    "compression ratio calcuation multistage": "compression_ratio_calculation_multistage",
    "field gas compression for gaslift": "field_gas_compression_for_gas_lift",
    "gas dehydraton before compression": "gas_dehydration_before_compression",
    "compressor driver selection engin motor turbine": "compressor_driver_selection_engine_motor_turbine",
    "compressor station desgin layout": "compressor_station_design_layout",
    "ngl recovery comprssion refrigeration": "ngl_recovery_compression_refrigeration",
    "gas gathering comprssion systems": "gas_gathering_compression_systems",
}

abbreviations = {
    "cv": "reciprocating_compressor_clearance_volume",
    "rcv": "reciprocating_compressor_clearance_volume",
    "anti-surge": "centrifugal_surge_control",
    "poly eff": "polytropic_vs_isentropic_efficiency",
    "iso eff": "polytropic_vs_isentropic_efficiency",
    "api618": "api_618_recip_standards_compliance",
    "api617": "api_617_centrifugal_standards_compliance",
    "api670": "vibration_monitoring_api_670",
    "ngl": "ngl_recovery_compression_refrigeration",
}

related_terms = {
    "dead space": "reciprocating_compressor_clearance_volume",
    "compressibility factor": "gas_properties_compression_performance",
    "z factor": "gas_properties_compression_performance",
    "intercooler": "intercooling_benefits_multistage",
    "packing ring": "packing_rider_ring_wear_mechanisms",
    "rider ring": "packing_rider_ring_wear_mechanisms",
    "capacity control valve": "capacity_control_methods_comparison",
    "vibration monitoring": "vibration_monitoring_api_670",
    "compression ratio": "compression_ratio_calculation_multistage",
    "gas lift": "field_gas_compression_for_gas_lift",
    "dehydration": "gas_dehydration_before_compression",
    "compressor driver": "compressor_driver_selection_engine_motor_turbine",
    "station": "compressor_station_design_layout",
    "refrigeration": "ngl_recovery_compression_refrigeration",
    "gas gathering": "gas_gathering_compression_systems",
}

# Merge all into SEMANTIC_MAP
SEMANTIC_MAP.update(misspellings)
SEMANTIC_MAP.update(abbreviations)
SEMANTIC_MAP.update(related_terms)

# Add more synonyms, acronyms, and misspellings for each domain (targeting 200+ entries)
extra_synonyms = {
    "reciprocating compressor clearance": "reciprocating_compressor_clearance_volume",
    "compressor dead space": "reciprocating_compressor_clearance_volume",
    "compressor dead volume": "reciprocating_compressor_clearance_volume",
    "compressor residual volume": "reciprocating_compressor_clearance_volume",
    "centrifugal compressor surge": "centrifugal_surge_control",
    "centrifugal anti surge": "centrifugal_surge_control",
    "compressor anti surge": "centrifugal_surge_control",
    "polytropic efficiency compressor": "polytropic_vs_isentropic_efficiency",
    "isentropic efficiency compressor": "polytropic_vs_isentropic_efficiency",
    "rod load compressor": "rod_load_analysis_reciprocating",
    "intercooler compressor": "intercooling_benefits_multistage",
    "compressor gas properties": "gas_properties_compression_performance",
    "compressor valve types": "compressor_valve_design_maintenance",
    "compressor packing": "packing_rider_ring_wear_mechanisms",
    "compressor rider ring": "packing_rider_ring_wear_mechanisms",
    "api 618 compressor": "api_618_recip_standards_compliance",
    "api 617 compressor": "api_617_centrifugal_standards_compliance",
    "compressor capacity control system": "capacity_control_methods_comparison",
    "compressor vibration monitoring": "vibration_monitoring_api_670",
    "screw compressor type": "screw_compressor_applications_limitations",
    "compressor compression ratio": "compression_ratio_calculation_multistage",
    "field gas compressor": "field_gas_compression_for_gas_lift",
    "gas dehydration unit": "gas_dehydration_before_compression",
    "compressor driver selection": "compressor_driver_selection_engine_motor_turbine",
    "compressor station design": "compressor_station_design_layout",
    "ngl recovery compressor": "ngl_recovery_compression_refrigeration",
    "gas gathering compressor": "gas_gathering_compression_systems",
}

SEMANTIC_MAP.update(extra_synonyms)

# Add more misspellings and variants for robustness
misspellings_extra = {
    "reciprocating compressor clearnce": "reciprocating_compressor_clearance_volume",
    "centrifugal surge cntrol": "centrifugal_surge_control",
    "polytropic vs isentropic efficency": "polytropic_vs_isentropic_efficiency",
    "rod load analisis": "rod_load_analysis_reciprocating",
    "intercooling benfits": "intercooling_benefits_multistage",
    "gas properties comprssion": "gas_properties_compression_performance",
    "compressor valve desgin": "compressor_valve_design_maintenance",
    "packing rider ring wear mechnisms": "packing_rider_ring_wear_mechanisms",
    "api 618 recip standards complience": "api_618_recip_standards_compliance",
    "api 617 centrifugal standards complience": "api_617_centrifugal_standards_compliance",
    "capacity control methods comparsion": "capacity_control_methods_comparison",
    "vibration monitoring api 6700": "vibration_monitoring_api_670",
    "screw compressor aplications": "screw_compressor_applications_limitations",
    "compression ratio calcuation": "compression_ratio_calculation_multistage",
    "field gas compression for gaslift": "field_gas_compression_for_gas_lift",
    "gas dehydraton before compression": "gas_dehydration_before_compression",
    "compressor driver selection engin motor turbine": "compressor_driver_selection_engine_motor_turbine",
    "compressor station desgin": "compressor_station_design_layout",
    "ngl recovery comprssion": "ngl_recovery_compression_refrigeration",
    "gas gathering comprssion": "gas_gathering_compression_systems",
}

SEMANTIC_MAP.update(misspellings_extra)

# Add more abbreviations and acronyms
abbreviations_extra = {
    "poly": "polytropic_vs_isentropic_efficiency",
    "iso": "polytropic_vs_isentropic_efficiency",
    "api 618": "api_618_recip_standards_compliance",
    "api 617": "api_617_centrifugal_standards_compliance",
    "api 670": "vibration_monitoring_api_670",
}

SEMANTIC_MAP.update(abbreviations_extra)

# Add more related terms
related_terms_extra = {
    "compressor clearance volume": "reciprocating_compressor_clearance_volume",
    "compressor surge": "centrifugal_surge_control",
    "compressor efficiency": "polytropic_vs_isentropic_efficiency",
    "compressor rod load": "rod_load_analysis_reciprocating",
    "compressor intercooling": "intercooling_benefits_multistage",
    "compressor gas performance": "gas_properties_compression_performance",
    "compressor valve maintenance": "compressor_valve_design_maintenance",
    "compressor packing ring": "packing_rider_ring_wear_mechanisms",
    "compressor api 618": "api_618_recip_standards_compliance",
    "compressor api 617": "api_617_centrifugal_standards_compliance",
    "compressor capacity control methods": "capacity_control_methods_comparison",
    "compressor vibration monitoring api 670": "vibration_monitoring_api_670",
    "compressor screw": "screw_compressor_applications_limitations",
    "compressor compression ratio calculation": "compression_ratio_calculation_multistage",
    "compressor field gas compression": "field_gas_compression_for_gas_lift",
    "compressor gas dehydration": "gas_dehydration_before_compression",
    "compressor driver selection engine": "compressor_driver_selection_engine_motor_turbine",
    "compressor station layout": "compressor_station_design_layout",
    "compressor ngl recovery": "ngl_recovery_compression_refrigeration",
    "compressor gas gathering": "gas_gathering_compression_systems",
}

SEMANTIC_MAP.update(related_terms_extra)

# Add more variants and misspellings for robustness
variants = {
    "recip compressor cv": "reciprocating_compressor_clearance_volume",
    "centrifugal anti-surge control": "centrifugal_surge_control",
    "polytropic efficiency vs isentropic efficiency": "polytropic_vs_isentropic_efficiency",
    "rod load analysis compressor": "rod_load_analysis_reciprocating",
    "intercooling stage compressor": "intercooling_benefits_multistage",
    "gas properties for compression performance": "gas_properties_compression_performance",
    "compressor valve design and maintenance": "compressor_valve_design_maintenance",
    "packing and rider ring wear mechanisms": "packing_rider_ring_wear_mechanisms",
    "api 618 reciprocating compressor standards compliance": "api_618_recip_standards_compliance",
    "api 617 centrifugal compressor standards compliance": "api_617_centrifugal_standards_compliance",
    "capacity control method comparison": "capacity_control_methods_comparison",
    "vibration monitoring api670": "vibration_monitoring_api_670",
    "screw compressor application and limitations": "screw_compressor_applications_limitations",
    "compression ratio calculation for multistage compressors": "compression_ratio_calculation_multistage",
    "field gas compression for gas lift operation": "field_gas_compression_for_gas_lift",
    "gas dehydration before compressor": "gas_dehydration_before_compression",
    "compressor driver selection (engine motor turbine)": "compressor_driver_selection_engine_motor_turbine",
    "compressor station design and layout": "compressor_station_design_layout",
    "ngl recovery compression and refrigeration": "ngl_recovery_compression_refrigeration",
    "gas gathering compression and systems": "gas_gathering_compression_systems",
}

SEMANTIC_MAP.update(variants)

# Add more synonyms and related terms for each domain (targeting 200+ entries)
synonyms_extra = {
    "reciprocating compressor clearance volume calculation": "reciprocating_compressor_clearance_volume",
    "centrifugal compressor surge control system": "centrifugal_surge_control",
    "polytropic efficiency vs isentropic efficiency comparison": "polytropic_vs_isentropic_efficiency",
    "rod load analysis for reciprocating compressors": "rod_load_analysis_reciprocating",
    "intercooling benefits for multistage compressors": "intercooling_benefits_multistage",
    "gas properties affecting compression performance": "gas_properties_compression_performance",
    "compressor valve design and maintenance procedures": "compressor_valve_design_maintenance",
    "packing and rider ring wear mechanisms in compressors": "packing_rider_ring_wear_mechanisms",
    "api 618 reciprocating compressor standards": "api_618_recip_standards_compliance",
    "api 617 centrifugal compressor standards": "api_617_centrifugal_standards_compliance",
    "capacity control methods for compressors": "capacity_control_methods_comparison",
    "vibration monitoring according to api 670": "vibration_monitoring_api_670",
    "screw compressor applications and limitations": "screw_compressor_applications_limitations",
    "compression ratio calculation for multistage compressor": "compression_ratio_calculation_multistage",
    "field gas compression for gas lift systems": "field_gas_compression_for_gas_lift",
    "gas dehydration before compression process": "gas_dehydration_before_compression",
    "compressor driver selection (engine, motor, turbine)": "compressor_driver_selection_engine_motor_turbine",
    "compressor station design and layout standards": "compressor_station_design_layout",
    "ngl recovery compression and refrigeration systems": "ngl_recovery_compression_refrigeration",
    "gas gathering compression systems design": "gas_gathering_compression_systems",
}

SEMANTIC_MAP.update(synonyms_extra)

# Finalize expected entry count
_EXPECTED_ENTRY_COUNT = len(SEMANTIC_MAP)

def _compute_map_hash() -> str:
    items = sorted(SEMANTIC_MAP.items())
    hash_input = "".join([f"{k}:{v}" for k, v in items])
    return hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

_MAP_INTEGRITY_HASH = _compute_map_hash()

def verify_integrity() -> dict:
    actual_count = len(SEMANTIC_MAP)
    actual_hash = _compute_map_hash()
    is_valid = (actual_count == _EXPECTED_ENTRY_COUNT) and (actual_hash == _MAP_INTEGRITY_HASH)
    return {
        "status": "valid" if is_valid else "invalid",
        "entries": actual_count,
        "hash": actual_hash,
        "is_valid": is_valid,
        "expected_count": _EXPECTED_ENTRY_COUNT,
        "expected_hash": _MAP_INTEGRITY_HASH,
    }

def _normalize_string(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9\s\-\(\),_/]", "", s)
    s = re.sub(r"\s+", " ", s)
    s = s.strip()
    return s

def normalize_term(term: str) -> str:
    norm = _normalize_string(term)
    return SEMANTIC_MAP.get(norm, norm)

def get_related_terms(term: str) -> list:
    norm = normalize_term(term)
    related = []
    for k, v in SEMANTIC_MAP.items():
        if v == norm and k != norm:
            related.append(k)
    return sorted(set(related))

def get_all_mappings() -> dict:
    return dict(SEMANTIC_MAP)

# For robustness, add normalization for common misspellings and variants
def _expand_term(term: str) -> str:
    norm = _normalize_string(term)
    if norm in SEMANTIC_MAP:
        return SEMANTIC_MAP[norm]
    # Try removing plural 's'
    if norm.endswith("s") and norm[:-1] in SEMANTIC_MAP:
        return SEMANTIC_MAP[norm[:-1]]
    # Try removing 'ing'
    if norm.endswith("ing") and norm[:-3] in SEMANTIC_MAP:
        return SEMANTIC_MAP[norm[:-3]]
    # Try removing 'ed'
    if norm.endswith("ed") and norm[:-2] in SEMANTIC_MAP:
        return SEMANTIC_MAP[norm[:-2]]
    # Try removing 'er'
    if norm.endswith("er") and norm[:-2] in SEMANTIC_MAP:
        return SEMANTIC_MAP[norm[:-2]]
    return norm

# Optionally, override normalize_term to use _expand_term for more robustness
normalize_term = _expand_term