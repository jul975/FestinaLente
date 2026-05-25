"""
Dynamic Energy Budget (DEB) package for FestinaLente.

deb/
├── functions.py
│   ├── mobilization_flux(...)
│   ├── somatic_maintenance_due(...)
│   ├── maturity_maintenance_due(...)
│   └── growth_from_surplus(...)
│
├── rules.py
│   ├── MaintenanceRule
│   ├── DEBMaintenanceRule
│   ├── MovementRule
│   └── BrockwayBoyneMovementRule
│
├── state.py
│   └── SheepAgentState
│
├── agent.py
│   └── SheepAgent
│
└── ledger.py
    └── AgentDayLedger

"""