"""
Description: This script downloads the mass spectrum of a chemical species from
    the NIST Chemistry web book using the CAS Registry Numbers (CAS #). The
    downloaded mass spectrum is saved as a JDX file which can be imported into
    the RGASoft's mass library.
    You can specify multiple CAS # to download the mass spectra at once.
    
Usage:
    - You must have Python 3.x installed on your computer.
    - Copy this script to a location where you have the write permission.
    - Modify the script to provide the CAS # list in the CAS_registry_numbers.
    - Change the out_dir if neccessary. By default, the JDX files are saved to
    the same directory where the script resides.
    - Run:
        python downloadMassSpectraFromNIST.py
"""

from urllib.request import urlopen

url_format="http://webbook.nist.gov/cgi/cbook.cgi?JCAMP=%s&amp;Index=0&amp;Type=Mass"
            
CAS_registry_numbers = [
    "67-66-3",
    "630-08-0",
    "7782-44-7",
]

out_dir = "."

for cas_number in CAS_registry_numbers:
    print(cas_number)
    cas_number = cas_number.replace('-','')  # Remove hypens
    try:
        out_file = open(out_dir + '\\' + cas_number + '-Mass.jdx', "w")
        response = urlopen(url_format%cas_number)
        lines = response.readlines()
        for line in lines:
            out_file.write(line.decode("utf-8"))
        out_file.close()
    except Exception as e:
        print(e)
print("Done")
