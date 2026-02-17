import hashlib
import re

SEMANTIC_MAP_VERSION = "1.0.0"
SEMANTIC_MAP_AUTHOR = "AUTO14 Engineering Team"
SEMANTIC_MAP_ENGINE = "AUTO14_steering_systems"

SEMANTIC_MAP = {
    # Hydraulic Power Steering Fluid Contamination
    "hydraulic power steering fluid contamination": "hydraulic_ps_fluid_contamination",
    "ps fluid contamination": "hydraulic_ps_fluid_contamination",
    "power steering fluid contamination": "hydraulic_ps_fluid_contamination",
    "hydraulic fluid contamination": "hydraulic_ps_fluid_contamination",
    "steering fluid contamination": "hydraulic_ps_fluid_contamination",
    "psf contamination": "hydraulic_ps_fluid_contamination",
    "dirty ps fluid": "hydraulic_ps_fluid_contamination",
    "contaminated steering fluid": "hydraulic_ps_fluid_contamination",
    "hydraulic fluid dirty": "hydraulic_ps_fluid_contamination",
    "ps fluid dirty": "hydraulic_ps_fluid_contamination",
    "ps fluid impurities": "hydraulic_ps_fluid_contamination",
    "hydraulic fluid impurities": "hydraulic_ps_fluid_contamination",
    "psf impurities": "hydraulic_ps_fluid_contamination",
    "steering fluid impurities": "hydraulic_ps_fluid_contamination",
    "ps fluid debris": "hydraulic_ps_fluid_contamination",
    "hydraulic fluid debris": "hydraulic_ps_fluid_contamination",
    "psf debris": "hydraulic_ps_fluid_contamination",
    "fluid contamination": "hydraulic_ps_fluid_contamination",
    "ps fluid contamination symptoms": "hydraulic_ps_fluid_contamination",
    "ps fluid contamination diagnosis": "hydraulic_ps_fluid_contamination",

    # Electric Power Steering Torque Sensor Drift
    "electric power steering torque sensor drift": "eps_torque_sensor_drift",
    "eps torque sensor drift": "eps_torque_sensor_drift",
    "torque sensor drift": "eps_torque_sensor_drift",
    "steering torque sensor drift": "eps_torque_sensor_drift",
    "eps sensor drift": "eps_torque_sensor_drift",
    "torque sensor offset": "eps_torque_sensor_drift",
    "eps torque sensor offset": "eps_torque_sensor_drift",
    "eps sensor offset": "eps_torque_sensor_drift",
    "torque sensor calibration error": "eps_torque_sensor_drift",
    "eps torque sensor calibration error": "eps_torque_sensor_drift",
    "eps torque sensor miscalibration": "eps_torque_sensor_drift",
    "eps torque sensor bias": "eps_torque_sensor_drift",
    "eps torque sensor deviation": "eps_torque_sensor_drift",
    "eps torque sensor malfunction": "eps_torque_sensor_drift",
    "eps torque sensor failure": "eps_torque_sensor_drift",
    "eps torque sensor error": "eps_torque_sensor_drift",

    # Rack and Pinion Inner Tie Rod Wear
    "rack and pinion inner tie rod wear": "rack_pinion_inner_tie_rod_wear",
    "inner tie rod wear": "rack_pinion_inner_tie_rod_wear",
    "rack and pinion tie rod wear": "rack_pinion_inner_tie_rod_wear",
    "rack pinion tie rod wear": "rack_pinion_inner_tie_rod_wear",
    "tie rod wear": "rack_pinion_inner_tie_rod_wear",
    "inner tie rod failure": "rack_pinion_inner_tie_rod_wear",
    "rack pinion inner tie rod failure": "rack_pinion_inner_tie_rod_wear",
    "rack pinion tie rod failure": "rack_pinion_inner_tie_rod_wear",
    "tie rod end wear": "rack_pinion_inner_tie_rod_wear",
    "tie rod end failure": "rack_pinion_inner_tie_rod_wear",
    "rack pinion tie rod end wear": "rack_pinion_inner_tie_rod_wear",
    "rack pinion tie rod end failure": "rack_pinion_inner_tie_rod_wear",
    "rack pinion inner tie rod looseness": "rack_pinion_inner_tie_rod_wear",
    "inner tie rod looseness": "rack_pinion_inner_tie_rod_wear",
    "tie rod looseness": "rack_pinion_inner_tie_rod_wear",
    "rack pinion tie rod looseness": "rack_pinion_inner_tie_rod_wear",

    # Ackermann Steering Geometry Principles
    "ackermann steering geometry principles": "ackermann_steering_geometry",
    "ackermann geometry": "ackermann_steering_geometry",
    "ackermann principle": "ackermann_steering_geometry",
    "ackermann steering": "ackermann_steering_geometry",
    "ackermann angle": "ackermann_steering_geometry",
    "ackermann theory": "ackermann_steering_geometry",
    "ackermann steering geometry": "ackermann_steering_geometry",
    "ackermann": "ackermann_steering_geometry",
    "ackerman steering": "ackermann_steering_geometry",
    "ackerman geometry": "ackermann_steering_geometry",
    "ackerman principle": "ackermann_steering_geometry",
    "ackerman angle": "ackermann_steering_geometry",
    "ackerman steering geometry": "ackermann_steering_geometry",

    # Steer-by-Wire Redundancy Architecture
    "steer-by-wire redundancy architecture": "steer_by_wire_redundancy",
    "steer by wire redundancy": "steer_by_wire_redundancy",
    "sbw redundancy": "steer_by_wire_redundancy",
    "steer by wire backup": "steer_by_wire_redundancy",
    "steer by wire fail-safe": "steer_by_wire_redundancy",
    "steer by wire safety": "steer_by_wire_redundancy",
    "steer by wire redundant system": "steer_by_wire_redundancy",
    "steer by wire redundant architecture": "steer_by_wire_redundancy",
    "sbw redundant system": "steer_by_wire_redundancy",
    "sbw redundant architecture": "steer_by_wire_redundancy",
    "sbw fail-safe": "steer_by_wire_redundancy",
    "sbw backup": "steer_by_wire_redundancy",
    "sbw safety": "steer_by_wire_redundancy",
    "steer by wire backup system": "steer_by_wire_redundancy",

    # Steering Column Intermediate Shaft U-Joint Failure
    "steering column intermediate shaft u-joint failure": "steering_col_intermediate_shaft_u_joint_failure",
    "intermediate shaft u-joint failure": "steering_col_intermediate_shaft_u_joint_failure",
    "u-joint failure": "steering_col_intermediate_shaft_u_joint_failure",
    "steering u-joint failure": "steering_col_intermediate_shaft_u_joint_failure",
    "steering column u-joint failure": "steering_col_intermediate_shaft_u_joint_failure",
    "steering shaft u-joint failure": "steering_col_intermediate_shaft_u_joint_failure",
    "intermediate shaft u joint failure": "steering_col_intermediate_shaft_u_joint_failure",
    "u joint failure": "steering_col_intermediate_shaft_u_joint_failure",
    "steering u joint failure": "steering_col_intermediate_shaft_u_joint_failure",
    "steering column u joint failure": "steering_col_intermediate_shaft_u_joint_failure",
    "steering shaft u joint failure": "steering_col_intermediate_shaft_u_joint_failure",
    "intermediate shaft universal joint failure": "steering_col_intermediate_shaft_u_joint_failure",
    "universal joint failure": "steering_col_intermediate_shaft_u_joint_failure",
    "steering universal joint failure": "steering_col_intermediate_shaft_u_joint_failure",
    "steering column universal joint failure": "steering_col_intermediate_shaft_u_joint_failure",
    "steering shaft universal joint failure": "steering_col_intermediate_shaft_u_joint_failure",
    "intermediate shaft uj failure": "steering_col_intermediate_shaft_u_joint_failure",
    "steering uj failure": "steering_col_intermediate_shaft_u_joint_failure",

    # Power Steering Pump Flow and Pressure Testing
    "power steering pump flow and pressure testing": "ps_pump_flow_pressure_testing",
    "ps pump flow and pressure testing": "ps_pump_flow_pressure_testing",
    "ps pump testing": "ps_pump_flow_pressure_testing",
    "power steering pump testing": "ps_pump_flow_pressure_testing",
    "ps pump flow testing": "ps_pump_flow_pressure_testing",
    "ps pump pressure testing": "ps_pump_flow_pressure_testing",
    "ps pump test": "ps_pump_flow_pressure_testing",
    "power steering pump test": "ps_pump_flow_pressure_testing",
    "ps pump flow test": "ps_pump_flow_pressure_testing",
    "ps pump pressure test": "ps_pump_flow_pressure_testing",
    "ps pump flow measurement": "ps_pump_flow_pressure_testing",
    "ps pump pressure measurement": "ps_pump_flow_pressure_testing",
    "ps pump flow check": "ps_pump_flow_pressure_testing",
    "ps pump pressure check": "ps_pump_flow_pressure_testing",
    "ps pump flow and pressure check": "ps_pump_flow_pressure_testing",

    # Electric Power Steering Motor Current Draw Analysis
    "electric power steering motor current draw analysis": "eps_motor_current_draw_analysis",
    "eps motor current draw analysis": "eps_motor_current_draw_analysis",
    "eps motor current draw": "eps_motor_current_draw_analysis",
    "eps current draw analysis": "eps_motor_current_draw_analysis",
    "eps current draw": "eps_motor_current_draw_analysis",
    "eps motor current analysis": "eps_motor_current_draw_analysis",
    "eps motor current": "eps_motor_current_draw_analysis",
    "eps current analysis": "eps_motor_current_draw_analysis",
    "electric power steering current draw": "eps_motor_current_draw_analysis",
    "electric power steering motor current": "eps_motor_current_draw_analysis",
    "electric power steering current analysis": "eps_motor_current_draw_analysis",
    "eps motor amperage": "eps_motor_current_draw_analysis",
    "eps motor amp draw": "eps_motor_current_draw_analysis",
    "eps amp draw": "eps_motor_current_draw_analysis",
    "eps amperage": "eps_motor_current_draw_analysis",
    "eps motor amp analysis": "eps_motor_current_draw_analysis",

    # Toe Angle and Tire Wear Correlation
    "toe angle and tire wear correlation": "toe_angle_tire_wear_correlation",
    "toe angle tire wear correlation": "toe_angle_tire_wear_correlation",
    "toe angle tire wear": "toe_angle_tire_wear_correlation",
    "toe tire wear correlation": "toe_angle_tire_wear_correlation",
    "toe tire wear": "toe_angle_tire_wear_correlation",
    "toe angle wear": "toe_angle_tire_wear_correlation",
    "toe wear": "toe_angle_tire_wear_correlation",
    "toe angle tire wear relationship": "toe_angle_tire_wear_correlation",
    "toe tire wear relationship": "toe_angle_tire_wear_correlation",
    "toe angle tire wear effect": "toe_angle_tire_wear_correlation",
    "toe tire wear effect": "toe_angle_tire_wear_correlation",
    "toe angle tire wear impact": "toe_angle_tire_wear_correlation",
    "toe tire wear impact": "toe_angle_tire_wear_correlation",
    "toe angle tire wear cause": "toe_angle_tire_wear_correlation",
    "toe tire wear cause": "toe_angle_tire_wear_correlation",

    # Rack and Pinion Hydraulic Seal Leak Diagnosis
    "rack and pinion hydraulic seal leak diagnosis": "rack_pinion_hydraulic_seal_leak_diagnosis",
    "rack pinion hydraulic seal leak diagnosis": "rack_pinion_hydraulic_seal_leak_diagnosis",
    "rack and pinion seal leak diagnosis": "rack_pinion_hydraulic_seal_leak_diagnosis",
    "rack pinion seal leak diagnosis": "rack_pinion_hydraulic_seal_leak_diagnosis",
    "rack and pinion hydraulic seal leak": "rack_pinion_hydraulic_seal_leak_diagnosis",
    "rack pinion hydraulic seal leak": "rack_pinion_hydraulic_seal_leak_diagnosis",
    "rack and pinion seal leak": "rack_pinion_hydraulic_seal_leak_diagnosis",
    "rack pinion seal leak": "rack_pinion_hydraulic_seal_leak_diagnosis",
    "rack and pinion leak diagnosis": "rack_pinion_hydraulic_seal_leak_diagnosis",
    "rack pinion leak diagnosis": "rack_pinion_hydraulic_seal_leak_diagnosis",
    "rack and pinion leak": "rack_pinion_hydraulic_seal_leak_diagnosis",
    "rack pinion leak": "rack_pinion_hydraulic_seal_leak_diagnosis",
    "rack and pinion hydraulic leak": "rack_pinion_hydraulic_seal_leak_diagnosis",
    "rack pinion hydraulic leak": "rack_pinion_hydraulic_seal_leak_diagnosis",
    "rack and pinion seal failure": "rack_pinion_hydraulic_seal_leak_diagnosis",
    "rack pinion seal failure": "rack_pinion_hydraulic_seal_leak_diagnosis",

    # Steering Angle Sensor Calibration Procedures
    "steering angle sensor calibration procedures": "steering_angle_sensor_calibration",
    "steering angle sensor calibration": "steering_angle_sensor_calibration",
    "steering angle sensor calibrate": "steering_angle_sensor_calibration",
    "steering angle sensor calibration procedure": "steering_angle_sensor_calibration",
    "steering angle sensor calibration steps": "steering_angle_sensor_calibration",
    "steering angle sensor calibration method": "steering_angle_sensor_calibration",
    "steering angle sensor calibration process": "steering_angle_sensor_calibration",
    "steering angle sensor calibration instructions": "steering_angle_sensor_calibration",
    "steering angle sensor calibration guide": "steering_angle_sensor_calibration",
    "steering angle sensor calibration how to": "steering_angle_sensor_calibration",
    "steering angle sensor calibration technique": "steering_angle_sensor_calibration",
    "steering angle sensor calibration requirements": "steering_angle_sensor_calibration",
    "steering angle sensor calibration tools": "steering_angle_sensor_calibration",
    "steering angle sensor calibration equipment": "steering_angle_sensor_calibration",

    # Variable Ratio Steering Analysis
    "variable ratio steering analysis": "variable_ratio_steering_analysis",
    "variable ratio steering": "variable_ratio_steering_analysis",
    "variable steering ratio": "variable_ratio_steering_analysis",
    "variable ratio steering system": "variable_ratio_steering_analysis",
    "variable ratio steering mechanism": "variable_ratio_steering_analysis",
    "variable ratio steering effect": "variable_ratio_steering_analysis",
    "variable ratio steering impact": "variable_ratio_steering_analysis",
    "variable ratio steering function": "variable_ratio_steering_analysis",
    "variable ratio steering operation": "variable_ratio_steering_analysis",
    "variable ratio steering performance": "variable_ratio_steering_analysis",
    "variable ratio steering evaluation": "variable_ratio_steering_analysis",
    "variable ratio steering review": "variable_ratio_steering_analysis",
    "variable ratio steering comparison": "variable_ratio_steering_analysis",
    "variable ratio steering pros": "variable_ratio_steering_analysis",
    "variable ratio steering cons": "variable_ratio_steering_analysis",

    # Power Steering Hose Pressure Rating and Failure
    "power steering hose pressure rating and failure": "ps_hose_pressure_rating_failure",
    "ps hose pressure rating and failure": "ps_hose_pressure_rating_failure",
    "ps hose pressure rating": "ps_hose_pressure_rating_failure",
    "ps hose failure": "ps_hose_pressure_rating_failure",
    "power steering hose pressure rating": "ps_hose_pressure_rating_failure",
    "power steering hose failure": "ps_hose_pressure_rating_failure",
    "ps hose burst": "ps_hose_pressure_rating_failure",
    "ps hose rupture": "ps_hose_pressure_rating_failure",
    "ps hose leak": "ps_hose_pressure_rating_failure",
    "power steering hose burst": "ps_hose_pressure_rating_failure",
    "power steering hose rupture": "ps_hose_pressure_rating_failure",
    "power steering hose leak": "ps_hose_pressure_rating_failure",
    "ps hose pressure failure": "ps_hose_pressure_rating_failure",
    "ps hose pressure loss": "ps_hose_pressure_rating_failure",
    "ps hose pressure drop": "ps_hose_pressure_rating_failure",
    "ps hose pressure test": "ps_hose_pressure_rating_failure",

    # EPS Motor Position Sensor Hall Effect Failure
    "eps motor position sensor hall effect failure": "eps_motor_position_sensor_hall_failure",
    "eps position sensor hall effect failure": "eps_motor_position_sensor_hall_failure",
    "eps hall effect sensor failure": "eps_motor_position_sensor_hall_failure",
    "eps motor hall effect sensor failure": "eps_motor_position_sensor_hall_failure",
    "eps hall sensor failure": "eps_motor_position_sensor_hall_failure",
    "eps motor hall sensor failure": "eps_motor_position_sensor_hall_failure",
    "eps position sensor hall failure": "eps_motor_position_sensor_hall_failure",
    "eps motor position sensor hall failure": "eps_motor_position_sensor_hall_failure",
    "eps hall effect failure": "eps_motor_position_sensor_hall_failure",
    "eps hall failure": "eps_motor_position_sensor_hall_failure",
    "eps motor hall effect failure": "eps_motor_position_sensor_hall_failure",
    "eps motor hall failure": "eps_motor_position_sensor_hall_failure",
    "eps hall sensor malfunction": "eps_motor_position_sensor_hall_failure",
    "eps motor hall sensor malfunction": "eps_motor_position_sensor_hall_failure",
    "eps hall effect sensor malfunction": "eps_motor_position_sensor_hall_failure",

    # Kingpin Inclination and Scrub Radius Effects
    "kingpin inclination and scrub radius effects": "kingpin_inclination_scrub_radius_effects",
    "kingpin inclination scrub radius effects": "kingpin_inclination_scrub_radius_effects",
    "kingpin inclination effects": "kingpin_inclination_scrub_radius_effects",
    "scrub radius effects": "kingpin_inclination_scrub_radius_effects",
    "kingpin inclination": "kingpin_inclination_scrub_radius_effects",
    "scrub radius": "kingpin_inclination_scrub_radius_effects",
    "kingpin inclination impact": "kingpin_inclination_scrub_radius_effects",
    "scrub radius impact": "kingpin_inclination_scrub_radius_effects",
    "kingpin inclination function": "kingpin_inclination_scrub_radius_effects",
    "scrub radius function": "kingpin_inclination_scrub_radius_effects",
    "kingpin inclination performance": "kingpin_inclination_scrub_radius_effects",
    "scrub radius performance": "kingpin_inclination_scrub_radius_effects",
    "kingpin inclination review": "kingpin_inclination_scrub_radius_effects",
    "scrub radius review": "kingpin_inclination_scrub_radius_effects",

    # Steering Column Tilt and Telescoping Mechanism Failure
    "steering column tilt and telescoping mechanism failure": "steering_col_tilt_telescoping_failure",
    "steering column tilt telescoping failure": "steering_col_tilt_telescoping_failure",
    "steering column tilt failure": "steering_col_tilt_telescoping_failure",
    "steering column telescoping failure": "steering_col_tilt_telescoping_failure",
    "steering column tilt mechanism failure": "steering_col_tilt_telescoping_failure",
    "steering column telescoping mechanism failure": "steering_col_tilt_telescoping_failure",
    "steering column tilt mechanism malfunction": "steering_col_tilt_telescoping_failure",
    "steering column telescoping mechanism malfunction": "steering_col_tilt_telescoping_failure",
    "steering column tilt malfunction": "steering_col_tilt_telescoping_failure",
    "steering column telescoping malfunction": "steering_col_tilt_telescoping_failure",
    "steering column tilt mechanism defect": "steering_col_tilt_telescoping_failure",
    "steering column telescoping mechanism defect": "steering_col_tilt_telescoping_failure",
    "steering column tilt defect": "steering_col_tilt_telescoping_failure",
    "steering column telescoping defect": "steering_col_tilt_telescoping_failure",

    # Active Return-to-Center Steering Analysis
    "active return-to-center steering analysis": "active_return_to_center_steering_analysis",
    "active return to center steering analysis": "active_return_to_center_steering_analysis",
    "active return to center steering": "active_return_to_center_steering_analysis",
    "active return-to-center steering": "active_return_to_center_steering_analysis",
    "active return to center": "active_return_to_center_steering_analysis",
    "active return-to-center": "active_return_to_center_steering_analysis",
    "active return to center function": "active_return_to_center_steering_analysis",
    "active return-to-center function": "active_return_to_center_steering_analysis",
    "active return to center mechanism": "active_return_to_center_steering_analysis",
    "active return-to-center mechanism": "active_return_to_center_steering_analysis",
    "active return to center operation": "active_return_to_center_steering_analysis",
    "active return-to-center operation": "active_return_to_center_steering_analysis",
    "active return to center review": "active_return_to_center_steering_analysis",
    "active return-to-center review": "active_return_to_center_steering_analysis",

    # Rack and Pinion Mounting Bushing Wear
    "rack and pinion mounting bushing wear": "rack_pinion_mounting_bushing_wear",
    "rack pinion mounting bushing wear": "rack_pinion_mounting_bushing_wear",
    "rack and pinion bushing wear": "rack_pinion_mounting_bushing_wear",
    "rack pinion bushing wear": "rack_pinion_mounting_bushing_wear",
    "rack and pinion mounting bushing failure": "rack_pinion_mounting_bushing_wear",
    "rack pinion mounting bushing failure": "rack_pinion_mounting_bushing_wear",
    "rack and pinion bushing failure": "rack_pinion_mounting_bushing_wear",
    "rack pinion bushing failure": "rack_pinion_mounting_bushing_wear",
    "rack and pinion mounting bushing looseness": "rack_pinion_mounting_bushing_wear",
    "rack pinion mounting bushing looseness": "rack_pinion_mounting_bushing_wear",
    "rack and pinion bushing looseness": "rack_pinion_mounting_bushing_wear",
    "rack pinion bushing looseness": "rack_pinion_mounting_bushing_wear",

    # EPS Column-Assist vs Rack-Assist Architecture
    "eps column-assist vs rack-assist architecture": "eps_column_assist_vs_rack_assist",
    "eps column assist vs rack assist architecture": "eps_column_assist_vs_rack_assist",
    "eps column assist vs rack assist": "eps_column_assist_vs_rack_assist",
    "eps column-assist vs rack-assist": "eps_column_assist_vs_rack_assist",
    "eps column assist architecture": "eps_column_assist_vs_rack_assist",
    "eps rack assist architecture": "eps_column_assist_vs_rack_assist",
    "eps column assist": "eps_column_assist_vs_rack_assist",
    "eps rack assist": "eps_column_assist_vs_rack_assist",
    "eps column vs rack assist": "eps_column_assist_vs_rack_assist",
    "eps column vs rack assist architecture": "eps_column_assist_vs_rack_assist",
    "eps column vs rack assist comparison": "eps_column_assist_vs_rack_assist",
    "eps column vs rack assist review": "eps_column_assist_vs_rack_assist",

    # Hydraulic Power Steering Pump Belt Failure Effects
    "hydraulic power steering pump belt failure effects": "hydraulic_ps_pump_belt_failure_effects",
    "ps pump belt failure effects": "hydraulic_ps_pump_belt_failure_effects",
    "power steering pump belt failure effects": "hydraulic_ps_pump_belt_failure_effects",
    "hydraulic pump belt failure effects": "hydraulic_ps_pump_belt_failure_effects",
    "ps pump belt failure": "hydraulic_ps_pump_belt_failure_effects",
    "power steering pump belt failure": "hydraulic_ps_pump_belt_failure_effects",
    "hydraulic pump belt failure": "hydraulic_ps_pump_belt_failure_effects",
    "ps pump belt break": "hydraulic_ps_pump_belt_failure_effects",
    "power steering pump belt break": "hydraulic_ps_pump_belt_failure_effects",
    "hydraulic pump belt break": "hydraulic_ps_pump_belt_failure_effects",
    "ps pump belt snapped": "hydraulic_ps_pump_belt_failure_effects",
    "power steering pump belt snapped": "hydraulic_ps_pump_belt_failure_effects",
    "hydraulic pump belt snapped": "hydraulic_ps_pump_belt_failure_effects",
    "ps pump belt malfunction": "hydraulic_ps_pump_belt_failure_effects",
    "power steering pump belt malfunction": "hydraulic_ps_pump_belt_failure_effects",
    "hydraulic pump belt malfunction": "hydraulic_ps_pump_belt_failure_effects",

    # Steering Wheel Vibration Diagnosis (Shimmy vs Shake)
    "steering wheel vibration diagnosis": "steering_wheel_vibration_diagnosis",
    "steering wheel vibration": "steering_wheel_vibration_diagnosis",
    "steering wheel shimmy": "steering_wheel_vibration_diagnosis",
    "steering wheel shake": "steering_wheel_vibration_diagnosis",
    "steering vibration": "steering_wheel_vibration_diagnosis",
    "steering shake": "steering_wheel_vibration_diagnosis",
    "steering shimmy": "steering_wheel_vibration_diagnosis",
    "steering wheel vibration analysis": "steering_wheel_vibration_diagnosis",
    "steering wheel vibration test": "steering_wheel_vibration_diagnosis",
    "steering wheel vibration troubleshooting": "steering_wheel_vibration_diagnosis",
    "steering wheel vibration cause": "steering_wheel_vibration_diagnosis",
    "steering wheel vibration symptom": "steering_wheel_vibration_diagnosis",
    "steering wheel vibration effect": "steering_wheel_vibration_diagnosis",
    "steering wheel vibration impact": "steering_wheel_vibration_diagnosis",
    "steering wheel vibration correction": "steering_wheel_vibration_diagnosis",

    # Active Front Steering (AFS) Planetary Gear System
    "active front steering planetary gear system": "active_front_steering_planetary_gear_system",
    "active front steering (afs) planetary gear system": "active_front_steering_planetary_gear_system",
    "afs planetary gear system": "active_front_steering_planetary_gear_system",
    "active front steering planetary gear": "active_front_steering_planetary_gear_system",
    "afs planetary gear": "active_front_steering_planetary_gear_system",
    "active front steering gear system": "active_front_steering_planetary_gear_system",
    "afs gear system": "active_front_steering_planetary_gear_system",
    "active front steering gear": "active_front_steering_planetary_gear_system",
    "afs gear": "active_front_steering_planetary_gear_system",
    "active front steering planetary": "active_front_steering_planetary_gear_system",
    "afs planetary": "active_front_steering_planetary_gear_system",
    "active front steering system": "active_front_steering_planetary_gear_system",
    "afs system": "active_front_steering_planetary_gear_system",

    # Steering Gear Ratio Calculation and Effects
    "steering gear ratio calculation and effects": "steering_gear_ratio_calculation_effects",
    "steering gear ratio calculation": "steering_gear_ratio_calculation_effects",
    "steering gear ratio effects": "steering_gear_ratio_calculation_effects",
    "steering gear ratio": "steering_gear_ratio_calculation_effects",
    "gear ratio calculation": "steering_gear_ratio_calculation_effects",
    "gear ratio effects": "steering_gear_ratio_calculation_effects",
    "gear ratio": "steering_gear_ratio_calculation_effects",
    "steering ratio calculation": "steering_gear_ratio_calculation_effects",
    "steering ratio effects": "steering_gear_ratio_calculation_effects",
    "steering ratio": "steering_gear_ratio_calculation_effects",
    "steering gear ratio function": "steering_gear_ratio_calculation_effects",
    "steering gear ratio impact": "steering_gear_ratio_calculation_effects",
    "steering gear ratio review": "steering_gear_ratio_calculation_effects",
    "steering gear ratio comparison": "steering_gear_ratio_calculation_effects",

    # EPS Thermal Management and Overheating Protection
    "eps thermal management and overheating protection": "eps_thermal_management_overheating_protection",
    "eps thermal management": "eps_thermal_management_overheating_protection",
    "eps overheating protection": "eps_thermal_management_overheating_protection",
    "eps thermal protection": "eps_thermal_management_overheating_protection",
    "eps overheating": "eps_thermal_management_overheating_protection",
    "eps thermal management system": "eps_thermal_management_overheating_protection",
    "eps overheating protection system": "eps_thermal_management_overheating_protection",
    "eps thermal protection system": "eps_thermal_management_overheating_protection",
    "eps overheating system": "eps_thermal_management_overheating_protection",
    "eps thermal management function": "eps_thermal_management_overheating_protection",
    "eps overheating protection function": "eps_thermal_management_overheating_protection",
    "eps thermal protection function": "eps_thermal_management_overheating_protection",
    "eps overheating function": "eps_thermal_management_overheating_protection",
    "eps thermal management review": "eps_thermal_management_overheating_protection",
    "eps overheating protection review": "eps_thermal_management_overheating_protection",

    # Four-Wheel Steering (4WS) Rear Steering Control
    "four-wheel steering rear steering control": "four_wheel_steering_rear_control",
    "four wheel steering rear steering control": "four_wheel_steering_rear_control",
    "four-wheel steering (4ws) rear steering control": "four_wheel_steering_rear_control",
    "4ws rear steering control": "four_wheel_steering_rear_control",
    "four-wheel steering rear control": "four_wheel_steering_rear_control",
    "four wheel steering rear control": "four_wheel_steering_rear_control",
    "4ws rear control": "four_wheel_steering_rear_control",
    "four-wheel steering rear steering": "four_wheel_steering_rear_control",
    "four wheel steering rear steering": "four_wheel_steering_rear_control",
    "4ws rear steering": "four_wheel_steering_rear_control",
    "four-wheel steering control": "four_wheel_steering_rear_control",
    "four wheel steering control": "four_wheel_steering_rear_control",
    "4ws control": "four_wheel_steering_rear_control",

    # Steering Column Bearing Noise Diagnosis
    "steering column bearing noise diagnosis": "steering_col_bearing_noise_diagnosis",
    "steering column bearing noise": "steering_col_bearing_noise_diagnosis",
    "steering column bearing diagnosis": "steering_col_bearing_noise_diagnosis",
    "steering column bearing noise test": "steering_col_bearing_noise_diagnosis",
    "steering column bearing noise troubleshooting": "steering_col_bearing_noise_diagnosis",
    "steering column bearing noise cause": "steering_col_bearing_noise_diagnosis",
    "steering column bearing noise symptom": "steering_col_bearing_noise_diagnosis",
    "steering column bearing noise effect": "steering_col_bearing_noise_diagnosis",
    "steering column bearing noise impact": "steering_col_bearing_noise_diagnosis",
    "steering column bearing noise correction": "steering_col_bearing_noise_diagnosis",
    "steering column bearing noise review": "steering_col_bearing_noise_diagnosis",
    "steering column bearing noise comparison": "steering_col_bearing_noise_diagnosis",

    # Bump Steer Analysis and Correction
    "bump steer analysis and correction": "bump_steer_analysis_correction",
    "bump steer analysis": "bump_steer_analysis_correction",
    "bump steer correction": "bump_steer_analysis_correction",
    "bump steer": "bump_steer_analysis_correction",
    "bump steer test": "bump_steer_analysis_correction",
    "bump steer troubleshooting": "bump_steer_analysis_correction",
    "bump steer cause": "bump_steer_analysis_correction",
    "bump steer symptom": "bump_steer_analysis_correction",
    "bump steer effect": "bump_steer_analysis_correction",
    "bump steer impact": "bump_steer_analysis_correction",
    "bump steer review": "bump_steer_analysis_correction",
    "bump steer comparison": "bump_steer_analysis_correction",

    # Add misspellings, abbreviations, synonyms, and related terms for coverage
    "hydraulic power steering contamination": "hydraulic_ps_fluid_contamination",
    "hydraulic steering fluid contamination": "hydraulic_ps_fluid_contamination",
    "hydraulic ps fluid contamination": "hydraulic_ps_fluid_contamination",
    "hydraulic psf contamination": "hydraulic_ps_fluid_contamination",
    "psf dirty": "hydraulic_ps_fluid_contamination",
    "psf impurities": "hydraulic_ps_fluid_contamination",
    "psf debris": "hydraulic_ps_fluid_contamination",
    "psf diagnosis": "hydraulic_ps_fluid_contamination",
    "psf symptoms": "hydraulic_ps_fluid_contamination",
    "psf test": "hydraulic_ps_fluid_contamination",
    "psf check": "hydraulic_ps_fluid_contamination",

    "eps torque sensor drift diagnosis": "eps_torque_sensor_drift",
    "eps torque sensor drift symptoms": "eps_torque_sensor_drift",
    "eps torque sensor drift test": "eps_torque_sensor_drift",
    "eps torque sensor drift check": "eps_torque_sensor_drift",
    "eps torque sensor drift troubleshooting": "eps_torque_sensor_drift",
    "eps torque sensor drift correction": "eps_torque_sensor_drift",

    "inner tie rod diagnosis": "rack_pinion_inner_tie_rod_wear",
    "inner tie rod symptoms": "rack_pinion_inner_tie_rod_wear",
    "inner tie rod test": "rack_pinion_inner_tie_rod_wear",
    "inner tie rod check": "rack_pinion_inner_tie_rod_wear",
    "inner tie rod troubleshooting": "rack_pinion_inner_tie_rod_wear",
    "inner tie rod correction": "rack_pinion_inner_tie_rod_wear",

    "ackermann steering geometry diagnosis": "ackermann_steering_geometry",
    "ackermann steering geometry test": "ackermann_steering_geometry",
    "ackermann steering geometry review": "ackermann_steering_geometry",
    "ackermann steering geometry comparison": "ackermann_steering_geometry",
    "ackermann steering geometry effect": "ackermann_steering_geometry",
    "ackermann steering geometry impact": "ackermann_steering_geometry",

    "sbw diagnosis": "steer_by_wire_redundancy",
    "sbw test": "steer_by_wire_redundancy",
    "sbw review": "steer_by_wire_redundancy",
    "sbw comparison": "steer_by_wire_redundancy",
    "sbw effect": "steer_by_wire_redundancy",
    "sbw impact": "steer_by_wire_redundancy",

    "u-joint diagnosis": "steering_col_intermediate_shaft_u_joint_failure",
    "u-joint test": "steering_col_intermediate_shaft_u_joint_failure",
    "u-joint review": "steering_col_intermediate_shaft_u_joint_failure",
    "u-joint comparison": "steering_col_intermediate_shaft_u_joint_failure",
    "u-joint effect": "steering_col_intermediate_shaft_u_joint_failure",
    "u-joint impact": "steering_col_intermediate_shaft_u_joint_failure",

    "ps pump diagnosis": "ps_pump_flow_pressure_testing",
    "ps pump test": "ps_pump_flow_pressure_testing",
    "ps pump review": "ps_pump_flow_pressure_testing",
    "ps pump comparison": "ps_pump_flow_pressure_testing",
    "ps pump effect": "ps_pump_flow_pressure_testing",
    "ps pump impact": "ps_pump_flow_pressure_testing",

    "eps motor diagnosis": "eps_motor_current_draw_analysis",
    "eps motor test": "eps_motor_current_draw_analysis",
    "eps motor review": "eps_motor_current_draw_analysis",
    "eps motor comparison": "eps_motor_current_draw_analysis",
    "eps motor effect": "eps_motor_current_draw_analysis",
    "eps motor impact": "eps_motor_current_draw_analysis",

    "toe angle diagnosis": "toe_angle_tire_wear_correlation",
    "toe angle test": "toe_angle_tire_wear_correlation",
    "toe angle review": "toe_angle_tire_wear_correlation",
    "toe angle comparison": "toe_angle_tire_wear_correlation",
    "toe angle effect": "toe_angle_tire_wear_correlation",
    "toe angle impact": "toe_angle_tire_wear_correlation",

    "rack pinion diagnosis": "rack_pinion_hydraulic_seal_leak_diagnosis",
    "rack pinion test": "rack_pinion_hydraulic_seal_leak_diagnosis",
    "rack pinion review": "rack_pinion_hydraulic_seal_leak_diagnosis",
    "rack pinion comparison": "rack_pinion_hydraulic_seal_leak_diagnosis",
    "rack pinion effect": "rack_pinion_hydraulic_seal_leak_diagnosis",
    "rack pinion impact": "rack_pinion_hydraulic_seal_leak_diagnosis",

    "steering angle sensor diagnosis": "steering_angle_sensor_calibration",
    "steering angle sensor test": "steering_angle_sensor_calibration",
    "steering angle sensor review": "steering_angle_sensor_calibration",
    "steering angle sensor comparison": "steering_angle_sensor_calibration",
    "steering angle sensor effect": "steering_angle_sensor_calibration",
    "steering angle sensor impact": "steering_angle_sensor_calibration",

    "variable ratio diagnosis": "variable_ratio_steering_analysis",
    "variable ratio test": "variable_ratio_steering_analysis",
    "variable ratio review": "variable_ratio_steering_analysis",
    "variable ratio comparison": "variable_ratio_steering_analysis",
    "variable ratio effect": "variable_ratio_steering_analysis",
    "variable ratio impact": "variable_ratio_steering_analysis",

    "ps hose diagnosis": "ps_hose_pressure_rating_failure",
    "ps hose test": "ps_hose_pressure_rating_failure",
    "ps hose review": "ps_hose_pressure_rating_failure",
    "ps hose comparison": "ps_hose_pressure_rating_failure",
    "ps hose effect": "ps_hose_pressure_rating_failure",
    "ps hose impact": "ps_hose_pressure_rating_failure",

    "eps hall diagnosis": "eps_motor_position_sensor_hall_failure",
    "eps hall test": "eps_motor_position_sensor_hall_failure",
    "eps hall review": "eps_motor_position_sensor_hall_failure",
    "eps hall comparison": "eps_motor_position_sensor_hall_failure",
    "eps hall effect": "eps_motor_position_sensor_hall_failure",
    "eps hall impact": "eps_motor_position_sensor_hall_failure",

    "kingpin inclination diagnosis": "kingpin_inclination_scrub_radius_effects",
    "kingpin inclination test": "kingpin_inclination_scrub_radius_effects",
    "kingpin inclination review": "kingpin_inclination_scrub_radius_effects",
    "kingpin inclination comparison": "kingpin_inclination_scrub_radius_effects",
    "kingpin inclination effect": "kingpin_inclination_scrub_radius_effects",
    "kingpin inclination impact": "kingpin_inclination_scrub_radius_effects",

    "scrub radius diagnosis": "kingpin_inclination_scrub_radius_effects",
    "scrub radius test": "kingpin_inclination_scrub_radius_effects",
    "scrub radius review": "kingpin_inclination_scrub_radius_effects",
    "scrub radius comparison": "kingpin_inclination_scrub_radius_effects",
    "scrub radius effect": "kingpin_inclination_scrub_radius_effects",
    "scrub radius impact": "kingpin_inclination_scrub_radius_effects",

    "steering column tilt diagnosis": "steering_col_tilt_telescoping_failure",
    "steering column tilt test": "steering_col_tilt_telescoping_failure",
    "steering column tilt review": "steering_col_tilt_telescoping_failure",
    "steering column tilt comparison": "steering_col_tilt_telescoping_failure",
    "steering column tilt effect": "steering_col_tilt_telescoping_failure",
    "steering column tilt impact": "steering_col_tilt_telescoping_failure",

    "steering column telescoping diagnosis": "steering_col_tilt_telescoping_failure",
    "steering column telescoping test": "steering_col_tilt_telescoping_failure",
    "steering column telescoping review": "steering_col_tilt_telescoping_failure",
    "steering column telescoping comparison": "steering_col_tilt_telescoping_failure",
    "steering column telescoping effect": "steering_col_tilt_telescoping_failure",
    "steering column telescoping impact": "steering_col_tilt_telescoping_failure",

    "active return to center diagnosis": "active_return_to_center_steering_analysis",
    "active return to center test": "active_return_to_center_steering_analysis",
    "active return to center review": "active_return_to_center_steering_analysis",
    "active return to center comparison": "active_return_to_center_steering_analysis",
    "active return to center effect": "active_return_to_center_steering_analysis",
    "active return to center impact": "active_return_to_center_steering_analysis",

    "rack pinion mounting bushing diagnosis": "rack_pinion_mounting_bushing_wear",
    "rack pinion mounting bushing test": "rack_pinion_mounting_bushing_wear",
    "rack pinion mounting bushing review": "rack_pinion_mounting_bushing_wear",
    "rack pinion mounting bushing comparison": "rack_pinion_mounting_bushing_wear",
    "rack pinion mounting bushing effect": "rack_pinion_mounting_bushing_wear",
    "rack pinion mounting bushing impact": "rack_pinion_mounting_bushing_wear",

    "eps column assist diagnosis": "eps_column_assist_vs_rack_assist",
    "eps column assist test": "eps_column_assist_vs_rack_assist",
    "eps column assist review": "eps_column_assist_vs_rack_assist",
    "eps column assist comparison": "eps_column_assist_vs_rack_assist",
    "eps column assist effect": "eps_column_assist_vs_rack_assist",
    "eps column assist impact": "eps_column_assist_vs_rack_assist",

    "eps rack assist diagnosis": "eps_column_assist_vs_rack_assist",
    "eps rack assist test": "eps_column_assist_vs_rack_assist",
    "eps rack assist review": "eps_column_assist_vs_rack_assist",
    "eps rack assist comparison": "eps_column_assist_vs_rack_assist",
    "eps rack assist effect": "eps_column_assist_vs_rack_assist",
    "eps rack assist impact": "eps_column_assist_vs_rack_assist",

    "hydraulic ps pump belt diagnosis": "hydraulic_ps_pump_belt_failure_effects",
    "hydraulic ps pump belt test": "hydraulic_ps_pump_belt_failure_effects",
    "hydraulic ps pump belt review": "hydraulic_ps_pump_belt_failure_effects",
    "hydraulic ps pump belt comparison": "hydraulic_ps_pump_belt_failure_effects",
    "hydraulic ps pump belt effect": "hydraulic_ps_pump_belt_failure_effects",
    "hydraulic ps pump belt impact": "hydraulic_ps_pump_belt_failure_effects",

    "steering wheel vibration diagnosis": "steering_wheel_vibration_diagnosis",
    "steering wheel vibration test": "steering_wheel_vibration_diagnosis",
    "steering wheel vibration review": "steering_wheel_vibration_diagnosis",
    "steering wheel vibration comparison": "steering_wheel_vibration_diagnosis",
    "steering wheel vibration effect": "steering_wheel_vibration_diagnosis",
    "steering wheel vibration impact": "steering_wheel_vibration_diagnosis",

    "afs diagnosis": "active_front_steering_planetary_gear_system",
    "afs test": "active_front_steering_planetary_gear_system",
    "afs review": "active_front_steering_planetary_gear_system",
    "afs comparison": "active_front_steering_planetary_gear_system",
    "afs effect": "active_front_steering_planetary_gear_system",
    "afs impact": "active_front_steering_planetary_gear_system",

    "steering gear ratio diagnosis": "steering_gear_ratio_calculation_effects",
    "steering gear ratio test": "steering_gear_ratio_calculation_effects",
    "steering gear ratio review": "steering_gear_ratio_calculation_effects",
    "steering gear ratio comparison": "steering_gear_ratio_calculation_effects",
    "steering gear ratio effect": "steering_gear_ratio_calculation_effects",
    "steering gear ratio impact": "steering_gear_ratio_calculation_effects",

    "eps thermal management diagnosis": "eps_thermal_management_overheating_protection",
    "eps thermal management test": "eps_thermal_management_overheating_protection",
    "eps thermal management review": "eps_thermal_management_overheating_protection",
    "eps thermal management comparison": "eps_thermal_management_overheating_protection",
    "eps thermal management effect": "eps_thermal_management_overheating_protection",
    "eps thermal management impact": "eps_thermal_management_overheating_protection",

    "eps overheating protection diagnosis": "eps_thermal_management_overheating_protection",
    "eps overheating protection test": "eps_thermal_management_overheating_protection",
    "eps overheating protection review": "eps_thermal_management_overheating_protection",
    "eps overheating protection comparison": "eps_thermal_management_overheating_protection",
    "eps overheating protection effect": "eps_thermal_management_overheating_protection",
    "eps overheating protection impact": "eps_thermal_management_overheating_protection",

    "4ws diagnosis": "four_wheel_steering_rear_control",
    "4ws test": "four_wheel_steering_rear_control",
    "4ws review": "four_wheel_steering_rear_control",
    "4ws comparison": "four_wheel_steering_rear_control",
    "4ws effect": "four_wheel_steering_rear_control",
    "4ws impact": "four_wheel_steering_rear_control",

    "steering column bearing diagnosis": "steering_col_bearing_noise_diagnosis",
    "steering column bearing test": "steering_col_bearing_noise_diagnosis",
    "steering column bearing review": "steering_col_bearing_noise_diagnosis",
    "steering column bearing comparison": "steering_col_bearing_noise_diagnosis",
    "steering column bearing effect": "steering_col_bearing_noise_diagnosis",
    "steering column bearing impact": "steering_col_bearing_noise_diagnosis",

    "bump steer diagnosis": "bump_steer_analysis_correction",
    "bump steer test": "bump_steer_analysis_correction",
    "bump steer review": "bump_steer_analysis_correction",
    "bump steer comparison": "bump_steer_analysis_correction",
    "bump steer effect": "bump_steer_analysis_correction",
    "bump steer impact": "bump_steer_analysis_correction",
}

_EXPECTED_ENTRY_COUNT = len(SEMANTIC_MAP)

def _compute_map_hash():
    items = sorted(SEMANTIC_MAP.items())
    map_str = "".join(f"{k}:{v};" for k, v in items)
    return hashlib.sha256(map_str.encode("utf-8")).hexdigest()

_MAP_INTEGRITY_HASH = _compute_map_hash()

def verify_integrity():
    actual_count = len(SEMANTIC_MAP)
    actual_hash = _compute_map_hash()
    is_valid = (actual_count == _EXPECTED_ENTRY_COUNT) and (actual_hash == _MAP_INTEGRITY_HASH)
    return {
        "status": "valid" if is_valid else "invalid",
        "entries": actual_count,
        "hash": actual_hash,
        "is_valid": is_valid
    }

def normalize_term(term: str) -> str:
    t = term.lower().strip()
    t = re.sub(r"[\(\)]", "", t)
    t = re.sub(r"[\s\-]+", " ", t)
    t = t.replace("  ", " ")
    t = t.replace("vs.", "vs")
    t = t.replace("vs ", "vs ")
    t = t.replace("fail safe", "fail-safe")
    t = t.replace("u joint", "u-joint")
    t = t.replace("psf", "ps fluid")
    t = t.replace("afs", "active front steering")
    t = t.replace("sbw", "steer by wire")
    t = t.replace("eps", "electric power steering")
    t = t.replace("4ws", "four wheel steering")
    t = t.replace("ps", "power steering")
    t = t.replace("hydraulic ps", "hydraulic power steering")
    t = t.replace("hydraulic psf", "hydraulic power steering fluid")
    t = t.replace("hydraulic pump", "hydraulic power steering pump")
    t = t.replace("rack pinion", "rack and pinion")
    t = t.replace("steering col", "steering column")
    t = t.replace("steering shaft", "steering column")
    t = t.replace("steering gear", "steering gear")
    t = t.replace("toe tire", "toe angle tire")
    t = t.replace("scrub radius", "scrub radius")
    t = t.replace("kingpin inclination", "kingpin inclination")
    t = re.sub(r"\s+", " ", t)
    t = t.strip()
    return SEMANTIC_MAP.get(t, t)

def get_related_terms(term: str) -> list:
    normalized = normalize_term(term)
    related = []
    for k, v in SEMANTIC_MAP.items():
        if v == normalized and k != term:
            related.append(k)
    return related

def get_all_mappings() -> dict:
    return dict(SEMANTIC_MAP)