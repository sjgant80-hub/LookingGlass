# Konomi Standard - Base UDTs

## LAYER 1: Primitives

Identifier: UUID, PATH, TAG, URN
Timestamp: ISO8601, EPOCH_MS, OPC_FILETIME
Quality: GOOD(192), BAD(0), UNCERTAIN(64)
Value: {v, q:Quality, t:Timestamp, unit}
Range: {lo, hi, lo_inc, hi_inc, unit}
Quantity: {value, unit, uncertainty}
Duration: {value, unit:ms|s|min|hr|day}
Status: {code, name, desc, severity}

## Usage
All standards share these base types.
Layer 2+ standards reference Layer 1 UDTs.
Crosswalks map between standards.
Agents: parse, expand, validate, crosswalk.
