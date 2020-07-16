self.description = 'download remote packages with -U without a URL filename'

addr = self.add_simple_http_server({
    # simple
    '/simple.pkg/': 'simple',

    # content-disposition filename
    '/cd.pkg/': {
        'headers': { 'Content-Disposition': 'filename="cd-alt.pkg"' },
        'body': 'cd'
    },
    '/cd.pkg/.sig': {
        'code': 404
    },

    # redirect
    '/redir.pkg/': { 'code': 303, 'headers': { 'Location': '/redir-dest.pkg' } },
    '/redir-dest.pkg': 'redir-dest',
    '/redir-dest.pkg.sig': 'redir-dest.sig',

    # content-disposition and redirect
    '/cd-redir.pkg/': { 'code': 303, 'headers': { 'Location': '/cd-redir-dest.pkg' } },
    '/cd-redir-dest.pkg': {
        'headers': { 'Content-Disposition': 'filename="cd-redir-dest-alt.pkg"' },
        'body': 'cd-redir-dest'
    },
    '/cd-redir-dest.pkg': 'redir-dest',
    '/cd-redir-dest.pkg.sig': 'redir-dest.sig',

    '': 'fallback',
})

url = 'http://{}'.format(addr)
self.args = '-Uw {url}/simple.pkg/ {url}/cd.pkg/ {url}/redir.pkg/ {url}/cd-redir.pkg/'.format(url=url)

self.addrule('PACMAN_RETCODE=0')

# TODO: figure out some way to predict the final file name
#self.addrule('CACHE_FCONTENTS=simple.pkg|simple')
#self.addrule('CACHE_FCONTENTS=simple.pkg.sig|simple.sig')

self.addrule('!CACHE_FEXISTS=cd.pkg')
self.addrule('CACHE_FCONTENTS=cd-alt.pkg|cd')
self.addrule('!CACHE_FEXISTS=cd-alt.pkg.sig|cd.sig')

self.addrule('!CACHE_FEXISTS=redir.pkg')
self.addrule('CACHE_FCONTENTS=redir-dest.pkg|redir-dest')
self.addrule('CACHE_FCONTENTS=redir-dest.pkg.sig|redir-dest.sig')

self.addrule('!CACHE_FEXISTS=cd-redir.pkg')
self.addrule('CACHE_FCONTENTS=cd-redir-dest.pkg|redir-dest')
self.addrule('CACHE_FCONTENTS=cd-redir-dest.pkg.sig|redir-dest.sig')

self.addrule('!CACHE_FEXISTS=.sig')
