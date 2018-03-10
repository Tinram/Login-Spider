
# Login Spider

#### Spider website pages protected by a login.


## Purpose

Log-in to a website to access the area of a registered user, then spider the page links and process the page content.


## Requirements

+ Python 2.6+
+ pycurl


## Background

Having to use Windows on-site, Python dependencies were somewhat restricted to build a spider (`pip` would only install some, *Beautiful Soup* was not one of them).


## Usage

Configure the website access details in the *CONFIG* section of *login_spider.py*.

(Viewing the website login form's HTML source will be needed to configure the *FORM_POST* string, as each site will use something different.)

Execute:

        python login_spider.py


## Speed

Dependent on CPU and OS, approximately 35 seconds to process a 200 page website with a localhost connection (zero network overhead).


## Credits

jfs and philshem for threading pools in Python.


## License

Login Spider is released under the [GPL v.3](https://www.gnu.org/licenses/gpl-3.0.html).
