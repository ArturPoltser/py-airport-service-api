from airport.enums import CrewPositionEnum


CREW_POSITION_TYPE = (
    (CrewPositionEnum.PILOT.value, "Pilot"),
    (CrewPositionEnum.COPILOT.value, "Co-Pilot"),
    (CrewPositionEnum.FLIGHT_ATTENDANT.value, "Flight Attendant"),
    (CrewPositionEnum.AIR_TRAFFIC_CONTROLLER.value, "Air Traffic Controller"),
    (CrewPositionEnum.GROUND_CREW.value, "Ground Crew"),
    (CrewPositionEnum.SECURITY_OFFICER.value, "Security Officer"),
    (CrewPositionEnum.AIRPORT_STAFF.value, "Airport Staff"),
)
