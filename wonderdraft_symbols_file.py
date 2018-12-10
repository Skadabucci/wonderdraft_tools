'''
To use this file set the working_dir, target_folders and prefix.
Make sure your directory structure looks like this:
<working_dir>/<target_folder>/<sprites>/<symbols>/<asset_folder(s)>/<image(s)>
Then just run this as a python3 script.
Also, pip3 install the imgsize module.

TODO: Use os.path or pathlib everywhere!
There are various other todos in here. Feel free to make commits to this helper.
'''
import io
import json
import os

from imgsize import get_size


# TODO: Make this an optional argument. Find this location in the FS.
working_dir = 'C:\\Users\\Anthony\\AppData\\Roaming\\Wonderdraft\\assets'

# These values are used to help set the center of gravity for each image.
# We are going to multiply the height of the image in pixels to these values.
# Since the origin (0, 0) is the center of the image we should only take half
# to bring the y_offset up top.
TOP_OF_IMAGE = 0.5
BOTTOM_OF_IMAGE = -0.5

# Additional movement values
CLOSE_TO_TOP = 0.42
CLOSE_TO_BOTTOM = -0.42
UP = 0.25
DOWN = -0.25

# TODO: This should be a config file instead of hardcoded
offset_y_map = {
    'Bedroll': TOP_OF_IMAGE,
    'Bush': BOTTOM_OF_IMAGE,
    'Tent': BOTTOM_OF_IMAGE,
    'Backpack': DOWN,
    # Dead Trees || Trees
    'Tree': TOP_OF_IMAGE,
    # Rocks
    'Rock': BOTTOM_OF_IMAGE,
    # Roads
    'Road': TOP_OF_IMAGE,
    # Elements
    'Ice Block': TOP_OF_IMAGE,
    'Snow Pile': TOP_OF_IMAGE,
    # Landscapes
    'Grass Field': TOP_OF_IMAGE,
    'Snowy Ground': TOP_OF_IMAGE,
    'Water Texture': TOP_OF_IMAGE,
    # Manmade
    'Bridge': CLOSE_TO_BOTTOM,
    # Cliffsides
    'Cliffside': CLOSE_TO_TOP
}


def create_folder_prefix(base_dir, folder, prefix=None):
    '''Add a prefix to a folder in a given base directory.
    
    If the folder already has the prefix we bail. If the name of the new folder and the old
    folder match or if the folder already has the prefix we bail. Passing a value of None will
    remove the prefix. The prefix will be of the form:
    <prefix> - <folder's original name>
    '''
    if prefix and prefix in folder:
        return  # The prefix already exists, bail.
    try:
        # Try to pull out an already existing prefix eg. "2D - foo" -> "foo"
        folder_no_prefix = folder.split('-')[1].strip()
    except IndexError:
        # There was no prefix on this folder, just clean it up
        folder_no_prefix = folder.strip()

    # Make a prefix or set it to the empty string
    prefix = '{} - '.format(prefix) if prefix is not None else ''
    old_folder_name = '{}\\{}'.format(base_dir, folder)
    new_folder_name = '{}\\{}{}'.format(base_dir, prefix, folder_no_prefix)

    if old_folder_name == new_folder_name:
        print('Skipping Rename, old folder name matches new folder name.')
        return

    print(
        "Renaming: \n...\\{} \n...\\{}".format(
            old_folder_name.split('\\')[-1],
            new_folder_name.split('\\')[-1]
        )
    )
    # os.rename(old_filename, new_filename)

def make_symbols_file(directory):
    '''Create the wonderdraft_symbols file here.

    We default the offset_x to 0 always. offset_y can be overwritten with the offset_y_map, and
    radius is always calculated as the minimum of 15% of the smallest image dimension OR 100.
    '''
    symbols_file_json = {}
    for filename in os.listdir(directory):
        offset_y = 0
        if filename.startswith('.'):
            continue

        # Calculate the radius
        with io.open('{}\\{}'.format(directory, filename), 'rb') as fobj:
            width, height = get_size(fobj)
            # TODO: make these arguments that get passed in.
            radius = min(min(width, height) * .15, 100)

        # Determine if we are going to overwrite the offset_y from the offset_y_map
        for offset_keyname, offset_y_value in offset_y_map.items():
            if offset_keyname.lower() in filename.lower():
                offset_y = offset_y_value * height

        key_name = filename.split('.')[0]  # Take out .png in the filename
        symbols_file_json[key_name] = {
            "name": key_name,
            "radius": int(radius),
            "offset_x": int(0),
            "offset_y": int(offset_y),
            "draw_mode": "normal"
        }

    # Write the dict to the file as json
    symbols_filename = '{}\\{}'.format(directory, '.wonderdraft_symbols')
    print('Writing file {}'.format(symbols_filename))
    with io.open(symbols_filename, 'w+') as f:
        f.write(json.dumps(symbols_file_json, indent=4))


def main():
    # TODO: make these arguments
    prefix = '2D'  # A prefix set on each of the folders that hold the wonderdraft_symbols file.
    target_folders = ['\\Exterior Assets', '\\Interior Assets']
    # TODO: Automatically create the sprites/symbols directory if it doesn't exist and move everything in there.
    local_path = '\\sprites\\symbols'

    for target in target_folders:
        symbols_directory = working_dir + target + local_path
        for asset_folder in os.listdir(symbols_directory):
            symbol_pack_dir = '{}\\{}'.format(symbols_directory, asset_folder)
            create_folder_prefix(symbols_directory, asset_folder, prefix=prefix)
            make_symbols_file(symbol_pack_dir)


if __name__ == '__main__':
    main()
