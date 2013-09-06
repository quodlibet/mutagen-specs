=======================
ID3v2 Accessibility 1.0
=======================


Status of this document
-----------------------

This document is a proposed addendum to the ID3v2.3 and ID3v2.4 standards. 
Distribution of this document is unlimited.


Abstract
--------

This document describes extensions which make ID3v2 metadata accessible to 
the visually impaired. The approach may also be useful for audio players 
which have limited display capabilities. A new frame type is proposed that 
carries an audio clip which can provide a verbal expression of the textual 
information carried by another ID3v2 frame.


Conventions in this document
----------------------------

Text within "" is a text string exactly as it appears in a tag. Numbers 
preceded with $ are hexadecimal and numbers preceded with % are binary. $xx 
is used to indicate a byte with unknown content. %x is used to indicate a 
bit with unknown content. The most significant bit (MSB) of a byte is 
called 'bit 7' and the least significant bit (LSB) is called 'bit 0'.

A tag is the whole tag described the ID3v2 main structure document [2]. A 
frame is a block of information in the tag. The tag consists of a header, 
frames and optional padding. A field is a piece of information; one value, 
a string etc. A numeric string is a string that consists of the characters 
"0123456789" only.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", 
"SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this 
document are to be interpreted as described in RFC 2119.


Introduction
------------

The ID3v2 standards provide a way to deliver metadata that is predominantly 
human-readable, textual data. However, in this form the information is not 
easily accessible to the visually impaired.

The purpose of this Addendum is to allow content providers or third-party 
tools to provide an audio description (i.e. a spoken narrative) that is 
equivalent to the textual information carried by an ID3v2 frame. A new 
"audio-text" frame is defined which carries an audio clip and a matching 
equivalent text string. These text strings can be compared against the 
strings carried by other ID3v2 frames to identify when a matching audio 
description is available.

The audio clips can be played whenever the equivalent textual information 
is displayed or highlighted, providing a greatly improved user interface 
for the visually impaired. However, the feature may also be popular with 
other users and useful for media players with limited display capabilities.


Proposed audio-text frame
-------------------------

The purpose of this frame is to carry a short audio clip which represents 
the information carried by another ID3v2 frame that is present in the same 
tag.

To avoid these audio clips being confused with the main audio content of 
the file the ID3v2 unsynchronisation scheme must be used if the audio clip 
uses an MPEG audio format. If the unsynchronisation scheme is not 
appropriate for the audio format then the scrambling scheme defined in 
section 5 must be applied to the audio clip data.

::

    <ID3v2.3 or ID3v2.4 frame header, ID: "ATXT">
    Text encoding   $xx
    MIME type       <text string> $00
    Flags           %0000000a
    Equivalent text <text string according to encoding> $00 (00)
    Audio data      <binary data>

The Frame ID for the audio-text frame shall be set to "ATXT" using 
ISO-8859-1 character encoding.

The MIME type shall be represented as a terminated string encoded using 
ISO-8859-1 character encoding. Where the MIME type corresponds to MPEG 1/2 
layer I, II and III, MPEG 2.5 or AAC audio the ID3v2 unsynchronisation 
scheme should be applied, either to the audio-text frame or to the tag 
which contains it. For other MIME types the scrambling scheme defined in 
the Appendix should be applied to the audio data.

*Flag a - Scrambling flag*
    This flag shall be set if the scrambling method defined in Section 5 
    has been applied to the audio data, or not set if no scrambling has 
    been applied.

    The Equivalent text field carries a null terminated string encoded 
    according to the Text encoding byte as defined by the ID3v2 
    specifications [1], [2]. This text must be semantically equivalent to 
    the spoken narrative in the audio clip and should match the text and 
    encoding used by another ID3v2 frame in the tag.

    The Audio data carries an audio clip which provides the audio 
    description. The encoding of the audio data shall match the MIME type 
    field and the data shall be scrambled if the scrambling flag is set.

    More than one audio-text frame may be present in a tag but each must 
    carry a unique string in the Equivalent text field. 


Scrambling scheme for non-MPEG audio formats
--------------------------------------------

This scrambling scheme is provided for non-MPEG audio formats where the 
unsynchronisation scheme defined by the ID3v2 specifications is unsuitable. 
Each bit of the audio data is scrambled by taking the exclusive-OR (XOR) 
between it and the equivalent bit of a pseudo-random byte sequence. The 
first byte of this pseudo-random byte sequence is always %11111110 and is 
used to scramble the first byte of the audio data. The next byte of the 
sequence is derived from the current byte of the sequence using the 
algorithm in Table 1 and is used to scramble the next byte of audio data. 
This process is repeated until all bytes in the audio clip have been 
scrambled.

    +----------------------------------------+
    | Table 1: Scrambling sequence algorithm |
    +====================+===================+
    +     byte N+1       |      byte N       |
    +--------------------+-------------------+
    +     bit 7 =        |  bit 6 XOR bit 5  |
    +--------------------+-------------------+
    +     bit 6 =        |  bit 5 XOR bit 4  |
    +--------------------+-------------------+
    +     bit 5 =        |  bit 4 XOR bit 3  |
    +--------------------+-------------------+
    +     bit 4 =        |  bit 3 XOR bit 2  |
    +--------------------+-------------------+
    +     bit 3 =        |  bit 2 XOR bit 1  |
    +--------------------+-------------------+
    +     bit 2 =        |  bit 1 XOR bit 0  |
    +--------------------+-------------------+
    +     bit 1 =        |  bit 7 XOR bit 5  |
    +--------------------+-------------------+
    +     bit 0 =        |  bit 6 XOR bit 4  |
    +--------------------+-------------------+

This algorithm results in a 127-bit pseudo-random sequence which repeats on 
byte boundaries every 127 bytes. To recover the audio data from the 
scrambled data the scrambling procedure is repeated.


Notes
-----

* Failure to use the ID3v2 unsynchronisation scheme or the alternative 
  scrambling scheme, as appropriate to the audio format, is very likely to 
  confuse media players which are likely to start playback when an 
  audio-text frame in encountered rather than at the end of the ID3v2 tag.
* Players which only support MPEG audio formats are not required to support 
  the scrambling scheme provided for non-MPEG formats.
* It is not required to provide an audio-text frame to represent every text
  string present in a tag. The emphasis should be on text strings in frames 
  that are commonly used to identify and describe the content (e.g 
  ":ref:`TIT2<TIT2>`", ":ref:`TALB<TALB>`" & ":ref:`TPE1<TPE1>`").
* A parser that does not recognise "ATXT" frames can skip them using the size
  field in the frame header.
* Editing text fields in ID3 tags may result in the retention of irrelevant
  ATXT frames and gaps in the provision of audio text unless action is 
  taken to amend the corresponding ATXT frames. 

Copyright
---------

Copyright © BBC Future Media & Technology, 2006. All Rights Reserved.

This document and translations of it may be copied and furnished to others, 
and derivative works that comment on or otherwise explain it or assist in 
its implementation may be prepared, copied, published and distributed, in 
whole or in part, without restriction of any kind, provided that a 
reference to this document is included on all such copies and derivative 
works. However, this document itself may not be modified in any way and 
reissued as the original document.

The limited permissions granted above are perpetual and will not be revoked.

This document and the information contained herein is provided on an "AS 
IS" basis and THE AUTHORS DISCLAIM ALL WARRANTIES, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO ANY WARRANTY THAT THE USE OF THE INFORMATION 
HEREIN WILL NOT INFRINGE ANY RIGHTS OR ANY IMPLIED WARRANTIES OF 
MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.


References
----------

Martin Nilsson, ID3 tag version 2.3.0.

Martin Nilsson, ID3 tag version 2.4.0 - Main Structure.

M. Nilsson, "ID3 tag version 2.4.0 - Native frames.

S. Bradner, "Key words for use in RFCs to Indicate Requirement Levels", RFC 
2119, March 1997.


Author's address
----------------

| Chris Newell
| BBC Research & Development
| Kingswood Warren
| Tadworth
| Surrey
| KT20 6NP
| UK

Email: chris.newell at bbc.co.uk 
