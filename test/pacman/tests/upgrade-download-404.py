self.description = 'download a remote package with -U'

addr = self.add_simple_http_server({})

self.args = '-Uw http://%s/foo.pkg' % (addr)

self.addrule('!PACMAN_RETCODE=0')
self.addrule('!CACHE_FEXISTS=foo.pkg')
self.addrule('!CACHE_FEXISTS=foo.pkg.sig')
