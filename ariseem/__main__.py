"""
    ariseem
    ~~~~~~~

    Minimalistic REST API for wake-on-lan

    :copyright: (c) 2017 by Timo Furrer <tuxtimo@gmail.com>
    :license: MIT, see LICENSE for more details.
"""

import os
import logging

from flask import Flask, jsonify
import yaml

from .wol import wake_on_lan

#: Holds the Flask app instance
app = Flask(__name__)
#: Holds the logger instance
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def read_config(configfile):
    """
    Read the ariseem config from a file

    Use the following format:

        machines:
            myserver: AA:BB:CC:DD:EE:FF
            mypc: AA:BB:CC:FF:EE:DD

        groups:
            vpn:
                - myserver
                - mypc
    """
    with open(configfile, 'r') as conf_file:
        config = yaml.safe_load(conf_file)
    return config


#: Holds the current configuration
config = read_config(os.environ.get('ARISEEM_CONFIG', './config.yml'))


class ApiError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(ApiError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/api/machines', methods=['GET'])
def get_maschines():
    """
    Get all available machines
    """
    return jsonify(config.get('machines', {}))


@app.route('/api/machines/<string:machine_name>', methods=['POST'])
def wol_machine(machine_name):
    """
    WOL an available machine
    """
    if not config.get('machines'):
        raise ApiError('No machines configured', status_code=404)

    machine_mac = config['machines'].get(machine_name)
    if not machine_mac:
        raise ApiError(f'No machine with name {machine_name} found', status_code=404)

    logger.info(f'Resolved {machine_name} to {machine_mac}')

    try:
        wake_on_lan(machine_mac)
    except Exception as exc:
        raise ApiError(f'Unable to wol machine {machine_name}: {exc}')
    else:
        logger.info(f'Sent WOL packet to {machine_name} at {machine_mac}')
        return jsonify({'message': f'WOL packet sent to {machine_name}'})


@app.route('/api/groups', methods=['GET'])
def get_groups():
    """
    Get all available groups
    """
    return jsonify(config.get('groups', {}))


@app.route('/api/groups/<group_name>', methods=['POST'])
def wol_group(group_name):
    """
    WOL an available group
    """
    if not config.get('groups'):
        raise ApiError('No groups configured', status_code=404)

    group = config['groups'].get(group_name)
    if not group:
        raise ApiError(f'No group with name {group_name} found', status_code=404)

    machine_macs = ((name, config['machines'][name]) for name in group)

    for machine_name, machine_mac in machine_macs:
        logger.info(f'Resolved {machine_name} to {machine_mac} from {group_name}')
        try:
            wake_on_lan(machine_mac)
        except Exception as exc:
            raise ApiError(f'Unable to wol machine {machine_name}: {exc}')
        else:
            logger.info(f'Sent WOL packet to {machine_name} at {machine_mac} from {group_name}')

    return jsonify({'message': f'WOL packets sent to group {group_name}'})
