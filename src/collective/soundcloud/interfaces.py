from zope.interface import Interface

class IOAuth2AuthenticationSettings(Interface):
    
    def getClientId(self):
        """fetch client id"""

    def setClientId(self, value):
        """store client id"""
        
    def getClientSecret(self):
        """fetch client secret"""
        
    def setClientSecret(self, value):
        """store client secret"""
        
class IOAuth2TokenHandler(Interface):
    
    def getToken(self):
        """fetch token from storage"""
        
    def setToken(self, value):
        """store secret token"""