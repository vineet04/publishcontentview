# publishcontentview
* Pythong script to publish and promote red hat satellite content view and environment.
* Use config file to store secrets and import config module.
* Usage: $ python publishcv.py
* Improvements:
config file encrypted and information is not available in plain text format.
scripts now invoke module used to encrypt the config file. Decrypt while it runs and encrypts it again once finished using it.
