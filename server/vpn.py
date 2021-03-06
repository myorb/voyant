import falcon
import hug

from .providers import PROVIDERS


@hug.post('/')
def create_vpn(key, provider, region='EU1'):
    provider = PROVIDERS.get(provider)
    if not provider:
        raise falcon.HTTPBadRequest('PROVIDER_NOT_FOUND', 'The provider does not exist.')

    provider = provider["class"](key)

    region = provider.regions.get(region)
    if not region:
        raise falcon.HTTPBadRequest('REGION_NOT_FOUND', 'The region does not exist.')

    server = provider.create(region)

    return provider.server_to_json(server)


@hug.get('/')
def list_vpns(key, provider):
    provider = PROVIDERS.get(provider)
    if not provider:
        raise falcon.HTTPBadRequest('PROVIDER_NOT_FOUND', 'The provider does not exist.')

    provider = provider["class"](key)
    return [provider.server_to_json(server) for server in provider.list_servers()]


@hug.delete('/')
def destroy_vpn(key, provider, vpn_id):
    provider = PROVIDERS.get(provider)
    if not provider:
        raise falcon.HTTPBadRequest('PROVIDER_NOT_FOUND', 'The provider does not exist.')

    provider = provider["class"](key)

    try:
        provider.destroy(vpn_id)
    except:
        raise falcon.HTTPBadRequest('VPN_NOT_FOUND', 'The vpn \'{}\' does not exist.'.format(vpn_id))

    return {'success': True}


@hug.get('/config')
def get_config(key, provider, vpn_id):
    provider = PROVIDERS.get(provider)
    if not provider:
        raise falcon.HTTPBadRequest('PROVIDER_NOT_FOUND', 'The provider does not exist.')

    provider = provider["class"](key)
    config = provider.get_config(vpn_id)

    return config


@hug.get('/config/download', output=hug.output_format.text)
def get_file(key, provider, vpn_id):
    return get_config(key, provider, vpn_id).get('config')


@hug.get('/regions')
def get_regions(key, provider):
    provider = PROVIDERS.get(provider)
    if not provider:
        raise falcon.HTTPBadRequest('PROVIDER_NOT_FOUND', 'The provider does not exist.')

    provider = provider["class"](key)
    regions = provider.regions

    return regions.keys()


@hug.get('/providers')
def get_providers():
    return [{'text': val['text'], 'value': val['value']} for key, val in PROVIDERS.items()]
