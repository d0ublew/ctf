#define _CRT_SECURE_NO_WARNINGS

#include <Windows.h>
#include <iostream>

int main(int argc, char **argv) {
    IMAGE_DOS_HEADER dos;
    memset(&dos, 0, sizeof(IMAGE_DOS_HEADER));
    // Only these two fields are actually parsed
    dos.e_magic = 0x5A4D; // "MZ"
    dos.e_lfanew =
        sizeof(IMAGE_DOS_HEADER); // File address of new exe header (NT)

    IMAGE_NT_HEADERS32 nt_header;
    nt_header.Signature = 0x4550; // "PE"

    nt_header.FileHeader.Machine = IMAGE_FILE_MACHINE_I386;
    nt_header.FileHeader.NumberOfSections = 5; // text, data, rdata
    nt_header.FileHeader.TimeDateStamp = 0xfc03fc03;
    nt_header.FileHeader.PointerToSymbolTable = 0;
    nt_header.FileHeader.NumberOfSymbols = 0;
    nt_header.FileHeader.SizeOfOptionalHeader = sizeof(IMAGE_OPTIONAL_HEADER32);
    nt_header.FileHeader.Characteristics = IMAGE_FILE_DLL |
                                           IMAGE_FILE_LARGE_ADDRESS_AWARE |
                                           IMAGE_FILE_RELOCS_STRIPPED;

    nt_header.OptionalHeader.Magic = IMAGE_NT_OPTIONAL_HDR32_MAGIC;
    nt_header.OptionalHeader.MajorLinkerVersion = 0xe;
    nt_header.OptionalHeader.MinorLinkerVersion = 0x23;
    nt_header.OptionalHeader.SizeOfCode = 0xc600; // Size of .text section
    nt_header.OptionalHeader.SizeOfInitializedData =
        0x8800; // Size of .text + data sections
    nt_header.OptionalHeader.SizeOfUninitializedData = 0;
    nt_header.OptionalHeader.AddressOfEntryPoint = 0x18BD;
    nt_header.OptionalHeader.BaseOfCode =
        0x1000; // FIX if VA of .text is not 0x1000
    nt_header.OptionalHeader.BaseOfData =
        0xe000; // Start of .rdata section (RVA)
    nt_header.OptionalHeader.ImageBase = 0x10000000;
    nt_header.OptionalHeader.SectionAlignment = 0x1000;
    nt_header.OptionalHeader.FileAlignment = 0x200;
    nt_header.OptionalHeader.MajorOperatingSystemVersion = 6;
    nt_header.OptionalHeader.MinorOperatingSystemVersion = 0;
    nt_header.OptionalHeader.MajorImageVersion = 0;
    nt_header.OptionalHeader.MinorImageVersion = 0;
    nt_header.OptionalHeader.MajorSubsystemVersion = 6;
    nt_header.OptionalHeader.MinorSubsystemVersion = 0;
    nt_header.OptionalHeader.Win32VersionValue = 0;
    nt_header.OptionalHeader.SizeOfImage = 0x19000;
    nt_header.OptionalHeader.SizeOfHeaders = 0x400;
    nt_header.OptionalHeader.CheckSum = 0;
    nt_header.OptionalHeader.Subsystem = IMAGE_SUBSYSTEM_WINDOWS_GUI;
    nt_header.OptionalHeader.DllCharacteristics =
        IMAGE_DLLCHARACTERISTICS_NX_COMPAT |
        IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE;
    nt_header.OptionalHeader.SizeOfStackReserve = 0x100000;
    nt_header.OptionalHeader.SizeOfStackCommit = 0x1000;
    nt_header.OptionalHeader.SizeOfHeapReserve = 0x100000;
    nt_header.OptionalHeader.SizeOfHeapCommit = 0x1000;
    nt_header.OptionalHeader.LoaderFlags = 0;
    nt_header.OptionalHeader.NumberOfRvaAndSizes =
        IMAGE_NUMBEROF_DIRECTORY_ENTRIES;

    memset(nt_header.OptionalHeader.DataDirectory, 0,
           sizeof(IMAGE_DATA_DIRECTORY) * IMAGE_NUMBEROF_DIRECTORY_ENTRIES);

    // Export directory
    nt_header.OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_EXPORT]
        .VirtualAddress = 0x0138d0;
    nt_header.OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_EXPORT].Size =
        0x5c;

    // Import directory
    nt_header.OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_IMPORT]
        .VirtualAddress = 0x01392c;
    nt_header.OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_IMPORT].Size =
        0x50;

    // Resource directory
    nt_header.OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_RESOURCE]
        .VirtualAddress = 0x017000;
    nt_header.OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_RESOURCE]
        .Size = 0x1e0;

    // Relocation directory
    nt_header.OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_BASERELOC]
        .VirtualAddress = 0x018000;
    nt_header.OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_BASERELOC]
        .Size = 0x0ec4;

    // Debug directory
    nt_header.OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_DEBUG]
        .VirtualAddress = 0x012db8;
    nt_header.OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_DEBUG].Size =
        0x0070;

    // Configuration directory
    nt_header.OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_LOAD_CONFIG]
        .VirtualAddress = 0x012cf8;
    nt_header.OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_LOAD_CONFIG]
        .Size = 0x0040;

    // Import Address Table (IAT)
    nt_header.OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_IAT]
        .VirtualAddress = 0xe000;
    nt_header.OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_IAT].Size =
        0x130;

    IMAGE_EXPORT_DIRECTORY d;

    IMAGE_SECTION_HEADER text_section;
    memset(&text_section, 0, sizeof(IMAGE_SECTION_HEADER));
    const char text_name[] = ".sst0";
    memcpy(text_section.Name, text_name, sizeof(text_name));
    text_section.VirtualAddress = 0x1000;
    text_section.SizeOfRawData = 0xc600;
    text_section.Misc.VirtualSize = text_section.SizeOfRawData;
    text_section.PointerToRawData = 0x800;
    text_section.Characteristics =
        IMAGE_SCN_CNT_CODE | IMAGE_SCN_MEM_EXECUTE | IMAGE_SCN_MEM_READ;

    IMAGE_SECTION_HEADER rdata_section;
    memset(&rdata_section, 0, sizeof(IMAGE_SECTION_HEADER));
    const char rdata_name[] = ".sst1";
    memcpy(rdata_section.Name, rdata_name, sizeof(rdata_name));
    rdata_section.VirtualAddress = 0xe000;
    rdata_section.SizeOfRawData = 0x6200;
    rdata_section.Misc.VirtualSize = rdata_section.SizeOfRawData;
    rdata_section.PointerToRawData =
        text_section.SizeOfRawData + text_section.PointerToRawData;
    rdata_section.Characteristics =
        IMAGE_SCN_CNT_INITIALIZED_DATA | IMAGE_SCN_MEM_READ;

    IMAGE_SECTION_HEADER data_section;
    memset(&data_section, 0, sizeof(IMAGE_SECTION_HEADER));
    const char data_name[] = ".sst2";
    memcpy(data_section.Name, data_name, sizeof(data_name));
    data_section.VirtualAddress = 0x15000;
    data_section.SizeOfRawData = 0xa00;
    data_section.Misc.VirtualSize =
        data_section.SizeOfRawData; // Add a pseudo BSS section at the end of
                                    // this segment
    data_section.PointerToRawData =
        rdata_section.PointerToRawData + rdata_section.SizeOfRawData;
    data_section.Characteristics = IMAGE_SCN_CNT_INITIALIZED_DATA |
                                   IMAGE_SCN_MEM_READ | IMAGE_SCN_MEM_WRITE;

    IMAGE_SECTION_HEADER sst3_section;
    memset(&sst3_section, 0, sizeof(IMAGE_SECTION_HEADER));
    const char sst3_name[] = ".sst3";
    memcpy(sst3_section.Name, sst3_name, sizeof(sst3_name));
    sst3_section.VirtualAddress = 0x17000;
    sst3_section.SizeOfRawData = 0x200;
    sst3_section.Misc.VirtualSize =
        sst3_section.SizeOfRawData; // Add a pseudo BSS section at the end of
                                    // this segment
    sst3_section.PointerToRawData =
        data_section.PointerToRawData + data_section.SizeOfRawData;
    sst3_section.Characteristics =
        IMAGE_SCN_CNT_INITIALIZED_DATA | IMAGE_SCN_MEM_READ;

    IMAGE_SECTION_HEADER sst4_section;
    memset(&sst4_section, 0, sizeof(IMAGE_SECTION_HEADER));
    const char sst4_name[] = ".sst4";
    memcpy(sst4_section.Name, sst4_name, sizeof(sst4_name));
    sst4_section.VirtualAddress = 0x18000;
    sst4_section.SizeOfRawData = 0x1000;
    sst4_section.Misc.VirtualSize =
        sst4_section.SizeOfRawData; // Add a pseudo BSS section at the end of
                                    // this segment
    sst4_section.PointerToRawData =
        sst3_section.PointerToRawData + sst3_section.SizeOfRawData;
    sst4_section.Characteristics =
        IMAGE_SCN_CNT_INITIALIZED_DATA | IMAGE_SCN_MEM_READ;

    size_t header_size =
        sizeof(IMAGE_DOS_HEADER) + sizeof(IMAGE_NT_HEADERS32) +
        sizeof(IMAGE_SECTION_HEADER) * nt_header.FileHeader.NumberOfSections;
    size_t padding_size = text_section.PointerToRawData - header_size;
    size_t total_size =
        header_size + padding_size + text_section.SizeOfRawData +
        data_section.SizeOfRawData + rdata_section.SizeOfRawData +
        sst3_section.SizeOfRawData + sst4_section.SizeOfRawData;
    std::cout << header_size << std::endl;
    std::cout << padding_size << std::endl;
    std::cout << total_size << std::endl;

    unsigned char *buf = (unsigned char *)VirtualAlloc(
        NULL, total_size, MEM_COMMIT, PAGE_READWRITE);
    unsigned char *start = buf;

    // Headers
    memcpy(buf, &dos, sizeof(IMAGE_DOS_HEADER));
    buf += sizeof(IMAGE_DOS_HEADER);

    memcpy(buf, &nt_header, sizeof(IMAGE_NT_HEADERS32));
    buf += sizeof(IMAGE_NT_HEADERS32);

    memcpy(buf, &text_section, sizeof(IMAGE_SECTION_HEADER));
    buf += sizeof(IMAGE_SECTION_HEADER);

    memcpy(buf, &rdata_section, sizeof(IMAGE_SECTION_HEADER));
    buf += sizeof(IMAGE_SECTION_HEADER);

    memcpy(buf, &data_section, sizeof(IMAGE_SECTION_HEADER));
    buf += sizeof(IMAGE_SECTION_HEADER);

    memcpy(buf, &sst3_section, sizeof(IMAGE_SECTION_HEADER));
    buf += sizeof(IMAGE_SECTION_HEADER);

    memcpy(buf, &sst4_section, sizeof(IMAGE_SECTION_HEADER));
    buf += sizeof(IMAGE_SECTION_HEADER);

    // Padding
    buf += padding_size;

    // Binary data
    FILE *fp = fopen("C:\\Users\\d0ublew\\Desktop\\sst0.bin", "rb");
    fread(buf, 1, text_section.SizeOfRawData, fp);
    buf += text_section.SizeOfRawData;
    fclose(fp);

    fp = fopen("C:\\Users\\d0ublew\\Desktop\\sst1.bin", "rb");
    fread(buf, 1, rdata_section.SizeOfRawData, fp);
    buf += rdata_section.SizeOfRawData;
    fclose(fp);

    fp = fopen("C:\\Users\\d0ublew\\Desktop\\sst2.bin", "rb");
    fread(buf, 1, data_section.SizeOfRawData, fp);
    buf += data_section.SizeOfRawData;
    fclose(fp);

    fp = fopen("C:\\Users\\d0ublew\\Desktop\\sst3.bin", "rb");
    fread(buf, 1, sst3_section.SizeOfRawData, fp);
    buf += sst3_section.SizeOfRawData;
    fclose(fp);

    fp = fopen("C:\\Users\\d0ublew\\Desktop\\sst4.bin", "rb");
    fread(buf, 1, sst4_section.SizeOfRawData, fp);
    buf += sst4_section.SizeOfRawData;
    fclose(fp);

    fp = fopen("C:\\Users\\d0ublew\\Desktop\\new.dll", "wb");
    fwrite(start, 1, total_size, fp);
    fclose(fp);

    VirtualFree(buf, 0, MEM_RELEASE);

    return 0;
}
