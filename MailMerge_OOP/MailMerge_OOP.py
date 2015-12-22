import os
import sys
import time

class Address(object):
    """
    This class holds all the fields for a generic addrees and allows them to be
    formatted into a string suitable for addressing in postal mail.  The street
    number/name, city, state (2-Letter code), and zipCode(5 digits) are all
    required fields.  The optional number field can be omitted.  If present,
    the format function will require a string argument used to describe the
    number field (e.g. "Suite" or "Apt #", etc.).

    Address(string, string, string, string [, string]) --> Address object 
     storing those fields.
    """
    def __init__(self, street, city, state, zipCode, number=''):
        """
        Creates an object to hold the fields of a generic address.

          street:  street number and name in one string
          city:    city name in a string
          state:   two-letter code for state
          zipCode: 5-digit zip code in a string
          number [optional]: additional sub-address used after street address 
           in a string
        """
        
        assert zipCode.isdigit() and len(zipCode) == 5, 'invalid zip code'
        assert state.isalpha() and len(state) == 2, 'invalid state code'

        
        self.street = street
        self.number = number
        self.city = city
        self.state = state
        self.zipCode = zipCode

    def format(self, indent = 0, numberDesc = ''):
        """
        Returns a two-line string with the address fields put together in the
        usual manner.  NumberDesc provides a string used to describe the number
        field of the address (e.g. 'Suite', 'Apt', etc.).  It is ignored if the
        number field is empty.  If not provided and number field is not empty, 
        a default '#' character will be used.

        a.format(int=0, string='') --> string
        """
        number = '' if not self.number else (', #' + self.number if numberDesc
         is '' else ', ' + numberDesc + ' ' + self.number)
        start = ' ' * indent
        return(start + self.street + number + '\n' + start + self.city + ', ' +
         self.state.upper() + '  ' + self.zipCode)

    def __str__(self):
        """
        Function to provide compatibility with built-in Python stringification.
        """
        return self.format()

    def __repr__(self):
        return ('Address('+ self.street +  self.city + self.state + 
         self.zipCode + self.number + ')' )


class Customer(object):
    """
    This class stores the name and address of a customer, though with no
    disctintion on the type of customer, business or individual.  

    Customer(dict) --> Customer object with values from fields as attributes.
    """
    def __init__(self, fields):
        """
        Takes a dictionary of fields of data and stores them in this object.
        Fields are:
            name:    string, name of the customer
            street:  string, street number and name in one string
            city:    string, city name in a string
            state:   string, two-letter code for state
            zipCode: string, 5-digit zip code in a string
            number [optional]: string, additional sub-address used after street 
             address in a string
        All fields except number are required.
        """
        self.name = ''
        self.addr = ''
        self.indent = 0
        self.numberDesc = ''
        self.setFromFields(fields)
           
    def __str__(self):
        return self.name + '\n' + str(self.addr)

    def setFromFields(self, fields):
        """ 
        Uses (key, value) pairs in fields to set this object's attributes,
        specifically name and addr.  addr is created as an Address object.

        c.setFromFields(dict) --> None
        """
        
        if fields.get('name', '') == '':
            assert False, 'Name field missing or empty'
        else:
            self.name = fields['name']
        addrData = (fields.get('street', ''), 
         fields.get('city', ''),
         fields.get('state', ''), 
         fields.get('zip', ''), 
         fields.get('number', '') )
        
        if '' in addrData[:4]:
            assert False, 'Address data missing or empty'
        else:
            self.addr = Address(*addrData)

    def mergeToFile(self, fname, text):
        """
        Replaces <name> and <addr> tags in text with this customer's data
        and writes the result to file named fname.  text should be a list of
        lines to merge with.  Returns the number of field substitutions made.

        c.mergeToFile(string, list(string)) --> int (and creates a file).
        """
        outfile = open(fname, 'w')
        substitutions = 0
        for line in text:
            if line != self._getValueForLine(line):
                outfile.write(self._getValueForLine(line))
                substitutions += 1
            else:
                outfile.write(line)
        outfile.close()
        return substitutions

    def _getValueForLine(self, _line):
        """
        Examines the line for tags which should be replaced.  Returns the
        value that should replace the tag in the output for this customer.

        c._getValueForLine(string) --> string
        """
        if _line.strip().lower() == '<name>':
            subst = self.name + '\n'
        elif _line.strip().lower() == '<addr>':
            subst = str(self.addr.format(self.indent, self.numberDesc)) + '\n'
        elif _line.strip().lower() == '<greeting>':
            subst = '' + '\n'
        elif _line.strip().lower() == '<recruit>':
            subst = '' + '\n'
        else:
            return _line
        return subst
        
class BusCustomer(Customer):
    def __init__(self, fields):
        self.contact = ''
        self.contactTitle = ''
        self.greeting = ''
        super().__init__(fields)
        self.numberDesc = 'Suite'
               
    def setFromFields(self, fields):
        """ 
        Uses (key, value) pairs in fields to set this object's attributes,
        specifically name and addr.  addr is created as an Address object.

        c.setFromFields(dict) --> None
        """
        super().setFromFields(fields)
        if fields.get('contact', '') == '':
            self.contact = ''
        else:
            self.contact = fields['contact']
        if fields.get('contact_title', '') == '':
            self.contactTitle = ''
        else:
            self.contactTitle = fields['contact_title']
        if fields.get('greeting', '') == '':
            self.greeting = ''
        else:
            self.greeting = fields['greeting']
        
    def _getValueForLine(self, line):
        """
        Examines the line for tags which should be replaced.  Returns the
        value that should replace the tag in the output for this customer.

        bc._getValueForLine(string) --> string
        """
        if line.strip().lower() == '<name>':
            if self.contact == '' and self.contactTitle == '':
                line = self.name + '\n'
            elif self.contactTitle == '':
                line = self.contact + '\n'
            else:
                line = self.contact + ', ' + self.contactTitle + '\n'
        elif line.strip().lower() == '<addr>':
            line = super()._getValueForLine(line)
        elif line.strip().lower() == '<greeting>':
            line = self.greeting + '\n'
        else:
            line = super()._getValueForLine(line)
        return line
        
class PersonCustomer(Customer):
    
    def __init__(self, fields):
        self.recruit = 'If you enjoyed working together as much as we did, please feel free to submit your resume and join our team!'
        self.greeting = ''
        super().__init__(fields)
        self.numberDesc = 'Apt.'
                
    def setFromFields(self, fields):
        """ 
        Uses (key, value) pairs in fields to set this object's attributes,
        specifically name and addr.  addr is created as an Address object.

        c.setFromFields(dict) --> None
        """
        super().setFromFields(fields)
        if fields.get('greeting', '') == '':
            assert False, 'Greeting field missing or empty'
        else:
            self.greeting = fields['greeting']
           
    def _getValueForLine(self, line):
        """
        Examines the line for tags which should be replaced.  Returns the
        value that should replace the tag in the output for this customer.

        pc._getValueForLine(string) --> string
        """
        if line.strip().lower() == '<name>':
            line = super()._getValueForLine(line)
        elif line.strip().lower() == '<addr>':
            line = super()._getValueForLine(line)
        elif line.strip().lower() == '<greeting>':
            line = self.greeting + '\n'
        elif line.strip().lower() == '<recruit>':
            line = self.recruit + '\n\n'
        else:
            line = super()._getValueForLine(line)
        return line

class CustomerDB(object):
    """
    This class encapsulates the reading in (and writing out?) of customer 
    database files.

    CustomerDB(fileName) --> CustomerDB object with a list of Customer objects
    """
    def __init__(self, dbFName):
        """
        dbFName should be a file as expected by readCustomers() .
        """
        self.customers = []
        self._readCustomers(dbFName)

    def _makeCustomer(self, fields):
        if 'type' in fields:
            if fields.get('type', 'no type') == 'business':
                busCust = BusCustomer(fields)
                return busCust
            elif fields.get('type', 'no type') == 'person':
                perCust = PersonCustomer(fields)
                return perCust
            else:
                print("Wrong customer type!")
        else:
            cust = Customer(fields)
            return cust
                
    def _readCustomers(self, dbFName):
        """
        dbFName should be a text file with comment lines starting with '#',
        blank lines are ignored, and customer data in 'key = value' lines in
        between [customer] headings to separate the data:
            # This comment is ignored.
            [customer]
            name = Fred Brooks
            street = 124 Mythical St.
            city = Man Month
            state = NY
            zip = 99576
        """
        assert os.path.exists(dbFName), "can't find " + dbFName
        dbf = open(dbFName, 'r')
        fields = {}
        for line in dbf:
            line = line.strip()
            if line == '' or line[0] == '#':
                continue
            elif line == '[customer]':
                if len(fields) > 0:
                    self.customers.append(self._makeCustomer(fields))
                fields.clear()
            else:
                key, value = line.split('=', 1)
                fields[key.strip().lower()] = value.strip()
        if len(fields) > 0:
            self.customers.append(self._makeCustomer(fields))
            fields.clear()
        dbf.close()

    def merge(self, mergeFile):
        """
        Creates a merged file for each known Customer object using the
        mergeFile contents as a template.  Substitutes customer data for 
        fields.  Output file name is called <customer name>--<mergeFile>.
        """
        mfile = open(mergeFile, 'r')
        text = mfile.readlines()
        mfile.close()
        outName = '--' + mergeFile
        for c in self.customers:
            print('merging', c.name)
            c.mergeToFile(c.name + outName, text)

def main(args):
    """
    Checks command line arguments then creates a customer list from the data
    file and then merges the merge file for each customer.
    """
    if len(args) < 3:
        print('usage: ', args[0], '<cust file>', '<merge file>')
        exit(-1)

    if not os.path.exists(args[1]):
        print("Can't find customer file")
        exit(-1)

    if not os.path.exists(args[2]):
        print("Can't find merge file")
        exit(-1)

    custDb = CustomerDB(args[1])
    custDb.merge(args[2])
    
if __name__ == '__main__':
    main(sys.argv)
    
