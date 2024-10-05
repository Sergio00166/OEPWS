# Main database for PBTE

from os import sep


# Define binary ASCII control chars and it graphical representation
ascii_map = {
    0x00: '␀',  # Null
    0x01: '␁',  # Start of Heading
    0x02: '␂',  # Start of Text
    0x03: '␃',  # End of Text
    0x04: '␄',  # End of Transmission
    0x05: '␅',  # Enquiry
    0x06: '␆',  # Acknowledge
    0x07: '␇',  # Bell
    0x08: '␈',  # Backspace
    0x0A: '␊',  # Line Feed
    0x0B: '␋',  # Vertical Tab
    0x0C: '␌',  # Form Feed
    0x0D: '␍',  # Carriage Return
    0x0E: '␎',  # Shift Out
    0x0F: '␏',  # Shift In
    0x10: '␐',  # Data Link Escape
    0x11: '␑',  # Device Control 1
    0x12: '␒',  # Device Control 2
    0x13: '␓',  # Device Control 3
    0x14: '␔',  # Device Control 4
    0x15: '␕',  # Negative Acknowledge
    0x16: '␖',  # Synchronous Idle
    0x17: '␗',  # End of Transmission Block
    0x18: '␘',  # Cancel
    0x19: '␙',  # End of Medium
    0x1A: '␚',  # Substitute
    0x1B: '␛',  # Escape
    0x1C: '␜',  # File Separator
    0x1D: '␝',  # Group Separator
    0x1E: '␞',  # Record Separator
    0x1F: '␟',  # Unit Separator
    0x7F: '␡'   # Delete
}
# Create a map with all the graphical symbols
ascii_replaced = [ascii_map[x] for x in ascii_map]+[">","<","�"]
# Create a map without LF and CR
ascii_no_lfcr = [x for x in ascii_map if chr(x) not in ["\n", "\r"]]

# Here we have all the mapped scape codes for the keys
if sep == chr(92):  # Windows
    keys = {
        "delete": b'\x08',
        "return": b'\r',
        "ctrl+s": b'\x13',
        "ctrl+d": b'\x04',
        "ctrl+n": b'\x0e',
        "ctrl+x": b'\x18',
        "ctrl+c": b'\x03',
        "ctrl+p": b'\x10',
        "ctrl+g": b'\x07',
        "ctrl+a": b'\x01',
        "ctrl+o": b'\x0f',
        "ctrl+b": b'\x02',
        "ctrl+q": b'\x11',
        "ctrl+k": b'\x0b',
        "ctrl+u": b'\x15',
        "ctrl+f": b'\x06',
        "ctrl+t": b'\x14',
        "ctrl+r":b'\x12',
        "arr_up": b'\xe0H',
        "arr_down": b'\xe0P',
        "arr_right": b'\xe0M',
        "arr_left": b'\xe0K',
        "ctrl+arr_up": b'\xe0\x8d',
        "ctrl+arr_down": b'\xe0\x91',
        "ctrl+arr_left": b'\xe0s',
        "ctrl+arr_right": b'\xe0t',
        "ctrl+repag": b'\xe0\x86',
        "ctrl+avpag": b'\xe0v',
        "supr": b'\xe0S',
        "start": [b'\xe0G'],
        "end": [b'\xe0O'],
        "repag": b'\xe0I',
        "avpag": b'\xe0Q',
        "tab": b'\t',
        "insert": b'\xe0R',
        "alt+k": b'\x00%',
        "alt+u": b'\x00\x16',
        "alt+i": b'\x00\x17',
        "alt+d": b'\x00 ',
    }

else:  # Linux
    keys = {
        "delete": b'\x7f',
        "return": b'\r',
        "ctrl+s": b'\x13',
        "ctrl+d": b'\x04',
        "ctrl+n": b'\x0e',
        "ctrl+x": b'\x18',
        "ctrl+c": b'\x03',
        "ctrl+p": b'\x10',
        "ctrl+g": b'\x07',
        "ctrl+a": b'\x01',
        "ctrl+o": b'\x0f',
        "ctrl+b": b'\x02',
        "ctrl+q": b'\x11',
        "arr_up": b'\x1b[A',
        "arr_down": b'\x1b[B',
        "arr_right": b'\x1b[C',
        "arr_left": b'\x1b[D',
        "supr": b'\x1b[3~',
        "start": [b'\x1b[H',b'\x1b[1~'],
        "end": [b'\x1b[F',b'\x1b[4~'],
        "repag": b'\x1b[5~',
        "avpag": b'\x1b[6~',
        "tab": b'\t',
        "insert": b'2',
        "ctrl+arr_up": b'\x1b[1;5A',
        "ctrl+arr_down": b'\x1b[1;5B',
        "ctrl+arr_left": b'\x1b[1;5D',
        "ctrl+arr_right": b'\x1b[1;5C',
        "ctrl+repag": b'\x1b[5;5~',
        "ctrl+avpag": b'\x1b[6;5~',
        "ctrl+k": b'\x0b',
        "ctrl+u": b'\x15',
        "ctrl+f": b'\x06',
        "ctrl+t": b'\x14',
        "ctrl+r": b'\x12',
        "alt+k": b'\x1bk',
        "alt+u": b'\x1bu',
        "alt+i": b'\x1bi',
        "alt+d": b'\x1bd',
    }
