
# Login Spider

#### Spider pages the other side of a website log-in.


## Purpose

Log-in to a website using *pycurl* to access the pages of a registered user, then harvest the page links and process the pages.


## Usage

Configure the website access details in the *## CONFIG ##* section of *login_spider.py*.

(Viewing the website log-in form's HTML source will be needed to configure *FORM_POST*)

Execute:

        python login_spider.py


## Speed

Dependent on CPU and OS, approximately 35 seconds to process a 200 page website.


## Credits

jfs and philshem for threading pools in Python.


## License

Login Spider is released under the [GPL v.3](https://www.gnu.org/licenses/gpl-3.0.html).
