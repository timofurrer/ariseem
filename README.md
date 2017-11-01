# arise 'em

`ariseem` is a minimalistic service exposing a REST API to boot machines using wake-on-lan.

It's pure Python and does not require any system dependencies.

```
pip3 install ariseem
```

## Configuration

`ariseem` is configured via YAML file:

```
machines:
    - myserver: AA:BB:CC:DD:EE:FF
    - mypc: AA:BB:CC:FF:EE:DD

groups:
    - vpn:
        - myserver
        - mypc
```

`ariseem` can only *wol* machines configured in the `machines` section.
In addition groups of machines can be specified in the `groups` section.

## Usage

```
GET /api/machines
POST /api/machines/myserver

GET /api/groups
POST /api/groups/vpn
```
