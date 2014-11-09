ASF
===

Multiple Values
---------------

(Tested with Windows 8)

The following text keys support multiple values in Win8:

    Author, WM/Composer, WM/Conductor, WM/Producer, WM/Category, WM/Genre

For saving/reading multiple values:

 * For tags which can be in ContentDescription (Author) write the first value
   there, the rest in MetadataLibrary.
 * For tags which can be in ExtendedContentDescription (WM/Composer) write
   the first value there and the rest in MetadataLibrary.
 * When reading, the order in which the objects appear in the file doesn't
   matter. First value from ContentDescription, rest from MetadataLibrary etc.
