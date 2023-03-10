import importlib


mavlink = None

def set_dialect(dialect):
    '''set the MAVLink dialect to work with.
    For example, set_dialect("ardupilotmega")
    '''
    global mavlink
    
    modname = "Reader." + dialect
    mavlink = importlib.import_module(modname)

set_dialect('ardupilotmega')

mode_mapping_apm = {
    0 : 'MANUAL',
    1 : 'CIRCLE',
    2 : 'STABILIZE',
    3 : 'TRAINING',
    4 : 'ACRO',
    5 : 'FBWA',
    6 : 'FBWB',
    7 : 'CRUISE',
    8 : 'AUTOTUNE',
    10 : 'AUTO',
    11 : 'RTL',
    12 : 'LOITER',
    13 : 'TAKEOFF',
    14 : 'AVOID_ADSB',
    15 : 'GUIDED',
    16 : 'INITIALISING',
    17 : 'QSTABILIZE',
    18 : 'QHOVER',
    19 : 'QLOITER',
    20 : 'QLAND',
    21 : 'QRTL',
    22 : 'QAUTOTUNE',
    23 : 'QACRO',
    24 : 'THERMAL',
    25 : 'LOITERALTQLAND',
}

mode_mapping_acm = {
    0 : 'STABILIZE',
    1 : 'ACRO',
    2 : 'ALT_HOLD',
    3 : 'AUTO',
    4 : 'GUIDED',
    5 : 'LOITER',
    6 : 'RTL',
    7 : 'CIRCLE',
    8 : 'POSITION',
    9 : 'LAND',
    10 : 'OF_LOITER',
    11 : 'DRIFT',
    13 : 'SPORT',
    14 : 'FLIP',
    15 : 'AUTOTUNE',
    16 : 'POSHOLD',
    17 : 'BRAKE',
    18 : 'THROW',
    19 : 'AVOID_ADSB',
    20 : 'GUIDED_NOGPS',
    21 : 'SMART_RTL',
    22 : 'FLOWHOLD',
    23 : 'FOLLOW',
    24 : 'ZIGZAG',
    25 : 'SYSTEMID',
    26 : 'AUTOROTATE',
    27 : 'AUTO_RTL',
}

mode_mapping_rover = {
    0 : 'MANUAL',
    1 : 'ACRO',
    2 : 'LEARNING',
    3 : 'STEERING',
    4 : 'HOLD',
    5 : 'LOITER',
    6 : 'FOLLOW',
    7 : 'SIMPLE',
    8 : 'DOCK',
    10 : 'AUTO',
    11 : 'RTL',
    12 : 'SMART_RTL',
    15 : 'GUIDED',
    16 : 'INITIALISING'
}

mode_mapping_tracker = {
    0 : 'MANUAL',
    1 : 'STOP',
    2 : 'SCAN',
    4 : 'GUIDED',
    10 : 'AUTO',
    16 : 'INITIALISING'
}

mode_mapping_sub = {
    0: 'STABILIZE',
    1: 'ACRO',
    2: 'ALT_HOLD',
    3: 'AUTO',
    4: 'GUIDED',
    7: 'CIRCLE',
    9: 'SURFACE',
    16: 'POSHOLD',
    19: 'MANUAL',
}

mode_mapping_blimp = {
    0 : 'LAND',
    1 : 'MANUAL',
    2 : 'VELOCITY',
    3 : 'LOITER',
}

AP_MAV_TYPE_MODE_MAP = {
    # copter
    mavlink.MAV_TYPE_HELICOPTER:  mode_mapping_acm,
    mavlink.MAV_TYPE_TRICOPTER:   mode_mapping_acm,
    mavlink.MAV_TYPE_QUADROTOR:   mode_mapping_acm,
    mavlink.MAV_TYPE_HEXAROTOR:   mode_mapping_acm,
    mavlink.MAV_TYPE_OCTOROTOR:   mode_mapping_acm,
    mavlink.MAV_TYPE_DECAROTOR:   mode_mapping_acm,
    mavlink.MAV_TYPE_DODECAROTOR: mode_mapping_acm,
    mavlink.MAV_TYPE_COAXIAL:     mode_mapping_acm,
    # plane
    mavlink.MAV_TYPE_FIXED_WING: mode_mapping_apm,
    # rover
    mavlink.MAV_TYPE_GROUND_ROVER: mode_mapping_rover,
    # boat
    mavlink.MAV_TYPE_SURFACE_BOAT: mode_mapping_rover, # for the time being
    # tracker
    mavlink.MAV_TYPE_ANTENNA_TRACKER: mode_mapping_tracker,
    # sub
    mavlink.MAV_TYPE_SUBMARINE: mode_mapping_sub,
    # blimp
    mavlink.MAV_TYPE_AIRSHIP: mode_mapping_blimp,
}

mainstate_mapping_px4 = {
    0 : 'MANUAL',
    1 : 'ALTCTL',
    2 : 'POSCTL',
    3 : 'AUTO_MISSION',
    4 : 'AUTO_LOITER',
    5 : 'AUTO_RTL',
    6 : 'ACRO',
    7 : 'OFFBOARD',
    8 : 'STAB',
    9 : 'RATTITUDE',
    10 : 'AUTO_TAKEOFF',
    11 : 'AUTO_LAND',
    12 : 'AUTO_FOLLOW_TARGET',
    13 : 'MAX',
}


def mode_string_px4(MainState):
    return mainstate_mapping_px4.get(MainState, "Unknown")


def mode_string_acm(mode_number):
    '''return mode string for ArduCopter'''
    if mode_number in mode_mapping_acm:
        return mode_mapping_acm[mode_number]
    return "Mode(%u)" % mode_number


def mode_mapping_bynumber(mav_type):
    '''return dictionary mapping mode numbers to name, or None if unknown'''
    return AP_MAV_TYPE_MODE_MAP[mav_type] if mav_type in AP_MAV_TYPE_MODE_MAP else None


def evaluate_expression(expression, vars):
    '''evaluation an expression'''
    return eval(expression, globals(), vars)


def evaluate_condition(condition, vars):
    '''evaluation a conditional (boolean) statement'''
    if condition is None:
        return True
    v = evaluate_expression(condition, vars)
    if v is None:
        return False
    return v