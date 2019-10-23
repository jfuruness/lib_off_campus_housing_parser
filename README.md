# lib\_off\_campus\_housing\_parser
This package contains the functionality to record all uconn off campus housing info into an excel spreadsheet, sorted and in order by your preferences. It is optimized to consider the total cost of the apartment. This includes electricity, water, internet, heat, drive time, walk time, parking passes, laundromatt, gas cost, etc. It then opens all options filtered and sorted to be removed manually, and stores what is left into an excel file

* [lib\_off\_campus\_housing\_parser](#lib\_off\_campus\_housing\_parser)
* [Description](#package-description)
* [Usage](#usage)
* [Possible Future Improvements](#possible-future-improvements)
* [Installation](#installation)
* [Testing](#testing)
* [Development/Contributing](#developmentcontributing)
* [History](#history)
* [Credits](#credits)
* [Licence](#licence)
* [Todo and Possible Future Improvements](#todopossible-future-improvements)
* [FAQ](#faq)
## Package Description
* [lib\_off\_campus\_housing\_parser](#lib\_off\_campus\_housing\_parser)

It is optimized to consider the total cost of the apartment. This includes electricity, water, internet, heat, drive time, walk time, parking passes, laundromatt, gas cost, etc. It then opens all options filtered and sorted to be removed manually, and stores what is left into an excel file. This is done through a series of steps.

1. A Selenium Web Browser instance is created
2. You are logged into the uconn off campus housing website (Note: you can be a guest and still use this with a temporary login)
3. The parser iterates over all pages with listings to get all the links for each specific listing
4. All listings are loaded to get the specific listing html
5. All listing information is parsed from the html that relates to the cost
6. All listings are filtered by drive time and pets. They are also sorted in order of least total cost first
7. All listings are opened in the browser in sorted order. The user then goes through and manually closes the ones they are not interested in.
8. Once the user is finished, they hit enter on the terminal. After this, all listing information is saved into an excel file.

Happy apartment hunting!

### Usage
* [lib\_off\_campus\_housing\_parser](#lib\_off\_campus\_housing\_parser)

#### In a Script
NOTE: This script requires a few things.
1. You need a google api key to use google_maps to calculate drive times. Google how to get one of these and enable it for google_maps
2. You need to store your api key in environment variable google_api_key
3. You need to store your password for your netid in environment variable netid_password
4. If you have trouble with the above steps please contact me at jfuruness@gmail.com


Initializing the Off_Campus_Housing_Parser class:


| Parameter    | Default                             | Description                                                                                                       |
|--------------|-------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| executable_path         | ```'/home/anon/Downloads/chromedriver'``` | location of chromedriver |

To init in a script with arguments:
```python
from lib_off_campus_housing_parser import Off_Campus_Housing_Parser
Off_Campus_Housing_Parser(executable_path='/your/chromedriver/executable/path')
```

To run housing parser in a script:


| Parameter    | Default                             | Description                                                                                                       |
|--------------|-------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| drive_time_max         | 20 | max minutes willing to drive to UConn bookstore |
| max_rent         | 1500 | max dollars willing to spend on up front apartment cost |
| netid         | ```"jmf14015"``` | netid for login |
| pets         | ```False``` | If True then gets rid of all listings that do not allow pets|
| test         | ```False``` | If True then gets rid of all listings after the first page for a faster test |
|  excel_path | ```"/tmp/off_campus.xlsx"``` | path to the excel file |

To run with default arguments:
```python
from lib_off_campus_housing_parser import Off_Campus_Housing_Parser
parser = Off_Campus_Housing_Parser(executable_path='/your/chromedriver/executable/path')
parser.parse_houses()
```

To run with custom max drive time (20 min) and rent (2000 dollars):
```python
from lib_off_campus_housing_parser import Off_Campus_Housing_Parser
parser = Off_Campus_Housing_Parser(executable_path='/your/chromedriver/executable/path')
parser.parse_houses(drive_time_max=20, max_rent=2000)
```

To run with custom netid:
```python
from lib_off_campus_housing_parser import Off_Campus_Housing_Parser
parser = Off_Campus_Housing_Parser(executable_path='/your/chromedriver/executable/path')
parser.parse_houses(netid="abc12345")
```

To get only listings with pets:
```python
from lib_off_campus_housing_parser import Off_Campus_Housing_Parser
parser = Off_Campus_Housing_Parser(executable_path='/your/chromedriver/executable/path')
parser.parse_houses(pets=True)
```

To run with a different excel file path:
```python
from lib_off_campus_housing_parser import Off_Campus_Housing_Parser
parser = Off_Campus_Housing_Parser(executable_path='/your/chromedriver/executable/path')
parser.parse_houses(excel_path="/tmp/custom.xlsx")
```

You can create this and call functions to have better filtering mechanisms, I just assume that this is the base case that people will want to use. If you are having trouble writing an extension, please email me at jfuruness@gmail.com

#### From the Command Line

run in a terminal: ```off_campus_housing```

This will start the application with default arguments.

### Installation
* [lib\_off\_campus\_housing\_parser](#lib\_off\_campus\_housing\_parser)

First install the chrome driver (google this)

Then install the package with:
```pip3 install lib_off_campus_housing_parser --upgrade --force```

To install from source and develop:
```
git clone https://github.com/jfuruness/lib_off_campus_housing_parser.git
cd lib_off_campus_housing_parser
pip3 install wheel --upgrade
pip3 install -r requirements.txt --upgrade
python3 setup.py sdist bdist_wheel
python3 setup.py develop
```

### System Requirements
* [lib\_off\_campus\_housing\_parser](#lib\_off\_campus\_housing\_parser)

I don't think you need anything special on your system to run this program. Needs to have linux to get environment variables, idc so they are not in windows.

## Testing
* [lib\_off\_campus\_housing\_parser](#lib\_off\_campus\_housing\_parser)

Run tests on install by doing:
```pip3 install lib_off_campus_housing_parser --force --install-option test```
This will install the package, force the command line arguments to be installed, and run the tests
NOTE: You might need sudo to install command line arguments when doing this

You can test the package if in development by moving/cd into the directory where setup.py is located and running:
```python3 setup.py test```

To test a specific submodule, cd into that submodule and run:
```pytest```

Note: I currently have not written any tests, since I have tried the program and checked it's output by hand so I know that it works. I know that this is not sufficient, but no one is going to use this thing but me so whatevs.


## Development/Contributing
* [lib\_off\_campus\_housing\_parser](#lib\_off\_campus\_housing\_parser)

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request
6. Email me at jfuruness@gmail.com because I do not check those messages often

## History
   * [lib\_youtube\_cd\_burner](#lib\_youtube\_cd\_burner)
   * 0.1.0 - Initial commit

## Credits
* [lib\_off\_campus\_housing\_parser](#lib\_off\_campus\_housing\_parser)

There where various sites I visited to learn about the total cost of things around UConn, unfortunately I did not record them as I did them because I didn't plan on making a public package.

This would of course this would not have been possible without google_maps and selenium, two very useful packages.

## License
* [lib\_off\_campus\_housing\_parser](#lib\_off\_campus\_housing\_parser)

BSD License

## TODO/Possible Future Improvements
* [lib\_off\_campus\_housing\_parser](#lib\_off\_campus\_housing\_parser)

        * Should have departure time for driving not be the current time, and instead be 7:30AM during Monday, which is when it would be the worst
        * Should not have bare except, should have specific errors
        * Parallelize drive time calculations? I thought I ended up not doing this because google's api blocked me but I'm not sure, I should have written it down

## FAQ
* [lib\_off\_campus\_housing\_parser](#lib\_off\_campus\_housing\_parser)

Q: Why isn't selenium working?
A: Did you download the chrome driver? Did you set the executable path correctly? Google how to do this, since it changes as time goes on. Email jfuruness@gmail.com if you still have questions.

Q: It is endlessly scrolling
A: Your internet must be very slow. The pages load with javascript calls, so the script waits before it continues. It normally waits for a couple of seconds and then continues, but if it loads extremely slowly sometimes it tries to continue too soon and loops. You are going to have to change the sleep parameters in the code to run this.
