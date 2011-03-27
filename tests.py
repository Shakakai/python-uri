import unittest
from uri import Uri, Url


class UriTests(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def testHttpUri(self):
        http_url = "http://www.google.com/mail?locale=en_US#tab1"
        uri = Uri(http_url)
        self.assertEqual("http", uri.scheme)
        self.assertEqual("www.google.com", uri.authority)
        self.assertEqual("/mail", uri.path)
        self.assertEqual("locale=en_US", uri.query)
        self.assertEqual("tab1", uri.fragment)
    
    def testImaginaryUri(self):
        fake_uri = "urn:example:animal:ferret:nose"
        uri = Uri(fake_uri)
        self.assertEqual("urn", uri.scheme)
        self.assertEqual("example:animal:ferret:nose", uri.path)
    
    def testQuoraUri(self):
        q_uri = "http://www.quora.com/Is-there-a-polite-way-to-interrupt-or-stop-a-Death-by-Powerpoint-presentation"
        uri = Uri(q_uri)
        self.assertEqual("http", uri.scheme)
        self.assertEqual("www.quora.com", uri.authority)
        self.assertEqual("/Is-there-a-polite-way-to-interrupt-or-stop-a-Death-by-Powerpoint-presentation", uri.path)
        self.assertEqual("", uri.query)
        self.assertEqual("", uri.fragment)
    
    def testBitlyUri(self):
        bitly_url = "http://bit.ly/f3fvFA"
        uri = Uri(bitly_url)
        self.assertEqual("http", uri.scheme)
        self.assertEqual("bit.ly", uri.authority)
        self.assertEqual("/f3fvFA", uri.path)
        self.assertEqual("", uri.query)
        self.assertEqual("", uri.fragment)
    
    def testInputOutput(self):
        fake_uri = "urn:example:animal:ferret:nose"
        uri = Uri(fake_uri)
        self.assertEqual(fake_uri, str(uri))

class UrlTests(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def testUrl(self):
        http_url = "http://www.google.com:80/mail?locale=en_US#tab1"
        url = Url(http_url)
        self.assertEqual("http", url.protocol)
        self.assertEqual("www.google.com", url.hostname)
        self.assertEqual(80, url.port)
        self.assertEqual("tab1", url.hash)
        self.assertEqual("locale=en_US", url.query)
    
    def testInputOutput(self):
        http_url = "http://www.google.com:80/mail?locale=en_US#tab1"
        url = Url(http_url)
        self.assertEqual(http_url, str(url))
    
    def testSingleQueryParameter(self):
        http_url = "http://www.google.com:80/mail?locale=en_US#tab1"
        url = Url(http_url)
        parameters = url.get_query_parameters()
        self.assertTrue("locale" in parameters)
        self.assertEqual("en_US", parameters["locale"])
    
    def testMultiQueryParameters(self):
        http_url = "http://www.google.com:80/mail?locale=en_US&support=true#tab1"
        url = Url(http_url)
        parameters = url.get_query_parameters()
        self.assertTrue("locale" in parameters)
        self.assertEqual("en_US", parameters["locale"])
        self.assertTrue("support" in parameters)
        self.assertEqual("true", parameters["support"])
    
    def testNoQueryParameters(self):
        http_url = "http://www.google.com:80/mail?missingValue#tab1"
        url = Url(http_url)
        parameters = url.get_query_parameters()
        self.assertTrue(len(parameters) == 0, parameters)

if __name__ == '__main__':
    unittest.main()

        