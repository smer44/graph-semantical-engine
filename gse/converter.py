class IdentityConverter:

    def tostr(self,value):
        return str(value)

    def fromstr(self, value):
        return value


class StrToSimpleValueConverter:

    def __init__(self):
        self.known_fromstr = {"false" : False,
                      "False": False,
                      "true" : True,
                      "True" : True,
                      "None": None,
                      "none": None}

    def tostr(self,value):
        return str(value)

    def fromstr(self, value):
        """
        Converts a string to its primitive value,
        what can be int, float, boolean or None, or string if
        these variants does not match
        :param value:
        :return:
        """
        try:
            return int(value)
        except ValueError:
            pass
        try:
            return float(value)
        except ValueError:
            pass

        return self.known_fromstr.get(value,value)


class StrToCompoundValueConverter(StrToSimpleValueConverter):

    def __init__(self):
        StrToSimpleValueConverter.__init__(self)
        self.brackets_types={"[": ("]", list),
                             "(": (")", tuple),
                             "{": ("}", set),
                             }
        self.update_backwards_brackets()

    def update_backwards_brackets(self):
        self.backwards_brackets = set(t[0] for t in self.brackets_types.values())


    def fromstr(self,value):
        print(f"fromstr : { value=}")
        assert isinstance(value,str)
        value = value.strip()
        first = value[0]
        bracket_clz = self.brackets_types.get(first,None)
        if bracket_clz:
            bracket,clz = bracket_clz
            #assert value[-1] == bracket, f"fromstr : wrong brackets :{value=}"
            ret,pos = self.__str_to_collection__(value,bracket, clz, pos = 1)
            assert pos == len(value) , f"fromstr :wrong  {value=} bracket too early on {pos=} "
            return ret
        if first in self.backwards_brackets:
            raise ValueError(f"fromstr : closing bracket {first} without open bracket on")
        return StrToSimpleValueConverter.fromstr(self,value)


    def __str_to_collection__(self,value,closed_bracket,collection_class,pos ,komma = ","):
        print(f"__str_to_collection__ : { value=}, {pos=}")
        last_pos = pos

        ln = len(value)
        ret = []
        while pos < ln:
            char = value[pos]
            bracket_clz = self.brackets_types.get(char, None)
            if bracket_clz:
                bracket, clz = bracket_clz
                item, pos = self.__str_to_collection__(value,bracket, clz, pos=pos+1)
                ret.append(item)
                last_pos = pos

            elif char == komma:
                if pos > last_pos:
                    sub_value = value[last_pos:pos].strip()
                    if sub_value:
                        ret.append(self.fromstr(sub_value))
                pos += 1
                last_pos = pos
            elif char == closed_bracket:
                if pos > last_pos:
                    ret.append(self.fromstr(value[last_pos:pos]))
                pos+=1
                last_pos = pos
                break
            else:
                pos +=1



        return collection_class(ret), pos
#TODO - with closed bracket


def test():
    text = " [ a,b,5, [6.6, string with space ] ,f]" # wrong behaviour
    #text = " [ 5, [6.6,e ] ,f]" # wrong behaviour

    co =StrToCompoundValueConverter()

    res = co.fromstr(text)
    print(res)




