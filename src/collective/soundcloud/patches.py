# -*- coding: utf-8 -*-
import requests
import six
import soundcloud


try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


def make_request_patch_201(method, url, params):
    """Make an HTTP request, formatting params as required."""
    # patch accoding to
    # https://github.com/soundcloud/soundcloud-python/issues/68
    empty = []

    # TODO
    # del params[key]
    # without list
    for key, value in six.iteritems(params):
        if value is None:
            empty.append(key)
    for key in empty:
        del params[key]

    # allow caller to disable automatic following of redirects
    allow_redirects = params.get('allow_redirects', True)

    kwargs = {
        'allow_redirects': allow_redirects,
        'headers': {
            'User-Agent': soundcloud.USER_AGENT
        }
    }
    # options, not params
    if 'verify_ssl' in params:
        if params['verify_ssl'] is False:
            kwargs['verify'] = params['verify_ssl']
        del params['verify_ssl']
    if 'proxies' in params:
        kwargs['proxies'] = params['proxies']
        del params['proxies']
    if 'allow_redirects' in params:
        del params['allow_redirects']

    params = soundcloud.hashconversions.to_params(params)
    files = soundcloud.request.namespaced_query_string(
        soundcloud.request.extract_files_from_dict(params)
    )
    data = soundcloud.request.namespaced_query_string(
        soundcloud.request.remove_files_from_dict(params)
    )

    request_func = getattr(requests, method, None)
    if request_func is None:
        raise TypeError('Unknown method: %s' % (method,))

    if method == 'get':
        kwargs['headers']['Accept'] = 'application/json'
        qs = urlencode(data)
        if '?' in url:
            url_qs = '%s&%s' % (url, qs)
        else:
            url_qs = '%s?%s' % (url, qs)
        result = request_func(url_qs, **kwargs)
    else:
        kwargs['data'] = data
        if files:
            kwargs['files'] = files
        result = request_func(url, **kwargs)

    # BEFORE PATCH
    # if redirects are disabled, don't raise for 301 / 302
    # if result.status_code in (301, 302):
    #     if allow_redirects:
    #         result.raise_for_status()
    # else:
    #     result.raise_for_status()
    # return result

    # AFTER PATCH
    # if redirects are disabled, don't raise for 301 / 302
    if result.status_code in (301, 302):
        if allow_redirects:
            result.raise_for_status()
    elif result.status_code in (401, ):
        if result.headers['Status'] == "201 Created":
            result = requests.get(
                "{}?oauth_token={}".format(
                    result.headers['Location'],
                    data['oauth_token']
                )
            )
    else:
        result.raise_for_status()
    return result

# PATCH
soundcloud.request.make_request = make_request_patch_201
