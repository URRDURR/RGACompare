# The code excerpt below is a sample to read a RGA data file in Python.
# The sample code is based on a data file that has 2 step scan sequence:
#   Step 1: An Analog or a Histogram scan.
#   Step 2: PvsT scan with various gases.
# The code will extract all data of the Analog/Histogram scan and optionally
# skip over the PvsT scan (change flag SKIP_STEP2_DATA)
#
# For an Analog or a Histogram scan:
#   number_of_data_points = (stop_mass - start_mass) * points_per_amu + 1
#   points_per_amu = 1 for a Histogram scan
#
# For a PvsT scan:
#   number_of_data_points = number_of_gases
#
# With an installed Python 3.6+, run the script as follows:
# python <directory>\dataFileReader.py "<data_directory>\<file_name>.rgadata"

import struct
import json
import numpy as np
from PySide6.QtCore import QObject, Signal

def read_int(fd):
    bytes = fd.read(4)
    value = struct.unpack('i', bytes)[0]
    return value

def read_uint(fd):
    bytes = fd.read(4)
    value = struct.unpack('I', bytes)[0]
    return value

def read_int64(fd):
    bytes = fd.read(8)
    value = struct.unpack('q', bytes)[0]
    return value
    
def read_float(fd):
    bytes = fd.read(4)
    value = struct.unpack('f', bytes)[0]
    return value
    
def read_boolean(fd):
    bytes = fd.read(1)
    value = struct.unpack('?', bytes)[0]
    return value


SKIP_STEP2_DATA = False

class RgaScan():
    """
    Class for handling the RGASoft scan data files
    
    Args:
        filename (string): file location
    """
    def __init__(self, filename):
        self.file_identifier = None
        self.file_version = None
        self.is_single_precision = None

        # Metadata/Settings
        # Note, lots of the Metadata isnt here simply since its superfluous (and there is a lot of it)
        # If needed, go to [website] see how its stored, its in the "Settings JSON" file contained in the scan file
        self.pointsPerAmu = None
        self.scanRate = None
        self.startMass = None
        self.stopMass = None

        # Scan Data
        self.time_stamps = None
        self.spectra = None
        self.pvst = None
        self.total_pressures = None
        self.rtd_temperatures = None
        self.flange_temperatures = None
        self.analog_Vin_signals = None
        self.analog_Iin_signals = None
        self.gpio_in_signals = None

        self.load_scan_data(filename)

        self.colour = None # Unique colour for gui purpouses

    def load_scan_data(self, filename: str):
        """
        Loads in the entirety of the scan data and metadata for the RGASoft .rgadata filetype.
        Takes in the location of a .rgadata file and populates the RgaScan object

        Most of this is lifted verbaitem from the sample code given with the RGASoft installation (more detail in the manual)
        Documentation on the RGASoft RGA data file structure located in manual
        
        Args:
            filename (string): file location
        """
        with open(filename, "rb") as f:
            # File description - 32-byte string
            self.f_identifier = f.read(32)
            
            # File version - int32 value
            self.f_version = read_int(f)
            
            # Single Precision Floating Point - boolean
            self.is_single_precision = read_boolean(f)
            
            # Metadata - QVector of int64 - vector size = 100
            vsize = read_uint(f)
            bytes = f.read(vsize * 8)  # vector values
            metadata_list = [struct.unpack('q', bytes[8*i:8*i+8])[0] for i in range(vsize)]
            
            # Decode Metadata
            settings_location = metadata_list[0]
            data_location = metadata_list[1]
            settings_size = metadata_list[2]  # size of (JSON) settings block
            data_size = metadata_list[3]  # size of data block
            number_of_cycles = metadata_list[4]  # how many cycles of scan data
            single_cycle_data_size = metadata_list[5]  # size of a single cycle
            number_of_active_scan_steps = metadata_list[6]
            upper_index = 7 + number_of_active_scan_steps
            step_data_sizes = metadata_list[7:upper_index]  # data size of individual steps
                # Calculation:
                # data_size = single_cycle_data_size * number_of_cycles
                # single_cycle_data_size = SumOf(step_data_sizes) + Auxiliary_signal_sizes

            # The Settings in the JSON format can give the details of the scan sequence:
            #  How many steps, what kind of scan in each step, what settings for
            #  the mass range (Start/Stop mass), or how many individual mass used
            #  in the PvsT mode, etc.

            # Skip to the settings
            f.seek(settings_location)
            bytes = f.read(settings_size)
            json_string_len = struct.unpack('i', bytes[0:4])[0]
            bytes = bytes[4:]  # slice to get the content portion
            json_string = bytes.decode('utf-8')
            json_settings = json.loads(json_string)
            # print(json.dumps(json_settings, indent=4))

            self.pointsPerAmu = json_settings["cfgs"][0]["pointsPerAmu"]
            self.scanRate =  json_settings["cfgs"][0]["scanRate"]
            self.startMass = json_settings["cfgs"][0]["startMass"]
            self.stopMass = json_settings["cfgs"][0]["stopMass"]
            
            # Skip to the scan data
            f.seek(data_location)

            self.time_stamps = []
            self.spectra = []
            self.pvst = []
            self.total_pressures = []
            self.rtd_temperatures = []
            self.flange_temperatures = []
            self.analog_Vin_signals = []
            self.analog_Iin_signals = []
            self.gpio_in_signals = []
            for cycle in range(number_of_cycles):
                
                # Auxiliary signals
                if self.f_version > 17:
                    # Total pressure
                    total_pressure = read_float(f)
                    self.total_pressures.append(total_pressure)
                    
                    # RTD temperature
                    rtd_t = read_float(f)
                    self.rtd_temperatures.append(rtd_t)
                    
                    # Flange temperature
                    flange_t = read_float(f)
                    self.flange_temperatures.append(flange_t)
                    
                    # Analog Vin
                    analog_Vin = read_float(f)
                    self.analog_Vin_signals.append(analog_Vin)
                    
                    # Analog Iin
                    analog_Iin = read_float(f)
                    self.analog_Iin_signals.append(analog_Iin)
                    
                    # GPIO input
                    gpio_in = read_int(f)
                    self.gpio_in_signals.append(gpio_in)
                
                # Step data
                for step in range(len(step_data_sizes)):
                    # print('Step ', step + 1)
                    # Time stamp
                    time_stamp = read_int64(f)  # in ms
                    # print('Time stamp =', time_stamp, 'ms')
                    self.time_stamps.append(time_stamp)
                    
                    if (step == 0):  # Analog/Histogram scan step
                        # Signal intensities - QVector of float
                        vsize = read_uint(f)  # vsize = ((stop_mass - start_mass) / points_per_amu) + 1
                        # print('vsize (number of data points) =', vsize)
                        bytes = f.read(vsize * 4)
                        scan_signals = []
                        scan_signals = [struct.unpack('f', bytes[4*i:4*i+4])[0] for i in range(vsize)]
                        self.spectra.append(scan_signals)
                        # print('Spectrum signals =', scan_signals)
                    elif (step == 1):  # PvsT scan step
                        # Extract the number of gases from JSON
                        json_step2 = json_settings['cfgs'][1]
                        json_gases = json_step2['gases']
                        n_gases = len(json_gases)
                        # print('PvsT number of gases =', n_gases)
                        # print('PvsT gases =', json_gases)
                        # Signal intensities - N gases: N float values
                        scan_signals = []
                        bytes = f.read(n_gases * 4)
                        scan_signals = [struct.unpack('f', bytes[4*i:4*i+4])[0] for i in range(n_gases)]
                        self.pvst.append(scan_signals)
                        # print('PvsT signals =', scan_signals)
                
                    if SKIP_STEP2_DATA:
                        # Skip next step's data
                        second_step_data_size = step_data_sizes[1]
                        f.seek(second_step_data_size, 1)  # skip N bytes from the current file position
                        break
            
            # Makes scan spectra into np array for easier usage
            self.spectra = np.array(self.spectra)

    def amu_axis(self) -> np.ndarray:
        """Creates the x axis data for an AMU vs. y Plot

        Returns:
            np.ndarray: An np.ndarray containing all AMU axis points
        """

        total_data_points_per_cycle = (self.stopMass - self.startMass) * self.pointsPerAmu + 1
        amu_vector =  np.linspace(self.startMass, self.stopMass, total_data_points_per_cycle)
        return amu_vector
    
    def number_of_cyles(self) -> int:
        return len(self.spectra) - 1

    def get_cycle(self, index: int) -> int:
        return self.spectra[index]

    # def torr_axis(self, index: int):
    #     """Returns the torr_array of a specific index, """

class RgaScanList(QObject):

    scan_added = Signal(object)  
    scan_removed = Signal(object)  

    def __init__(self):
        super().__init__()

        self.scan_files = []

        self.plot_colours = [
            "#1f77b4",  # blue
            "#ff7f0e",  # orange
            "#2ca02c",  # green
            "#d62728",  # red
            "#9467bd",  # purple
            "#8c564b",  # brown
            "#e377c2",  # pink
            "#7f7f7f",  # gray
            "#bcbd22",  # olive
            "#17becf",  # cyan
            "#aec7e8",  # light blue
            "#ffbb78",  # light orange
]
        self.available_plot_colours = self.plot_colours.copy()

    def add_scan(self, scan: RgaScan):
        """Adds a scan to the internal list and emits a signal to update Plot and GUI elements

        Args:
            scan (RgaScan): The RgaScan object of the newly added scan
        """
        # Repopulates available plot colours if ever exausted
        if not self.available_plot_colours: 
            self.available_plot_colours = self.plot_colours.copy()

        # Allocates a colour to the new scan
        gui_colour = self.available_plot_colours.pop(0)
        scan.colour = gui_colour

        self.scan_files.append(scan)
        self.scan_added.emit(scan) # Emits signal to update Plot and GUI

    def remove_scan(self, scan: RgaScan):

        self.available_plot_colours.insert(0, scan.colour) # Frees up colour by adding back to pool for reassignment 
        self.scan_files.remove(scan)
        self.scan_removed.emit(scan) # Emits signal to update Plot and GUI

    def get_scan(self, index: int) -> RgaScan:
        return self.scan_files[index]
    
    def number_of_scans(self) -> int:
        return len(self.scan_files)
    
    def __len__(self) -> int:
        return len(self.scan_files)