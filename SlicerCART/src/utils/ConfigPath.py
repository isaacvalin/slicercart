from utils.requirements import *
from utils.constants import *
from utils.debugging_helpers import *

OUTPUT_CONFIG_PATH = 'output_path.txt' # Name of the temp file where the path
# of the config file to use (from selected output folder). To use here only.

class ConfigPath():
    @enter_function
    def __init__(self):
        self.set_config_values(INITIAL_CONFIG_FILE)

        # Essential for classification comboboxes versioning
        self.flag_combobox = True
        self.flag_remove_combobox = True
        self.combobox_version = 'v00'

    @enter_function
    def check_existing_configuration(self):
        """
        Check if a configuration file already exists in selected output folder.
        """

        path_to_saved_config_files = \
            f'{self.outputFolder}{os.sep}{CONF_FOLDER_NAME}'
        path_to_config_copy = \
            f'{path_to_saved_config_files}{os.sep}{CONFIG_COPY_FILENAME}'

        if os.path.exists(path_to_saved_config_files) == False:
            os.makedirs(path_to_saved_config_files)
            shutil.copy(CONFIG_FILE_PATH, path_to_config_copy)
        else:
            self.path_to_config_copy = path_to_config_copy
            self.config_yaml.clear()
            self.config_yaml = ConfigPath.open_project_config_file()
            ConfigPath.create_temp_file(name=OUTPUT_CONFIG_PATH,
                                        text=self.path_to_config_copy)

    @enter_function
    def open_project_config_file(self):
        """
        Load the appropriate configuration template from module or project if
        exists.
        """

        temp_file_exist = ConfigPath.get_temp_file()

        if temp_file_exist:
            with open(CONFIG_FILE_PATH, 'r') as file:
                self.config_yaml = yaml.safe_load(file)
        else:
            temp_dir = tempfile.gettempdir()
            temp_file_path = os.path.join(temp_dir, OUTPUT_CONFIG_PATH)
            # Read data of the temp file
            with open(temp_file_path, "r") as temp_file:
                output_path = temp_file.read()
            with open(output_path, 'r') as file:
                self.config_yaml = {}
                self.config_yaml = yaml.safe_load(file)

        return self.config_yaml

    @enter_function
    # Was in the initial code. Kept here for further usage if needed.
    def verify_empty(self):
        """
        verify_empty

        Args:
        """
        if self.outputFolder is not None and os.path.exists(self.outputFolder):

            content_of_output_folder = os.listdir(self.outputFolder)
            if '.DS_Store' in content_of_output_folder:
                content_of_output_folder.remove('.DS_Store')

            if len(content_of_output_folder) > 0:
                self.outputFolder = None

                msg = qt.QMessageBox()
                msg.setIcon(qt.QMessageBox.Critical)
                msg.setText("Error : The output folder must be empty ")
                msg.setInformativeText(
                    'Given that there is a new configuration of SlicerCART, '
                    'the output folder must be empty. ')
                msg.setWindowTitle("ERROR : The output folder must be empty ")
                msg.exec()
            else:
                self.check_existing_configuration()

    @enter_function
    def create_temp_file(self, name='output_folder_not_selected.txt',
                         text="Output folder not yet selected.\n"):
        """
        Create a temporary file for 1) using as a flag to check if output
        folder has een selected or not 2) saving the path of the config file
        in the selected output folder if selected (so it can be used).
        """

        # Create a temporary file
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, name)
        # Write some initial data to the file
        with open(temp_file_path, "w") as temp_file:
            temp_file.write(text)

    @enter_function
    def get_temp_file(self, name='output_folder_not_selected.txt'):
        """
        Verify if a specific temp file exists or not. By default, allows to
        detect if output folder has een selected or not.
        """

        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, name)

        try:
            # Write some initial data to the file
            with open(temp_file_path, "r") as temp_file:
                content = temp_file.read()
        except FileNotFoundError:
            return False

        return True

    @enter_function
    def delete_temp_file(self, name='output_folder_not_selected.txt'):
        """
        Delete a specific temp file if it exists.
        """

        # Get the path to the temporary file
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, name)

        # Check if the file exists
        if os.path.exists(temp_file_path):
            # Delete the file
            os.remove(temp_file_path)

    @enter_function
    def read_temp_file(self, name='output_folder_not_selected.txt'):
        """
        Read a specific temp file and return the contents.
        """

        # Get the path to the temporary file
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, name)

        # Open the file and read its contents
        with open(temp_file_path, "r") as file:
            content = file.read()
            return content

    @enter_function
    def write_config_file(self):
        """
        Write self.config_yaml in the appropriate location (initial or
        in the output folder configuration file).
        """

        temp_file_exist = ConfigPath.get_temp_file()

        if temp_file_exist:
            with open(CONFIG_FILE_PATH, 'w') as file:
                yaml.safe_dump(self.config_yaml, file)
        else:
            output_path = ConfigPath.read_temp_file(name=OUTPUT_CONFIG_PATH)
            with open(output_path, 'w') as file:
                yaml.safe_dump(self.config_yaml, file)

        # Ensure to get the latest config values
        ConfigPath.set_config_values(self.config_yaml)

    @enter_function
    def write_correct_path(self):
        """
        Ensure the temp file has the appropriate config file path,
        """

        path_to_saved_config_files = \
            f'{self.outputFolder}{os.sep}{CONF_FOLDER_NAME}'
        path_to_config_copy = \
            f'{path_to_saved_config_files}{os.sep}{CONFIG_COPY_FILENAME}'

        ConfigPath.create_temp_file(name=OUTPUT_CONFIG_PATH,
                                    text=path_to_config_copy)

    @enter_function
    def set_config_values(self, config):
        """
        Function moved from SlicerCART.py. Enables to select configuration
        values from a specified config file (for example, the latest). In
        fact, THIS IS A SETTER FUNCTION: it updates the config values from
        the config file passed in parameter.
        :param config: config yaml file content
        :return: config yaml file content
        """

        self.IS_DISPLAY_TIMER_REQUESTED = config[
            "is_display_timer_requested"]

        self.INPUT_FILE_EXTENSION = config["input_filetype"]
        self.DEFAULT_VOLUMES_DIRECTORY = config["default_volume_directory"]
        self.DefaultDir = self.DEFAULT_VOLUMES_DIRECTORY
        self.DEFAULT_SEGMENTATION_DIRECTORY = config[
            "default_segmentation_directory"]

        self.MODALITY = config["modality"]
        self.IS_CLASSIFICATION_REQUESTED = config[
            "is_classification_requested"]
        self.IS_SEGMENTATION_REQUESTED = config[
            "is_segmentation_requested"]
        self.IS_MOUSE_SHORTCUTS_REQUESTED = config[
            "is_mouse_shortcuts_requested"]
        self.IS_KEYBOARD_SHORTCUTS_REQUESTED = config[
            "is_keyboard_shortcuts_requested"]

        self.INTERPOLATE_VALUE = config["interpolate_value"]
        self.REQUIRE_EMPTY = config["require_empty"]
        self.ENABLE_DEBUG = config["enable_debug"]

        self.WORKING_LIST_FILENAME = config["working_list_filename"]
        self.REMAINING_LIST_FILENAME = config["remaining_list_filename"]

        self.CT_WINDOW_WIDTH = config["ct_window_width"]
        self.CT_WINDOW_LEVEL = config["ct_window_level"]

        self.REQUIRE_VOLUME_DATA_HIERARCHY_BIDS_FORMAT = config[
            "impose_bids_format"]

        self.KEEP_WORKING_LIST = config["keep_working_list"]
        self.SAVE_UINT8 = config["save_uint8"]

        if self.MODALITY == 'CT':
            # then BIDS not mandatory because it is not yet supported
            # therefore, either .nrrd or .nii.gz accepted
            REQUIRE_VOLUME_DATA_HIERARCHY_BIDS_FORMAT = False
            # CT_WINDOW_WIDTH = config["ct_window_width"]
            # CT_WINDOW_LEVEL = config["ct_window_level"]

        elif self.MODALITY == 'MRI':
            # therefore, .nii.gz required
            # INPUT_FILE_EXTENSION = '*.nii.gz'
            # user can decide whether to impose bids or not
            REQUIRE_VOLUME_DATA_HIERARCHY_BIDS_FORMAT = config[
                "impose_bids_format"]

        return config

    def set_output_folder(self, outputFolder):
        """
        Set output folder to ConfigPath class.
        """
        self.outputFolder = outputFolder

    @enter_function
    def get_initial_config_after_modif(self):
        """
        Read the initial configuration file. To use after Slicer
        Configuration Set Up Window has been modified.
        :return: content of the initial configuration file (dictionary)
        """
        # Read at startup the initial config file
        with open(CONFIG_FILE_PATH, 'r') as file:
            content = yaml.safe_load(file)
        return content

    @enter_function
    def extract_config_classification(self, content):
        """
        Get only the classification configuration from the content of a
        config file.
        :param content: content of a config file
        :return: classification labels as a dictionary
        """
        classif_dict = {}
        for element in CLASSIFICATION_BOXES_LIST:
            classif_dict[element] = content[element]
        return classif_dict

    @enter_function
    def compare_and_merge_classification(self, final_config_file, temp_dict):
        """
        Compare possibly modified classification labels with final config
        file (e.g. in the output folder or the initial config file if output
        folder has not yet been selected).
        :param: final_config_file: content of final config file (dictionary)
        :param: temp_dict: dictionary containing classification labels
        :return: final config file content (all config parameters)
        """

        initial_config_file_dict = (
            ConfigPath.extract_config_classification(final_config_file))

        # Use list() to avoid RuntimeError
        for key in list(
                initial_config_file_dict.keys()):
            if key not in temp_dict:
                del initial_config_file_dict[key]

        # Add or update keys from temp_dict to initial_config_file_dict
        for key, value in temp_dict.items():
            initial_config_file_dict[key] = value

        for element in initial_config_file_dict:
            final_config_file[element] = initial_config_file_dict[element]

        return final_config_file

    ### The following getter and setter relate to comboboxes versioning
    @enter_function
    def get_combobox_flag(self):
        """
        get_combobox_flag

        Args:
        """
        return self.flag_combobox

    @enter_function
    def set_combobox_flag(self, value=False):
        """
        set_combobox_flag

        Args:
            value: Description of value.
        """
        self.flag_combobox = value

    @enter_function
    def get_combobox_version(self):
        """
        get_combobox_version

        Args:
        """
        return self.combobox_version

    @enter_function
    def set_combobox_version(self, value):
        """
        set_combobox_version

        Args:
            value: Description of value.
        """
        self.combobox_version = value

    @enter_function
    def get_comboboxes_versions(self):
        """
        get_comboboxes_versions

        Args:
        """
        return self.all_combobox_version

    @enter_function
    def get_latest_combobox_version(self, config_file):
        """
        get_latest_combobox_version

        Args:
            config_file: Description of config_file.
        """
        if config_file['comboboxes'] != None :
            versions = config_file['comboboxes'].keys()
            self.combobox_version = max(versions, key=lambda k: int(k[1:]))
        return self.combobox_version

    @enter_function
    def set_latest_combobox_version(self, config_file):
        """
        set_latest_combobox_version

        Args:
            config_file: Description of config_file.
        """
        self.combobox_version = self.get_latest_combobox_version(config_file)
        return self.combobox_version

    @enter_function
    def get_remove_combobox_flag(self):
        """
        get_remove_combobox_flag

        Args:
        """
        return self.flag_remove_combobox

    @enter_function
    def set_remove_combobox_flag(self, value=False):
        """
        set_remove_combobox_flag

        Args:
            value: Description of value.
        """
        self.flag_remove_combobox = value

    @enter_function
    def set_interpolate_value(self, value):
        """
        set the interpolation state for rendered volumes.

        Args:
            value: true (interpolation) or false (raw image, not interpolated)
        """
        self.INTERPOLATE_VALUE = value


# Creating an instance of ConfigPath. This ensures that all the same
# config values will be used in the different files/modules.
ConfigPath = ConfigPath()