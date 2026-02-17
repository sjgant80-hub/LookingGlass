# System APIs

## REST (BlockArray)
POST /template/create → create 1000³ template
POST /instance/create → instantiate array
GET  /value?x,y,z    → get cube value
POST /value           → set cube value
POST /llm/process     → run LLM@coord
POST /llm/interlock   → face ops (1M cubes)

## WebSocket (Cube)
ws://host:6789
- initialize: {template_id}
- process: {vertex, text}
- connect: {source, target}
- status: get all vertex states

## Kontainer
- api: port 3001, 1 CPU, 1Gi
- web: port 3000, 0.5 CPU, 512Mi
- ws:  port 3002, 0.5 CPU, 512Mi
