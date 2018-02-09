
# Login Spider

#### Spider website pages the other side of a log-in.


## Purpose

Log-in to a website with *pycurl*, thereby accessing the pages of a registered user.

Then harvest the page links and process the pages.


## Usage

Configure the website access in the *## CONFIG ##* section of the script.

(Viewing the website log-in form's HTML source will be needed to configure *FORM_POST*)

Execute:

        python login_spider.py


## Credits

jfs and philshem for threading pools in Python.


## License

Login Spider is released under the [GPL v.3](https://www.gnu.org/licenses/gpl-3.0.html).
