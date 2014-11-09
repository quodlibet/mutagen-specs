MP4
===

* `QuickTime File Format Specification <https://developer.apple.com/library/mac/documentation/quicktime/QTFF/qtff.pdf>`__
* `ISO_IEC_14496-12 <https://github.com/lucidwind/mpeg4/raw/master/ISO_IEC_14496-12_2008.pdf>`__
* `ISO_IEC_14496-14 <https://github.com/lucidwind/mpeg4/raw/master/ISO_IEC_14496-14-2003.pdf>`__


Multivalue Tags
---------------

.. note::

    not finished..

The only case where iTunes writes multiple values is the ``covr`` atom by 
including multiple ``data`` atoms.

For a collection of 1700 random mp4s the only place where multiple values 
occur is multiple ``----`` atoms with ``com.apple.iTunes:unknown`` as 
identifier.

Foobar2000 (1.3.3)

    Writing:
        Foobar writes single values in the official atoms and multiple values 
        in the reverse DNS namespace. Multiple values get saved as multiple 
        ``---`` with the same name and one `data` each.

    Reading:
        Foobar only reads the first `data` atom in all child atoms in ``ilst`` 
        and ``----``. Everything else gets ignored and thrown out on save.

iTunes (11.4)

    Writing:
        Given two ``\xa9gen`` atoms with each two ``data`` atoms. Modifying 
        the genre modifies the first data atom of the second ``\xa9gen`` atom 
        and it leaves the second ``data`` as is and writes is back. The first 
        ``\xa9gen`` atom gets thrown out. If the genre gets removed in the 
        iTunes GUI, both ``\xa9gen`` get thrown out.

    Reading:
        Given two ``\xa9gen`` atoms with each two ``data`` atoms it displays 
        the first ``data`` of the second ``\xa9gen``.

    No idea how it handles ``---`` atoms.

    So, multiple values for official ``ilst`` sub atoms should be saved
    as multiple ``data`` because iTunes will at least not touch other values
    and editing/display use the first one.


Random Struct Decls
-------------------

::

    class DecoderConfigDescriptor extends BaseDescriptor :
            bit(8) tag=DecoderConfigDescrTag {
        bit(8) objectTypeIndication;
        bit(6) streamType;
        bit(1) upStream;
        const bit(1) reserved=1;
        bit(24) bufferSizeDB;
        bit(32) maxBitrate;
        bit(32) avgBitrate;
        DecoderSpecificInfo decSpecificInfo[0 .. 1];
        profileLevelIndicationIndexDescriptor profileLevelIndicationIndexDescr[0..255];
    }

::

    class ES_Descriptor extends BaseDescriptor :
            bit(8) tag=ES_DescrTag {
        bit(16) ES_ID;
        bit(1) streamDependenceFlag;
        bit(1) URL_Flag;
        bit(1) OCRstreamFlag;
        bit(5) streamPriority;
        if (streamDependenceFlag)
            bit(16) dependsOn_ES_ID;
        if (URL_Flag) {
            bit(8) URLlength;
            bit(8) URLstring[URLlength];
        }
        if (OCRstreamFlag)
            bit(16) OCR_ES_Id;
        DecoderConfigDescriptor decConfigDescr;
        if (ODProfileLevelIndication==0x01) //no SL extension.
        {
            SLConfigDescriptor slConfigDescr;
        }
        else // SL extension is possible.
        {
            SLConfigDescriptor slConfigDescr;
        }
        IPI_DescrPointer ipiPtr[0 .. 1];
        IP_IdentificationDataSet ipIDS[0 .. 255];
        IPMP_DescriptorPointer ipmpDescrPtr[0 .. 255];
        LanguageDescriptor langDescr[0 .. 255];
        QoS_Descriptor qosDescr[0 .. 1];
        RegistrationDescriptor regDescr[0 .. 1];
        ExtensionDescriptor extDescr[0 .. 255];
    }

