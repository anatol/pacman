self.description = 'download a remote package with -U'

addr = self.add_simple_http_server({ '/foo.pkg': 'foo', '/foo.pkg.sig': 'foo.sig' })

self.args = '-Uw http://%s/foo.pkg' % (addr)

self.addrule('PACMAN_RETCODE=0')
self.addrule('CACHE_FCONTENTS=foo.pkg|foo')
self.addrule('CACHE_FCONTENTS=foo.pkg.sig|foo.sig')
