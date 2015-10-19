class DatatypeUtils:
    @staticmethod
    def isString(string):
        return isinstance(string, basestring)
    
    @staticmethod
    def isBooleanString(string):
        if (not DatatypeUtils.isString(string)):
            raise ValueError("Argument is no a String!")
        return (string.lower() in ['true', 'false'])
    
    @staticmethod
    def isIntegerString(string):
        try:
            int(string)
            return True
        except:
            return False
    
    @staticmethod
    def isFloatString(string):
        try:
            float(string)
            return True
        except:
            return False
    
    @staticmethod
    def stringToBoolean(string):
        if (not DatatypeUtils.isBooleanString(string)):
            raise ValueError("'" + string + "' is no a Boolean!")
        return (string.lower() in ['true'])
    
    @staticmethod
    def stringToInteger(string):
        if (not DatatypeUtils.isIntegerString(string)):
            raise ValueError("'" + string + "' is no a Integer!")
        return int(string)
    
    @staticmethod
    def stringToFloat(string):
        if (not DatatypeUtils.isFloatString(string)):
            raise ValueError("'" + string + "' is no a Float!")
        return float(string)
