class DatatypeUtils:
    @staticmethod
    def isString(string):
        return isinstance(string, basestring)
    
    @staticmethod
    def stringToBoolean(string):
        if (not DatatypeUtils.isString(string)):
            raise ValueError('Parameter is not a String!')
            
        if (string.lower() in ("yes", "y", "true", "t", "1")):
            return True;
        if (string.lower() in ("no", "n", "false", "f", "0")):
            return False;
        raise ValueError(string + ' is not a Boolean value!')
        
    @staticmethod
    def stringToFloat(string):
        if (not DatatypeUtils.isString(string)):
            raise ValueError('Parameter is not a String!')
            
        try:
            value = float(string)
            return value
        except:
            raise ValueError(string + ' is not a Float value!')
    
    @staticmethod
    def stringToInteger(string):
        if (not DatatypeUtils.isString(string)):
            raise ValueError('Parameter is not a String!')
            
        try:
            value = int(string)
            return value
        except:
            raise ValueError(string + ' is not a Integer value!')
