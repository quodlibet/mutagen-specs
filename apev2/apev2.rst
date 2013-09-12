APEv2
=====

This is how information is laid out in an APEv2 tag:

================= =============
APE Tags Header_  32 bytes
----------------- -------------
APE Tag Item_ 1   10.. bytes
----------------- -------------
APE Tag Item_ 2   10.. bytes
----------------- -------------
...               10.. bytes
----------------- -------------
APE Tag Item_ n-1 10.. bytes
----------------- -------------
APE Tag Item_ n   10.. bytes
----------------- -------------
APE Tags Footer_  32 bytes
================= =============

APE tag items should be sorted ascending by size. When streaming, parts of
the APE tags can be dropped to reduce danger of drop outs between titles.
This is not a must, but strongly recommended. Actually the items should be
sorted by importance/byte, but this is not feasible. Only break this rule
if you add less important small items and you don't want to rewrite the
whole tag. An APE tag at the end of a file (strongly recommended) must have
at least a footer, an APE tag in the beginning of a file (strongly
unrecommended) must have at least a header. When located at the end of an
MP3 file, an APE tag should be placed after the the last frame, just before
the ID3v1 tag (if any).

.. _header:

APE Tags Header/Footer
----------------------

Contains number, length and attributes of all tag items

Header and Footer are different in 1 bit in the Tags Flags to distinguish between them.

Member of APE Tag 2.0

+------------------------------+----------+--------------------------------------------+
|Preamble                      | 64 bits  | { 'A', 'P', 'E', 'T', 'A', 'G', 'E', 'X' } |
+------------------------------+----------+--------------------------------------------+
|| Version Number, Bits 0...7  | 32 bits  | 1000 = Version 1.000 (old)                 |
|| Version Number, Bits 8...15 |          | 2000 = Version 2.000 (new)                 |
|| Version Number, Bits 16...23|          |                                            |
|| Version Number, Bits 24...31|          |                                            |
+------------------------------+----------+--------------------------------------------+
|| Tag Size, Bits 0... 7       | 32 bits  | Tag size in bytes including footer and all |
|| Tag Size, Bits 8...15       |          | tag items excluding the header to be as    |
|| Tag Size, Bits 16...23      |          | compatible as possible with APE Tags 1.000 |
|| Tag Size, Bits 24...31      |          |                                            |
+------------------------------+----------+--------------------------------------------+
|| Item Count, Bits 0... 7     |  32 bits | Number of items in the Tag (n)             |
|| Item Count, Bits 8...15     |          |                                            |
|| Item Count, Bits 16...23    |          |                                            |
|| Item Count, Bits 24...31    |          |                                            |
+------------------------------+----------+--------------------------------------------+
|| Tags Flags, Bits 0... 7     |  32 bits | Global flags of all items                  |
|| Tags Flags, Bits 8...15     |          | (there are also private flags for          |
|| Tags Flags, Bits 16...23    |          | every item)                                |
|| Tags Flags, Bits 24...31    |          |                                            |
+------------------------------+----------+--------------------------------------------+
|Reserved                      |  64 bits |    Must be zero                            |
+------------------------------+----------+--------------------------------------------+


Ape Tags Flags
--------------

Contains attribute of the tag (bit 31...) and of a item (bit 0...)

Member of APE Tags Header, Footer or Tag item

Note: APE Tags 1.0 do not use any of the APE Tag flags. All are set to zero
on creation and ignored on reading.


Bit 31
 * 0: Tag contains no header
 * 1: Tag contains a header

Bit 30
 * 0: Tag contains a footer
 * 1: Tag contains no footer

Bit 29
 * 0: This is the footer, not the header
 * 1: This is the header, not the footer

Bit 28...3
    Undefined, must be zero

Bit 2...1
 * 0: Item contains text information coded in UTF-8
 * 1: Item contains binary information*
 * 2: Item is a locator of external stored information**
 * 3: reserved

Bit 0
 * 0: Tag or Item is Read/Write
 * 1: Tag or Item is Read Only


[*] Binary information: Information which should not be edited by a text
editor, because

* Information is not a text.
* Contains control characters
* Contains internal restrictions which can't be handled by a normal text editor
* Can't be easily interpreted by humans.


[**] Allowed formats:

* http://host/directory/filename.ext
* ftp://host/directory/filename.ext
* filename.ext
* /directory/filename.ext
* DRIVE:/directory/filename.ext

Note: Locators are also UTF-8 encoded. This can especially occur when
filenames are encoded.

.. _item:

APE Tag Item
------------

An APE tag item is a value assigned by a key.

Member of APE Tag Version 2.0


Note:

* APE Tags Item Key are case sensitive.
* Nevertheless it is forbidden to use APE Tags Item Key which only differs
  in case.
* And nevertheless Tag readers are recommended to be case insensitive.
* Every Tag Item Key can only occures (at most) once. It is not possible to
  transmit a Tag Key multiple time to change it contents.
* Tags can be partially or complete repeated in the streaming format.
* This is to make it possible to display artist and title if you missed the
  start of the transmission.
* It is recommended to transmit very important information like artist /
  album / title every 2 minutes and additional 5...10 seconds before the
  end. Be careful and don't transmit these information too often or during
  passages with high bitrate demand to avoid unnecessary drop-outs.


+---------------------------------------+----------+---------------------------------------------+
|| Size of the Item Value, Bits 0...7   | 32 bits  |  Length len of the assigned value in bytes  |
|| Size of the Item Value, Bits 8...15  |          |                                             |
|| Size of the Item Value, Bits 16...23 |          |                                             |
|| Size of the Item Value, Bits 24...31 |          |                                             |
+---------------------------------------+----------+---------------------------------------------+
|| Item Flags, Bits 0...7               | 32 bits  |   Item flags                                |
|| Item Flags, Bits 8...15              |          |                                             |
|| Item Flags, Bits 16...23             |          |                                             |
|| Item Flags, Bits 24...31             |          |                                             |
+---------------------------------------+----------+---------------------------------------------+
|Item Key                               | m bytes  |  Item key, can contain ASCII characters     |
|                                       |          |  from 0x20 (Space) up to 0x7E (Tilde)       |
+---------------------------------------+----------+---------------------------------------------+
|0x00                                   | 1byte    |  Item key terminator                        |
+---------------------------------------+----------+---------------------------------------------+
|Item Value                             | len bytes|  Item value, can be binary data or          |
|                                       |          |  UTF-8 string                               |
+---------------------------------------+----------+---------------------------------------------+


APE Key
-------

* An APE tag item key is a key for accessing special meta-information in an
  audio file.
* Member of APE Tag Item.
* APE tag item keys can have a length of 2 (including) up to 255 (including)
  characters in the range from 0x20 (Space) until 0x7E (Tilde).
* Typical keys should have a length of 2 ... 16 characters using the
  following characters: Space (0x20), Slash (0x2F), Digits (0x30...0x39),
  Letters (0x41...0x5A, 0x61...0x7A).
* Values can contain binary data, a value or a list of values. See here.
  List of values can be mixed, i.e. contain UTF-8 strings and external
  references beginning with file://..., http://www..., ftp://ftp....
* Not allowed are the following keys: ID3, TAG, OggS and MP+.

Currently the following keys are defined:

TODO
