## Brian Blaylock
## April 8, 2021

"""
========
Palettes
========

Color pallettes for various organizations.
"""

# University of Utah
# https://umc.utah.edu/wp-content/uploads/2014/12/Web-Style-Guide-2014_v2.pdf
university_of_utah = dict(red="#CC0000", black="#000000", grey="#808080")

# BYU
# https://brand.byu.edu/brand-guidelines/colors/
BYU = dict(navy="#002E5D", white="#FFFFFF", royal="#0062B8")

# Naval Research Lab
# from Design Guide on Pipline
naval_research_lab = dict(
    navy="#162956",
    blue="#2E5590",
    light_blue="#6DA9CF",
    gray="#4C4F59",
    yellow="#FAB208",
)

# NASA
# https://w3.cs.jmu.edu/bernstdh/web/common/policies/NASA_StyleGuide_Nov06.pdf
NASA = dict(
    red="#FC3D21",
    blue="#0B3D91",
    grey="#797979",
    black="#000000",
)

# NOAA
# https://stratus.ssec.wisc.edu/aspb/NESDIS_Style_Guide_Policy.pdf
NOAA = dict(
    blue="#254290",
    lightblue="#00ADEF",
)

# USPS
# https://usbrandcolors.com/usps-colors/
usps = dict(blue="#004B87", red="#DA291C", black="#000000")

# Bootstrap 4
# https://colorswall.com/palette/3/
bootstrap = dict(
    primary="#0275d8",
    success="#5cb85c",
    info="#5bc0de",
    warning="#f0ad4e",
    danger="#d9534f",
    inverse="#292b2c",
    faded="#f7f7f7",
)

# Muppet
# https://muppet.fandom.com/wiki/Sandbox:Pantone
muppet = dict(
    kermit="#96FF38",
    piggy="#FFBFD1",
    rowlf="#853100",
    gonzo="#0089CC",
    fozzie="#FC9200",
    animal="#FF173D",
    beaker="#FF2E14",
    honeydew="#DEFA55",
    beauregard="#506700",
    drteeth="#6EFF00",
    floydPepper="#91A1FF",
    janice="#F0AD00",
    link="#FFD9C7",
    pepe="#F5002F",
    rizzo="#8F4A06",
    sam="#4FEDFF",
    scooter="#FFA61A",
    statler="#FFE0B8",
    waldorf="#FFC7A8",
    swedishChef="#FFD9C7",
    sweetums="#4A1A00",
)

# Sesame Street
# https://static.wikia.nocookie.net/muppet/images/e/e9/Ssstyleguide2001.jpg/revision/latest?cb=20200325143152
sesameStreet = dict(
    bigBird="#FFE600",
    bert="#FFE600",
    ernie="#F9A13A",
    cookieMonster="#0099D7",
    count="#BA96C7",
    elmo="#EF3F34",
    grover="#1C91FF",
    oscar="#7BC242",
    rosita="#9DD7C6",
    zoe="#FDB947",
    rubberDucky="#FEFF54",
)

# GNOME Project
# https://developer.gnome.org/hig/reference/palette.html
gnome = {
    "Blue 1": "#99c1f1",
"Blue 2": "#62a0ea",
"Blue 3": "#3584e4",
"Blue 4": "#1c71d8",
"Blue 5": "#1a5fb4",
"Green 1": "#8ff0a4",
"Green 2": "#57e389",
"Green 3": "#33d17a",
"Green 4": "#2ec27e",
"Green 5": "#26a269",
"Yellow 1": "#f9f06b",
"Yellow 2": "#f8e45c",
"Yellow 3": "#f6d32d",
"Yellow 4": "#f5c211",
"Yellow 5": "#e5a50a",
"Orange 1": "#ffbe6f",
"Orange 2": "#ffa348",
"Orange 3": "#ff7800",
"Orange 4": "#e66100",
"Orange 5": "#c64600",
"Red 1": "#f66151",
"Red 2": "#ed333b",
"Red 3": "#e01b24",
"Red 4": "#c01c28",
"Red 5": "#a51d2d",
"Purple 1": "#dc8add",
"Purple 2": "#c061cb",
"Purple 3": "#9141ac",
"Purple 4": "#813d9c",
"Purple 5": "#613583",
"Brown 1": "#cdab8f",
"Brown 2": "#b5835a",
"Brown 3": "#986a44",
"Brown 4": "#865e3c",
"Brown 5": "#63452c",
"Light 1": "#ffffff",
"Light 2": "#f6f5f4",
"Light 3": "#deddda",
"Light 4": "#c0bfbc",
"Light 5": "#9a9996",
"Dark 1": "#77767b",
"Dark 2": "#5e5c64",
"Dark 3": "#3d3846",
"Dark 4": "#241f31",
"Dark 5": "#000000"
}

gnome1 = {k:v for k, v in gnome.items() if k.endswith('1')}
gnome2 = {k:v for k, v in gnome.items() if k.endswith('2')}
gnome3 = {k:v for k, v in gnome.items() if k.endswith('3')}
gnome4 = {k:v for k, v in gnome.items() if k.endswith('4')}
gnome5 = {k:v for k, v in gnome.items() if k.endswith('5')}
