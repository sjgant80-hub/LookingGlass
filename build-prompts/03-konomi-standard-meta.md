# Konomi Standard - Meta Layer

## LAYER 0: META-STANDARD
STD = {id, scope, udt, hierarchy, states,
       entities, relations, rules, crosswalk}

UDT = {name, base, fields, methods, constraints}
LEVEL = {id, name, scope, timescale, systems,
         data_down, data_up}
STATE_MACHINE = {name, states, initial, transitions}
ENTITY = {name, udt, parent, children, tags}
RELATION = {type, from, to, cardinality}
RULE = {id, condition, action, severity}
CROSSWALK = {from_std, from_entity, to_std,
             to_entity, mapping, transform}

## Goal
Self-describing structure. Each layer uses
Layer 0 schema. Max info, min tokens.
