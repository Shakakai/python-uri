# http://www.apps.ietf.org/rfc/rfc2396.html

import re


class Uri(object):
    
    def __init__(self, source):
        self.authority = ""
        self.path = ""
        self.query = ""
        self.fragment = ""
        self._parse(source)
    
    def _parse(self, source):
        '''
            Parses a URI string into the following parts:
            - scheme
            - authority
            - query
            - fragment
            
            Syntax taken from http://www.apps.ietf.org/rfc/rfc2396.html
        '''
        # find the first ":" to process the scheme
        pos = source.find(":")
        self.scheme = source[0:pos]
        pos += 1
        
        # is there an authority?
        if source[pos:pos+2] == "//":
            pos += 2
            authority_delimiter = re.search("[/?#]", source[pos:])
            if authority_delimiter:
                self.authority = source[pos:pos+authority_delimiter.start(0)]
                pos += len(self.authority)
            else:
                self.authority = source[pos:]
                return # we're done
        
        if len(source[pos:]) == 0:
            return
        
        # do we have a query or fragment?
        path_delimiter = re.search("[?#]", source[pos:])
        if path_delimiter:
            self.path = source[pos:pos+path_delimiter.start(0)]
            pos += path_delimiter.start(0)
            if path_delimiter.group(0) == "#":
                self.fragment = source[pos:]
                return
            else:
                query_delimiter = re.search("#", source[pos:])
                if query_delimiter:
                    self.query = source[pos+1:pos+query_delimiter.start(0)]
                    pos += query_delimiter.start(0)
                    self.fragment = source[pos+1:]
                else:
                    self.query = source[pos+1:]
                    return
        else:
            self.path = source[pos:]
        
    
    def __str__(self):
        result = "%s:" % self.scheme
        if self.authority and len(self.authority) > 0:
            result = "%s//%s" % (result, self.authority)
        result = "%s%s" % (result, self.path)
        if self.query and len(self.query) > 0:
            result = "%s?%s" % (result, self.query)
        if self.fragment and len(self.fragment):
            result = "%s#%s" % (result, self.fragment)
        return result
    

class Url(object):
    
    def __init__(self, source):
        self._uri = Uri(source)
        self._port = None
        self._hostname = ""
        self._parse()
    
    def _parse(self):
        '''
        The primary difference between a URI and URL is the hostname property.
        Everything else is just tweaks to the property names.
        '''
        authority = self._uri.authority
        if len(authority) > 0:
            delimiter = authority.find(":")
            if delimiter > -1:
                self._hostname = authority[0:delimiter]
                self._port = int(authority[delimiter+1:])
            else:
                self._hostname = authority
        
    def _generate_authority(self):
        auth = self._hostname
        if self._port:
            auth = ":" + str(self._port)
        self._uri.authority = auth
    
    def set_hostname(self, value):
        self._hostname = value
        self._generate_authority()
    
    def get_hostname(self):
        return self._hostname
    
    hostname = property(get_hostname, set_hostname)
    
    def set_port(self, value):
        self._port = value
        self._generate_authority()
    
    def get_port(self):
        return self._port
    
    port = property(get_port, set_port)
    
    def get_protocol(self):
        return self._uri.scheme
    
    def set_protocol(self, value):
        self._uri.scheme = value
    
    protocol = property(get_protocol, set_protocol)
    
    def get_hash(self):
        return self._uri.fragment
    
    def set_hash(self, value):
        self._uri.fragment = value
    
    hash = property(get_hash, set_hash)
    
    def get_query(self):
        return self._uri.query
    
    def set_query(self, value):
        self._uri.query = value
    
    query = property(get_query, set_query)
    
    def __str__(self):
        return str(self._uri)
    
    def get_query_parameters(self):
        # shortcut missing or empty
        query = self.query
        result = {}
        if not query or len(query) == 0:
            return result
        
        pairs = query.split("&")
        for pair in query.split("&"):
            items = pair.split("=")
            if len(items) == 2:
                result[items[0]] = items[1]
        return result




