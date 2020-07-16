self.description = 'download remote packages with -U with a URL filename'

addr = self.add_simple_http_server({
    # simple
    '/simple.pkg': 'simple',
    '/simple.pkg.sig': {
        'headers': { 'Content-Disposition': 'filename="simple.sig-alt' },
        'body': 'simple.sig',
    },

    # content-disposition filename
    '/cd.pkg': {
        'headers': { 'Content-Disposition': 'filename="cd-alt.pkg"' },
        'body': 'cd'
    },
    '/cd.pkg.sig': 'cd.sig',
    '/cd-alt.pkg.sig': 'cd-alt.sig',

    # redirect
    '/redir.pkg': { 'code': 303, 'headers': { 'Location': '/redir-dest.pkg' } },
    '/redir-dest.pkg': 'redir-dest',
    '/redir.pkg.sig': 'redir.sig',
    '/redir-dest.pkg.sig': 'redir-dest.sig',

    # content-disposition and redirect
    '/cd-redir.pkg': { 'code': 303, 'headers': { 'Location': '/cd-redir-dest.pkg' } },
    '/cd-redir-dest.pkg': {
        'headers': { 'Content-Disposition': 'filename="cd-redir-dest-alt.pkg"' },
        'body': 'cd-redir-dest'
    },
    '/cd-redir.pkg.sig': 'cd-redir.sig',
    '/cd-redir-dest.pkg.sig': 'cd-redir-dest.sig',
    '/cd-redir-dest-alt.pkg.sig': 'cd-redir-dest-alt.sig',
})

url = 'http://{}'.format(addr)
self.args = '-Uw {url}/simple.pkg {url}/cd.pkg {url}/redir.pkg {url}/cd-redir.pkg'.format(url=url)

self.addrule('PACMAN_RETCODE=0')

self.addrule('CACHE_FCONTENTS=simple.pkg|simple')
self.addrule('CACHE_FCONTENTS=simple.pkg.sig|simple.sig')

self.addrule('!CACHE_FEXISTS=cd.pkg')
self.addrule('!CACHE_FEXISTS=cd.pkg.sig')
self.addrule('CACHE_FCONTENTS=cd-alt.pkg|cd')
self.addrule('CACHE_FCONTENTS=cd-alt.pkg.sig|cd.sig')

self.addrule('!CACHE_FEXISTS=redir.pkg')
self.addrule('CACHE_FCONTENTS=redir-dest.pkg|redir-dest')
self.addrule('CACHE_FCONTENTS=redir-dest.pkg.sig|redir-dest.sig')

self.addrule('!CACHE_FEXISTS=cd-redir.pkg')
self.addrule('!CACHE_FEXISTS=cd-redir-dest.pkg')
self.addrule('CACHE_FEXISTS=cd-redir-dest-alt.pkg')
self.addrule('CACHE_FCONTENTS=cd-redir-dest-alt.pkg|cd-redir-dest')
self.addrule('CACHE_FCONTENTS=cd-redir-dest-alt.pkg.sig|cd-redir-dest.sig')
