# Python3 LPD8806 LED Library

![LPD8806 CLI Example](https://i.imgur.com/J6heTvG.png "LPD8806 CLI Example")

## Credit to Sh4d and adammhaile for the initial Python2 implementation: 
* https://github.com/Sh4d/LPD8806
* https://github.com/adammhaile/RPi-LPD8806

## Changes
* Python3 compatibility via _2to3_ utility
* Fixed inaccurate color mapping
* Includes CLI for LED controls
* Control LED's via simple JSON config files

## Install
```
git clone git@github.com:edmundpf/LPD8806_Python3.git
cd LPD8806_Python3/
```

## Install CLI
```
cd /usr/bin/
sudo bash -c 'cat > led'
cd /home/pi/LED && py master.py "$@"
```
* Hit _enter_ then _ctrl+c_ to save
```
sudo chmod +x led
```
* Now you can use the CLI anywhere on the system via the **led** command

## Usage
### Without CLI installed (must be called within root directory i.e. _LPD8806_Python3/_)
```
python3 master.py -f actions/rainbow.json
```
### With CLI installed (can be called system-wide)
```
led -f actions/rainbow.json
```
### CLI flags
* -f, --file
  * **Choose config file** by entering relative or absolute file path
  * `-f /mydir/example.json`
* -d, --duration
  * **Choose action sleep duration** in seconds
  * _Only applies to config files with a **single action**_
  * A duration of _0_ will not include any sleep
  * Useful for turning LED's off at a certain time (can be paired with _cron_ for automation)
  * `-d 300`
* -l, --loops
  * **Choose number of loops**
  * _Only applies to config files with a **single action**_
  * A loops value of _-1_ will run indefinitely until a keyboard interrupt (_ctrl+c_)
  * Loops with values _0 and 1_ will run once, loops of _2 or greater_ will run the respective amount
  * `-l 4`
* -a, --args
  * **Modify arguments in config file**
  * _Applies to **all actions**_
  * Can input multiple args, config file args will be overwritten in order of arguments
  * For example let's look at the _color.json_ preset config file:
  ```
    [
      {
        "duration": 0,
        "loops": 0,
        "action": "color",
        "args": {"color": null}
      }
    ]
  ```
  * This config file expects one argument for _"color":_ `"args": {"color": null}` as a hex color code
  * The default null value will be overwritten with the argument you entered
  * `-a 0000FF`
* Presets
  * --off
    * Turns all LED's off
    * `led --off`
  * --color
    * Sets LED's a static color until keyboard interrupt
    * `led --color 00FF00`
  * --rainbow
    * Plays rainbow animation unti keyboard interrupt
    * `led --rainbow`
* Any number of these args can be combined to customize your config files
  * `led -f actions/color.json -a FF0000 -l 0 -d 3600`
* The CLI args are meant for modifying config files with a _single action_, config files with multiple actions should have all their respective args hard-coded and should only include the _file_ argument in the CLI
  * `led /mydir/multi-action.json`
  
## Config File

* The config file is a _list of actions_
* Each _action_ includes the following attributes:
  * **duration**
    * Duration of script in seconds
  * **loops**
    * Number of loops
  * **action**
    * Action type
    * **TO-DO: add more actions to CLI**
  * **args**
    * Required arguments for the respective action (name-sensitive)
    * Set to empty: `"args": {}` for actions with no arguments
    * **TO-DO: define and document action names for respective actions**
  * Action types
    * **off**
      * Turns all LED's off
    * **color**
      * Sets LED's a static color
      * Turns off after execution
      * Args
        * _color_
          * Hexadecimal color code: `"args": {"color": "FF0000"}`
    * **rainbow**
      * LED's change color from end-to-end in a rainbow sequence
      * Turns off after execution
  * Single Actions
    * _duration, loops, and args_ can be modified via CLI
    ```
    [
      {
        "duration": 0,
        "loops": -1,
        "action": "rainbow",
        "args": {}
      }
    ]
    ```
  * Multiple Actions
    * Arguments **CANNOT** be modified via CLI (just call the config file name)
    ```
    [
      {
        "duration": 4,
        "loops": 2,
        "action": "color",
        "args": {"color": "A833FF"}
      },
      {
        "duration": 6,
        "loops": 1,
        "action": "color",
        "args": {"color": "33FF8D"}
      }
    ]
    ```
## LED Configuration
  * RGB Configuration
    * Some LED strips do not have an _RGB_ color scheme, and thus will display unexpected colors
    * To choose the correct color scheme for you LED strip, edit _/raspledstrip/ledstrip.py_
    * Replace `self.c_order = ChannelOrder.RGB` with your color scheme i.e. `self.c_order = ChannelOrder.GRB`
  * Master Brightness
    * You may find your RGB strip is _too bright._ To choose a master brightness, edit _/raspledstrip/ledstrip.py_
    * Replace `self.masterBrightness = 1.0` with your preferred brightness i.e. `self.masterBrightness = 0.5`
## Contributing
  * If you wish to contribute to the project (add more actions, add more example .JSON configs, improve stability, etc.) please submit a pull request! Thanks!
