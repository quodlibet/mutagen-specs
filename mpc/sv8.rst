SV8 Specification
=================

Note: All fields, unless explicitly specified otherwise are read and
written in Big-Endian order.

Status of this document
-----------------------

This document is a work in progress, but part of the document will not be changed.

Here is how the status is indicated for each part:

====================== ===================================================================
Status                 Meaning
====================== ===================================================================
[final]                This part is final and will not be changed
---------------------- -------------------------------------------------------------------
[beta]                 This part will not be changed unless necessary
---------------------- -------------------------------------------------------------------
[alpha]                This part is still discussed and will probably change
---------------------- -------------------------------------------------------------------
nothing specified      This part is here for discussion, and not part of the specification
====================== ===================================================================


File magic number
-----------------

**[final]** Magic number is on 32bits and is equal to 'MPCK' or 0x4D50434B


File extension
--------------

**[final]** The prefered file extension for musepack files is .mpc

Packet formatting
-----------------

**[final]** All packets are formatted using Key / Size / Payload. Keys are 
16 bits long. It's equivalent to the packet ID or type. Size is a 
variable-size field::

    bits, big-endian
    0xxx xxxx                                           - value 0 to  2^7-1
    1xxx xxxx  0xxx xxxx                                - value 0 to 2^14-1
    1xxx xxxx  1xxx xxxx  0xxx xxxx                     - value 0 to 2^21-1
    1xxx xxxx  1xxx xxxx  1xxx xxxx  0xxx xxxx          - value 0 to 2^28-1
    ...


Size defines the packet length in bytes, including the Key and Size fields.
So the minimum length of a block is 3 bytes. The payload is the actual
packet data. Its size can be null. All unused bits in a packet MUST be null.


============= ================ =============
Field         Size (bits)      Value
============= ================ =============
Key           16               "EX"
------------- ---------------- -------------
Size          n*8; 0 < n < 10  0x1A
------------- ---------------- -------------
Payload       Size * 8         "example"
============= ================ =============


Summary of reserved packet keys
-------------------------------

Allowed chars in key are [A-Z] (65 <= value <= 90), so 676 keys are valid
out of 65536 possible.

================== ======= ========= =========
Packet Name        Key     Mandatory Status
================== ======= ========= =========
Stream Header      SH      yes       [final]
------------------ ------- --------- ---------
Replaygain         RG      yes       [final]
------------------ ------- --------- ---------
Encoder Info       EI      no        [final]
------------------ ------- --------- ---------
Seek Table Offset  SO      no        [final]
------------------ ------- --------- ---------
Audio Packet       AP      yes       [final]
------------------ ------- --------- ---------
Seek Table         ST      no        [final]
------------------ ------- --------- ---------
Chapter-Tag        CT      no        [beta]
------------------ ------- --------- ---------
Stream End         SE      yes       [final]
================== ======= ========= =========


Stream Header Packet
--------------------

**[final]** This packet key is "SH". It contains the information needed to
decode the stream. This block is mandatory and must be written before the
first audio packet.

=================== =============== ======= ========================================================
Field               Size (bits)     Value   Comment
=================== =============== ======= ========================================================
CRC                 32                      CRC 32 of the block (this field excluded). 0 = invalid
------------------- --------------- ------- --------------------------------------------------------
Stream version      8               8       Bitstream version
------------------- --------------- ------- --------------------------------------------------------
Sample count        n*8; 0<n<10             Number of samples in the stream. 0 = unknown
------------------- --------------- ------- --------------------------------------------------------
Beginning silence   n*8; 0<n<10             Number of samples to skip at the beginning of the stream
------------------- --------------- ------- --------------------------------------------------------
Sample frequency    3               0..7    See table below
------------------- --------------- ------- --------------------------------------------------------
Max used bands      5               1..32   Maximum number of bands used in the file
------------------- --------------- ------- --------------------------------------------------------
Channel count       4               1..16   Number of channels in the stream
------------------- --------------- ------- --------------------------------------------------------
MS used             1                       True if Mid Side Stereo is enabled
------------------- --------------- ------- --------------------------------------------------------
Audio block frames  3               0..7    Number of frames per audio packet (4^value=(1..16384))
=================== =============== ======= ========================================================

Do we need to specify the channel position ? There seems to be no standard
for positions / order of the channels.

The SV8 stream allows to start decoding only on the first packet frame, so
cutting the stream requires cutting on packet boundaries. Beginning silence
and sample count fields provide more precise cutting possibilities.

Frequency table

===== ==============
Value Frequency (Hz)
===== ==============
0     44100
----- --------------
1     48000
----- --------------
2     37800
----- --------------
3     32000
===== ==============

The CRC used is this one : `<http://www.w3.org/TR/PNG/#D-CRCAppendix
http://www.w3.org/TR/PNG/#D-CRCAppendix>`__.

Replaygain Packet
-----------------

**[final]** This packet key is "RG". It contains the necessary data needed
to apply replaygain on the current stream. This packet is mandatory and
must be written before the first audio packet.

=================== =========== ======= =====================================
Field               Size (bits) Value   Comment
=================== =========== ======= =====================================
ReplayGain version  8           1       The replay gain version
------------------- ----------- ------- -------------------------------------
Title gain          16                  The loudness calculated for the
                                        title, and not the gain that the
                                        player must apply
------------------- ----------- ------- -------------------------------------
Title peak          16
------------------- ----------- ------- -------------------------------------
Album gain          16                  The loudness calculated for the album
------------------- ----------- ------- -------------------------------------
Album peak          16
=================== =========== ======= =====================================

The replay gain values are stored in dB in Q8.8 format.
The 0 value means that this field has not been computed (no gain must be applied in this case.
exemples :

* Replay gain finds that this title has a loudness of 78.56 dB. It will be
  encoded as 78.56 * 256 ~ 20111 = 0x4E8F
* For 16-bit output (range [-32767 32768]), the max is 68813 (out of
  range). It will be encoded as 20 * log10(68813) * 256 ~ 24769 = 0x60C1
* For float output (range [-1 1]), the max is 0.96. It will be encoded as
  20 * log10(0.96 * 2^15^) * 256 ~ 23029 = 0x59F5 (for peak values it is
  suggested to round to nearest higher integer)

Encoder Info Packet
-------------------

**[final]** This packet key is "EI".

======== =========== =============== ======================================
Field    Size (bits) Value           Comment
======== =========== =============== ======================================
Profile  7           0..15.875       quality in 4.3 format
-------- ----------- --------------- --------------------------------------
PNS tool 1           True if enabled
-------- ----------- --------------- --------------------------------------
Major    8           1               Major version
-------- ----------- --------------- --------------------------------------
Minor    8           17              Minor version, even numbers for stable
                                     version, odd when unstable
-------- ----------- --------------- --------------------------------------
Build    8           3               Build
======== =========== =============== ======================================


Seek Table Offset Packet
------------------------

**[final]** This packet key is "SO". It contains an offset to the seek
table packet. This packet must be written before the first audio packet.
This packet must be present if the "ST" packet is present and is written
after the first audio packet.

======= ================ ======= ========================================
Field   Size (bits)      Value   Comment
======= ================ ======= ========================================
Offset  n*8; 0 < n < 10          Offset from this packet to the seek
                                 table packet
======= ================ ======= ========================================


Audio Packet
------------

**[final]** This packet key is "AP". It contains audio frames. The first
frame is a key frame.

============ =========== ==========================================
Field        Size (bits) Comment
============ =========== ==========================================
Audio Frames ?           n (or less if last packet) frames of audio
                         as defined in SH packet
============ =========== ==========================================


Seek Table Packet
-----------------

**[final]** This packet key is "ST".

============= =============== ======= ============================================
Field         Size (bits)     Value   Comment
============= =============== ======= ============================================
Seek Count    n*8; 0 < n < 10         Number of seek elements in this table
------------- --------------- ------- --------------------------------------------
Seek Distance 4               0..15   Distance between referenced blocks = 2^Value
------------- --------------- ------- --------------------------------------------
Seek Data     ?
============= =============== ======= ============================================

Format of seek data:

* Reference offset for seeking is the musepack magic number
* First 2 values are stored using the same code as the packet size code.
* Next values are coded as::

    code = value(n) - 2*value(n-1) + value(n-2)
    code <<= 1;
    if (code < 0)
      code = -code | 1;

code is sent as `golomb code <http://en.wikipedia.org/wiki/Golomb_code>`_
with M = 2^12^.


Chapter-Tag Packet
------------------

**[beta]** This packet key is "CT". It contains a chapter position and
associated tag. There is 1 packet for each chapter. When used in a file,
all CT packets must be consecutive. They must be the next (group of) packet
after Seek Table packet if present at the end of the file, or the last
(group of) packet before the Stream End packet else. Chapters are presented
by the application in the same order as they appear in the file. When
used while streaming, this packet can be inserted between AP packets, and
the tag data is valid for the next samples, until a new CT packet is sent.


============= ================ ======= ===========================================
Field         Size (bits)      Value   Comment
============= ================ ======= ===========================================
Sample offset n*8; 0 < n < 10          Position of the chapter in samples.
                                       In a file from the beginning of the
                                       file, in a stream from the last sample
                                       before this packet
------------- ---------------- ------- -------------------------------------------
Chapter gain  16                       The loudness calculated for the chapter,
                                       and not the gain that the player must apply
------------- ---------------- ------- -------------------------------------------
Chapter peak  16
------------- ---------------- ------- -------------------------------------------
APEv2 tag     n*8                      APEv2 tag without the preamble
                                       { 'A', 'P', 'E', 'T', 'A', 'G', 'E', 'X' }
                                       in the header or footer, preferably without
                                       footer. This field is optional.
============= ================ ======= ===========================================


Security Packet
---------------

Checksum (MD5, SHA1) or error correcting code (LDPC). To be defined later.
May be better to keep security features external only.


Stream End Packet
-----------------

**[final]** This packet key is "SE". The packet size must be 3 bytes. This
packet is mandatory and must be the last stream packet. Tags, if present,
must be written after this packet.


Streaming
---------

**[alpha]** This file format can be used for streaming. The "SH" block is (can
be?) used as a synchronization marker. The decoder will scan for a "SH"
block and check its CRC. Once the decoder is synchronized, it will start
decoding. It's up to the streaming server to choose when to send "SH"
block. To send meta data while streaming, the Chapter-Tag packet can be used.


Tags
----

**[final]** No packet must be written after the stream end packet, to allow
tagging by other applications. Those tags are global to the file, and
define the default values for all the tag fields. The Chapter-Tag packet
can redefine the field value for each chapter.

Example file
------------

Packets keys and magic number are highlighted::

    00000000   4D 50 43 4B  53 48 0F 12  A5 AB 62 08  84 FA C1 40  00 1B 1B 52  MPCKSH....b....@...R
    00000014   47 0C 01 00  00 00 00 00  00 00 00 45  49 07 A0 01  17 00 53 4F  G..........EI.....SO
    00000028   08 82 C2 83  31 00 41 50  82 B2 01 BA  A7 36 59 FE  BC 7B CD 3E  ....1.AP.....6Y..{.>
    0000003C   10 3B EF 9B  3A 8E DA 22  0B 64 9A 67  AE EC 99 CB  2A 66 4C 79  .;..:..".d.g....*fLy

    ... Lots of Audio Packets

    005081C4   BF FF FF 85  03 81 B7 32  A0 2E 3A E0  D4 FC 20 16  A0 40 80 53  .......2..:... ..@.S
    005081D8   54 81 01 47  12 E8 58 21  73 01 83 DC  A8 1D 95 4B  D9 F5 37 EF  T..G..X!s......K..7.
    005081EC   A9 1E AB 86  CA 3A 1E 12  B7 F4 9A 2A  C4 76 84 13  79 95 09 FA  .....:.....*.v..y...
    00508200   AB D1 86 7C  53 0D BF 84  E9 B3 3F 42  13 EB 02 EE  A8 15 CC 79  ...|S.....?B.......y
    00508214   20 01 5C 41  0F 21 2A 99  27 78 A6 E8  45 BB 67 A3  10 DE 45 5E   .\A.!*.'x..E.g...E^
    00508228   8F 38 6B E2  5C 6E 44 09  86 E0 E6 B7  B3 77 67 80  21 04 BF 20  .8k.\nD......wg.!..
    0050823C   C7 FC BD 9D  77 A5 4D 8C  C5 38 38 F6  8D 52 2B FC  56 43 D5 5A  ....w.M..88..R+.VC.Z
    00508250   AE 2F AD B9  A2 51 D1 D0  53 45 03                               ./...Q..SE.

